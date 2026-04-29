#!/usr/bin/env python
"""
Sync diferencial diario contra la API pública de iptv-org.

Qué hace:
  - Descarga el streams.json actualizado de iptv-org (se actualiza cada día ~00:00 UTC)
  - Para cada stream con channel_id conocido en nuestra BD:
      * Actualiza la stream_url si cambió
      * Reactiva el canal si volvió a aparecer
  - Marca is_active=False los canales que ya no aparecen en la API
  - Informa un resumen de los cambios

Uso:
    cd backend
    source venv/bin/activate
    python scripts/sync_iptv.py

Automatizar (añadir al crontab del servidor):
    0 1 * * *  cd /ruta/a/bustaTv/backend && source venv/bin/activate && python scripts/sync_iptv.py >> logs/sync.log 2>&1
"""

import sys
import json
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, ".")

from app.database import SessionLocal
from app.models.channel import Channel

API_STREAMS_URL = "https://iptv-org.github.io/api/streams.json"


def fetch_streams() -> list[dict]:
    print(f"  Descargando {API_STREAMS_URL} ...")
    with urllib.request.urlopen(API_STREAMS_URL, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"=== Sync iptv-org → bustaTv  [{now}] ===\n")

    # 1. Descargar streams frescos de iptv-org
    print("[1/4] Descargando streams actualizados...")
    raw_streams = fetch_streams()

    # Quedarnos solo con streams que tienen channel_id
    # y elegir el de mejor calidad por canal (mismo criterio que import)
    import re

    def parse_quality(q) -> int:
        if not q:
            return 0
        m = re.match(r"(\d+)", q)
        return int(m.group(1)) if m else 0

    raw_streams_sorted = sorted(
        raw_streams,
        key=lambda s: parse_quality(s.get("quality")),
        reverse=True,
    )

    # source_id → {url, quality}
    api_streams: dict[str, dict] = {}
    for s in raw_streams_sorted:
        cid = s.get("channel")
        if cid and cid not in api_streams:
            api_streams[cid] = {
                "url": s["url"],
                "quality": s.get("quality"),
            }

    print(f"  Streams en API con channel_id: {len(api_streams):,}")

    # 2. Cargar canales de nuestra BD que tienen source_id (importados de iptv-org)
    print("\n[2/4] Cargando canales locales con source_id...")
    db = SessionLocal()

    try:
        local_channels: list[Channel] = (
            db.query(Channel)
            .filter(Channel.source_id.isnot(None))
            .all()
        )
        print(f"  Canales en BD con source_id: {len(local_channels):,}")

        # 3. Calcular diferencias
        print("\n[3/4] Calculando diferencias...")

        updated_url = 0
        reactivated = 0
        deactivated = 0
        unchanged = 0

        for channel in local_channels:
            api_data = api_streams.get(channel.source_id)

            if api_data is None:
                # El canal desapareció de la API → desactivar
                if channel.is_active:
                    channel.is_active = False
                    deactivated += 1
                continue

            changed = False

            # ¿Cambió la URL?
            if channel.stream_url != api_data["url"]:
                channel.stream_url = api_data["url"]
                changed = True
                updated_url += 1

            # ¿Cambió la calidad?
            if api_data.get("quality") and channel.quality != api_data["quality"]:
                channel.quality = api_data["quality"]
                changed = True

            # ¿Estaba desactivado y volvió?
            if not channel.is_active:
                channel.is_active = True
                reactivated += 1
                changed = True

            if not changed:
                unchanged += 1

        db.commit()

        # 4. Resumen
        print("\n[4/4] Resumen del sync:")
        print(f"  URLs actualizadas:   {updated_url:,}")
        print(f"  Canales reactivados: {reactivated:,}")
        print(f"  Canales desactivados:{deactivated:,}")
        print(f"  Sin cambios:         {unchanged:,}")
        print(f"\n  Sync completado. [{now}]")

    except Exception as e:
        db.rollback()
        print(f"\n  ERROR: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
