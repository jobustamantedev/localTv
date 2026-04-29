#!/usr/bin/env python
"""
Importación inicial de canales desde la API pública de iptv-org.

Uso:
    cd backend
    source venv/bin/activate
    python scripts/import_iptv.py

Opciones de filtrado (editar las constantes de abajo):
    COUNTRIES   - lista de códigos ISO para importar, ej: ["US", "MX", "ES"]
                  dejar vacía [] para importar todos los países
    MIN_QUALITY - calidad mínima aceptada en píxeles verticales (ej: 720)
                  poner 0 para importar sin filtrar calidad
    SKIP_NSFW   - omitir canales marcados como NSFW
"""

import sys
import re
import urllib.request
import json

sys.path.insert(0, ".")

from app.database import SessionLocal, Base, engine
from app.models.category import Category
from app.models.channel import Channel

# ── Configuración de filtros ──────────────────────────────────────────────────
COUNTRIES: list[str] = []   # ej: ["US", "MX"] — vacío = todos
MIN_QUALITY: int = 0        # píxeles verticales mínimos; 0 = sin filtro
SKIP_NSFW: bool = True
# ─────────────────────────────────────────────────────────────────────────────

API_BASE = "https://iptv-org.github.io/api"


def fetch_json(endpoint: str) -> list[dict]:
    url = f"{API_BASE}/{endpoint}.json"
    print(f"  Descargando {url} ...")
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:98]


def unique_slug(base: str, existing: set[str]) -> str:
    slug = slugify(base)
    candidate = slug
    counter = 1
    while candidate in existing:
        candidate = f"{slug}-{counter}"
        counter += 1
    existing.add(candidate)
    return candidate


def parse_quality(quality_str) -> int:
    """Devuelve el número de líneas verticales, ej '720p' → 720."""
    if not quality_str:
        return 0
    match = re.match(r"(\d+)", quality_str)
    return int(match.group(1)) if match else 0


def main():
    print("=== Importación iptv-org → bustaTv ===\n")

    # 1. Descargar datos de la API
    print("[1/5] Descargando datos de la API...")
    raw_streams = fetch_json("streams")
    raw_channels = fetch_json("channels")
    raw_logos = fetch_json("logos")
    raw_categories = fetch_json("categories")

    # 2. Construir índices en memoria
    print("\n[2/5] Construyendo índices...")

    # channel_id → metadata del canal
    channels_by_id: dict[str, dict] = {c["id"]: c for c in raw_channels}

    # channel_id → mejor logo (in_use primero, luego PNG)
    logos_by_channel: dict[str, str] = {}
    for logo in raw_logos:
        cid = logo.get("channel")
        if not cid:
            continue
        if logo.get("in_use") and cid not in logos_by_channel:
            logos_by_channel[cid] = logo["url"]
        elif cid not in logos_by_channel:
            logos_by_channel[cid] = logo["url"]

    print(f"  Canales en API:    {len(channels_by_id):,}")
    print(f"  Logos disponibles: {len(logos_by_channel):,}")
    print(f"  Streams totales:   {len(raw_streams):,}")

    # 3. Filtrar streams
    print("\n[3/5] Aplicando filtros...")

    filtered = []
    skipped_no_id = 0
    skipped_nsfw = 0
    skipped_country = 0
    skipped_quality = 0

    seen_source_ids: set[str] = set()  # un stream por canal (el de mejor calidad)

    # Ordenar streams por calidad descendente para quedarnos con el mejor
    raw_streams_sorted = sorted(
        raw_streams,
        key=lambda s: parse_quality(s.get("quality")),
        reverse=True,
    )

    for stream in raw_streams_sorted:
        source_id = stream.get("channel")

        # Omitir streams sin channel_id (sin metadata enriquecida)
        if not source_id:
            skipped_no_id += 1
            continue

        # Un stream por canal
        if source_id in seen_source_ids:
            continue

        channel_meta = channels_by_id.get(source_id, {})

        # Filtro NSFW
        if SKIP_NSFW and channel_meta.get("is_nsfw"):
            skipped_nsfw += 1
            continue

        # Filtro por país
        country = channel_meta.get("country", "")
        if COUNTRIES and country not in COUNTRIES:
            skipped_country += 1
            continue

        # Filtro por calidad
        if MIN_QUALITY and parse_quality(stream.get("quality")) < MIN_QUALITY:
            skipped_quality += 1
            continue

        seen_source_ids.add(source_id)
        filtered.append((stream, channel_meta, country))

    print(f"  Sin channel_id:    {skipped_no_id:,}")
    print(f"  NSFW omitidos:     {skipped_nsfw:,}")
    print(f"  País no incluido:  {skipped_country:,}")
    print(f"  Calidad baja:      {skipped_quality:,}")
    print(f"  A importar:        {len(filtered):,}")

    if not filtered:
        print("\n  Nada que importar con los filtros actuales.")
        return

    # 4. Insertar en la base de datos
    print("\n[4/5] Insertando en la base de datos...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Crear o recuperar categorías de iptv-org
        category_map: dict[str, int] = {}  # iptv-org category_id → BD id

        for cat in raw_categories:
            if cat["id"] == "xxx":
                continue  # nunca importar xxx
            existing = db.query(Category).filter(Category.slug == cat["id"]).first()
            if existing:
                category_map[cat["id"]] = existing.id
            else:
                new_cat = Category(
                    name=cat["name"],
                    slug=cat["id"],
                    icon=None,
                )
                db.add(new_cat)
                db.flush()
                category_map[cat["id"]] = new_cat.id

        # Categoría fallback para canales sin categoría
        fallback_slug = "general"
        if fallback_slug not in category_map:
            gen = db.query(Category).filter(Category.slug == fallback_slug).first()
            category_map[fallback_slug] = gen.id if gen else list(category_map.values())[0]

        # Insertar canales
        existing_slugs: set[str] = {
            row[0] for row in db.query(Channel.slug).all()
        }
        existing_source_ids: set[str] = {
            row[0] for row in db.query(Channel.source_id).filter(Channel.source_id.isnot(None)).all()
        }

        inserted = 0
        skipped_dup = 0

        for stream, channel_meta, country in filtered:
            source_id = stream["channel"]

            # Omitir si ya existe en la BD
            if source_id in existing_source_ids:
                skipped_dup += 1
                continue

            # Resolver categoría: tomar la primera del canal
            categories_list = channel_meta.get("categories", [])
            cat_slug = categories_list[0] if categories_list else fallback_slug
            category_id = category_map.get(cat_slug, category_map[fallback_slug])

            name = stream.get("title") or channel_meta.get("name") or source_id
            slug = unique_slug(name, existing_slugs)
            logo_url = logos_by_channel.get(source_id)
            quality = stream.get("quality")

            channel = Channel(
                name=name,
                slug=slug,
                stream_url=stream["url"],
                logo_url=logo_url,
                category_id=category_id,
                is_active=True,
                source_id=source_id,
                country=country or None,
                quality=quality or None,
            )
            db.add(channel)
            existing_source_ids.add(source_id)
            inserted += 1

            if inserted % 500 == 0:
                db.flush()
                print(f"  ... {inserted:,} insertados")

        db.commit()
        print(f"\n  Duplicados omitidos: {skipped_dup:,}")
        print(f"  Canales insertados:  {inserted:,}")

    except Exception as e:
        db.rollback()
        print(f"\n  ERROR: {e}")
        raise
    finally:
        db.close()

    # 5. Resumen
    print("\n[5/5] Listo.")
    print(f"  Importación completada. {inserted:,} canales nuevos en la BD.")


if __name__ == "__main__":
    main()
