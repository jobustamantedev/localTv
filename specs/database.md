# bustaTv — Especificación Base de Datos

## Motor: SQLite
Archivo: `backend/bustaTv.db`

SQLite es suficiente para uso local educativo. El archivo se crea automáticamente al ejecutar Alembic.

## Schema Completo

### Tabla: `categories`

```sql
CREATE TABLE categories (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      VARCHAR(100) NOT NULL,
    slug      VARCHAR(100) NOT NULL UNIQUE,
    icon      VARCHAR(255)
);

CREATE INDEX ix_categories_slug ON categories(slug);
```

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | INTEGER | PK | Identificador único |
| name | VARCHAR(100) | NOT NULL | Nombre legible: "Deportes" |
| slug | VARCHAR(100) | NOT NULL, UNIQUE | URL-friendly: "deportes" |
| icon | VARCHAR(255) | nullable | Clase FontAwesome: "fa-futbol" |

### Tabla: `channels`

```sql
CREATE TABLE channels (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100) NOT NULL,
    slug        VARCHAR(100) NOT NULL UNIQUE,
    stream_url  VARCHAR(500) NOT NULL,
    logo_url    VARCHAR(500),
    category_id INTEGER NOT NULL REFERENCES categories(id),
    is_active   BOOLEAN NOT NULL DEFAULT 1,
    created_at  DATETIME DEFAULT (CURRENT_TIMESTAMP)
);

CREATE INDEX ix_channels_slug     ON channels(slug);
CREATE INDEX ix_channels_category ON channels(category_id);
CREATE INDEX ix_channels_active   ON channels(is_active);
```

| Columna | Tipo | Restricciones | Descripción |
|---|---|---|---|
| id | INTEGER | PK | Identificador único |
| name | VARCHAR(100) | NOT NULL | Nombre del canal: "ESPN" |
| slug | VARCHAR(100) | NOT NULL, UNIQUE | URL-friendly: "espn" |
| stream_url | VARCHAR(500) | NOT NULL | URL del stream: `https://tvtvhd.com/vivo/canales.php?stream=espn` |
| logo_url | VARCHAR(500) | nullable | URL del logo: `https://upload.wikimedia.org/...` |
| category_id | INTEGER | FK → categories.id | Categoría del canal |
| is_active | BOOLEAN | NOT NULL, DEFAULT 1 | Si el canal está disponible (no visible si es false) |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

## Diagrama Relacional

```
┌──────────────────────┐        ┌──────────────────────────────────┐
│     categories       │        │           channels                │
├──────────────────────┤        ├──────────────────────────────────┤
│ id       INTEGER PK  │◄───┐   │ id           INTEGER PK           │
│ name     VARCHAR     │    └───┼ category_id  INTEGER FK           │
│ slug     VARCHAR UNQ │    1:N │ name         VARCHAR UNQ          │
│ icon     VARCHAR     │        │ slug         VARCHAR UNQ          │
└──────────────────────┘        │ stream_url   VARCHAR              │
                                │ logo_url     VARCHAR              │
                                │ is_active    BOOLEAN              │
                                │ created_at   DATETIME             │
                                └──────────────────────────────────┘
```

## Seed Data — Datos Iniciales

### Categorías

```python
categories = [
    {"name": "Deportes", "slug": "deportes", "icon": "fa-futbol"},
    {"name": "Reality", "slug": "reality", "icon": "fa-tv"},
]
```

### Canales (basados en URLs encontradas en tvtvhd.com)

```python
channels = [
    {
        "name": "ESPN",
        "slug": "espn",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=espn",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ESPN_wordmark.svg/200px-ESPN_wordmark.svg.png",
        "category_id": 1,  # Deportes
        "is_active": True,
    },
    {
        "name": "ESPN 2",
        "slug": "espn2",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=espn2",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ESPN_wordmark.svg/200px-ESPN_wordmark.svg.png",
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "ESPN 3",
        "slug": "espn3",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=espn3",
        "logo_url": None,
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "ESPN 4",
        "slug": "espn4",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=espn4",
        "logo_url": None,
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "ESPN 5",
        "slug": "espn5",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=espn5",
        "logo_url": None,
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "ESPN 6",
        "slug": "espn6",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=espn6",
        "logo_url": None,
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "ESPN 7",
        "slug": "espn7",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=espn7",
        "logo_url": None,
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "DSports",
        "slug": "dsports",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=dsports",
        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/DirectTV_Sports_logo.png/200px-DirectTV_Sports_logo.png",
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "DSports+",
        "slug": "dsports-plus",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=dsportsplus",
        "logo_url": None,
        "category_id": 1,
        "is_active": True,
    },
    {
        "name": "DSports 2",
        "slug": "dsports2",
        "stream_url": "https://tvtvhd.com/vivo/canales.php?stream=dsports2",
        "logo_url": None,
        "category_id": 1,
        "is_active": True,
    },
]
```

## Script Seed — `backend/scripts/seed.py`

```python
#!/usr/bin/env python
"""
Script para poblar la base de datos con datos iniciales.
Uso: cd backend && python scripts/seed.py
"""

import sys
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.category import Category
from app.models.channel import Channel

def seed():
    """Poblar BD con categorías y canales."""
    db = SessionLocal()

    # Verificar si ya existen datos
    existing_categories = db.query(Category).count()
    if existing_categories > 0:
        print("⚠️  La BD ya tiene datos. Abortando para evitar duplicados.")
        db.close()
        return

    # Crear categorías
    categories = [
        Category(name="Deportes", slug="deportes", icon="fa-futbol"),
        Category(name="Reality", slug="reality", icon="fa-tv"),
    ]
    db.add_all(categories)
    db.flush()  # Asignar IDs sin commit
    db.refresh(categories[0])
    db.refresh(categories[1])

    deportes_id = categories[0].id

    # Crear canales
    channels = [
        Channel(
            name="ESPN",
            slug="espn",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn",
            logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ESPN_wordmark.svg/200px-ESPN_wordmark.svg.png",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="ESPN 2",
            slug="espn2",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn2",
            logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/ESPN_wordmark.svg/200px-ESPN_wordmark.svg.png",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="ESPN 3",
            slug="espn3",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn3",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="ESPN 4",
            slug="espn4",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn4",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="ESPN 5",
            slug="espn5",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn5",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="ESPN 6",
            slug="espn6",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn6",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="ESPN 7",
            slug="espn7",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=espn7",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="DSports",
            slug="dsports",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=dsports",
            logo_url="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/DirectTV_Sports_logo.png/200px-DirectTV_Sports_logo.png",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="DSports+",
            slug="dsports-plus",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=dsportsplus",
            category_id=deportes_id,
            is_active=True,
        ),
        Channel(
            name="DSports 2",
            slug="dsports2",
            stream_url="https://tvtvhd.com/vivo/canales.php?stream=dsports2",
            category_id=deportes_id,
            is_active=True,
        ),
    ]
    db.add_all(channels)
    db.commit()

    print("✅ Seed completado!")
    print(f"   - Categorías: {len(categories)}")
    print(f"   - Canales: {len(channels)}")
    db.close()

if __name__ == "__main__":
    seed()
```

**Ejecutar después de crear las tablas:**
```bash
cd backend
python scripts/seed.py
```

## Migraciones con Alembic

### Setup inicial

```bash
cd backend
alembic init alembic
```

Esto crea la carpeta `alembic/` con la estructura necesaria.

### Configurar Alembic

**Editar `alembic/env.py`:**
```python
# ... (primeras líneas de env.py)

from app.database import Base
from app.models import channel, category  # Importar modelos

target_metadata = Base.metadata

# ... (resto del archivo)
```

**Editar `alembic.ini`:**
```ini
sqlalchemy.url = sqlite:///./bustaTv.db
```

### Crear primera migración

```bash
alembic revision --autogenerate -m "initial_schema"
```

Esto genera un archivo en `alembic/versions/` que describe las tablas.

### Aplicar migraciones

```bash
alembic upgrade head
```

### Flujo de trabajo para cambios de schema

Cuando modificas un modelo:

1. Edita `app/models/channel.py` o `app/models/category.py`
2. Genera la migración:
   ```bash
   alembic revision --autogenerate -m "descripcion_del_cambio"
   ```
3. Revisa el archivo en `alembic/versions/`
4. Aplica:
   ```bash
   alembic upgrade head
   ```
5. Para rollback (deshacer):
   ```bash
   alembic downgrade -1
   ```

### Comandos útiles

```bash
alembic history          # Ver historial de migraciones
alembic current          # Ver migración actual aplicada
alembic branches         # Ver ramas de migraciones
alembic upgrade head     # Aplicar todas las migraciones
alembic downgrade -1     # Deshacer la última migración
```

## Consultas SQL de Referencia

### Obtener todos los canales con categoría

```sql
SELECT
    c.id, c.name, c.slug, c.stream_url, c.logo_url, c.is_active,
    cat.id as category_id, cat.name as category_name, cat.slug as category_slug
FROM channels c
LEFT JOIN categories cat ON c.category_id = cat.id
WHERE c.is_active = 1
ORDER BY cat.name, c.name;
```

### Canales por categoría

```sql
SELECT c.* FROM channels c
JOIN categories cat ON c.category_id = cat.id
WHERE cat.slug = 'deportes' AND c.is_active = 1
ORDER BY c.name;
```

### Canales inactivos (deshabilitados)

```sql
SELECT * FROM channels WHERE is_active = 0;
```

### Contar canales por categoría

```sql
SELECT cat.name, COUNT(c.id) as count
FROM categories cat
LEFT JOIN channels c ON c.category_id = cat.id
GROUP BY cat.id
ORDER BY cat.name;
```

## Inspeccionar la BD

### Usando `sqlite3` CLI

```bash
sqlite3 backend/bustaTv.db

# Ver todas las tablas
.tables

# Ver schema de una tabla
.schema channels

# Ver datos de una tabla
SELECT * FROM channels;

# Salir
.quit
```

### Usando un cliente GUI

- **DB Browser for SQLite** (multiplataforma, gratis)
- **DBeaver Community** (multiplataforma, gratis)
- Visual Studio Code con extensión SQLite

## Notas Importantes

1. **Datos iniciales:** El script `seed.py` solo funciona si la BD está vacía. Si quieres hacer reset, elimina `bustaTv.db`.

2. **URLs de streams:** Las URLs apuntan a tvtvhd.com. Si ese servicio cae o cambia, los streams no funcionarán. Esto es normal en un proyecto educativo — en producción habría que investigar fuentes más confiables.

3. **Slugs únicos:** El slug es un identificador única para cada canal/categoría. Útil para URLs amigables como `/channel/espn`.

4. **is_active:** Permite "archivar" canales sin borrarlos. Los canales con `is_active = 0` no aparecen en la UI por defecto.

5. **Migraciones:** Alembic es lo correcto para gestionar cambios de schema. Nunca edites manualmente las tablas en SQL — siempre usa migraciones.
