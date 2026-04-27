# bustaTv — Especificación Backend

## Stack
- Python 3.11+
- FastAPI 0.111+
- SQLAlchemy 2.0 (ORM)
- Alembic (migraciones)
- Uvicorn (servidor ASGI)
- SQLite (base de datos)
- Pydantic v2 (validación)

## Estructura de Carpetas

```
backend/
├── main.py                    # Entry point: crea app FastAPI
├── requirements.txt
├── .env                       # SECRET_API_KEY, DATABASE_URL
├── alembic.ini                # Config Alembic
├── bustaTv.db                 # SQLite (generado en runtime)
│
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 001_initial_schema.py
│
├── app/
│   ├── __init__.py
│   ├── config.py              # Settings via pydantic-settings
│   ├── database.py            # Engine, SessionLocal, Base, get_db
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── channel.py         # SQLAlchemy: Channel
│   │   └── category.py        # SQLAlchemy: Category
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── channel.py         # Pydantic: ChannelCreate, ChannelRead, etc
│   │   └── category.py        # Pydantic: CategoryCreate, CategoryRead
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── channels.py        # Endpoints CRUD canales
│   │   └── categories.py      # Endpoints categorías
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── channels.py        # Funciones DB canales
│   │   └── categories.py      # Funciones DB categorías
│   │
│   └── auth.py                # Validación API key
│
└── scripts/
    └── seed.py                # Poblar BD con datos iniciales
```

## Modelos SQLAlchemy

### `app/models/category.py`

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    icon = Column(String(255), nullable=True)  # FontAwesome o URL

    channels = relationship("Channel", back_populates="category")
```

### `app/models/channel.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    stream_url = Column(String(500), nullable=False)
    logo_url = Column(String(500), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="channels")
```

## Schemas Pydantic

### `app/schemas/category.py`

```python
from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

    model_config = {"from_attributes": True}
```

### `app/schemas/channel.py`

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChannelBase(BaseModel):
    name: str
    slug: str
    stream_url: str
    logo_url: Optional[str] = None
    category_id: int
    is_active: bool = True

class ChannelCreate(ChannelBase):
    pass

class ChannelUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    stream_url: Optional[str] = None
    logo_url: Optional[str] = None
    category_id: Optional[int] = None
    is_active: Optional[bool] = None

class ChannelRead(ChannelBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
```

## CRUD Layer

### `app/crud/categories.py`

```python
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate

def get_categories(db: Session):
    return db.query(Category).all()

def get_category_by_slug(db: Session, slug: str):
    return db.query(Category).filter(Category.slug == slug).first()

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
```

### `app/crud/channels.py`

```python
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.channel import Channel
from app.schemas.channel import ChannelCreate, ChannelUpdate

def get_channels(
    db: Session,
    active_only: bool = True,
    category_slug: str = None
):
    query = db.query(Channel)

    if active_only:
        query = query.filter(Channel.is_active == True)

    if category_slug:
        from app.models.category import Category
        query = query.join(Category).filter(Category.slug == category_slug)

    return query.all()

def get_channel(db: Session, channel_id: int):
    return db.query(Channel).filter(Channel.id == channel_id).first()

def get_channel_by_slug(db: Session, slug: str):
    return db.query(Channel).filter(Channel.slug == slug).first()

def create_channel(db: Session, channel: ChannelCreate):
    db_channel = Channel(**channel.model_dump())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def update_channel(db: Session, channel_id: int, updates: ChannelUpdate):
    db_channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not db_channel:
        return None

    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_channel, key, value)

    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

def delete_channel(db: Session, channel_id: int):
    db_channel = db.query(Channel).filter(Channel.id == channel_id).first()
    if not db_channel:
        return False

    db.delete(db_channel)
    db.commit()
    return True
```

## Routers

### `app/routers/categories.py`

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import categories as crud_categories
from app.schemas.category import CategoryRead

router = APIRouter(prefix="/api/categories", tags=["categories"])

@router.get("/", response_model=list[CategoryRead])
def read_categories(db: Session = Depends(get_db)):
    return crud_categories.get_categories(db)
```

### `app/routers/channels.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import channels as crud_channels
from app.schemas.channel import ChannelCreate, ChannelRead, ChannelUpdate
from app.auth import require_api_key

router = APIRouter(prefix="/api/channels", tags=["channels"])

# Público
@router.get("/", response_model=list[ChannelRead])
def read_channels(
    db: Session = Depends(get_db),
    active_only: bool = True,
    category_slug: str = None
):
    return crud_channels.get_channels(db, active_only, category_slug)

@router.get("/{channel_id}", response_model=ChannelRead)
def read_channel(channel_id: int, db: Session = Depends(get_db)):
    db_channel = crud_channels.get_channel(db, channel_id)
    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return db_channel

@router.get("/slug/{slug}", response_model=ChannelRead)
def read_channel_by_slug(slug: str, db: Session = Depends(get_db)):
    db_channel = crud_channels.get_channel_by_slug(db, slug)
    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return db_channel

# Admin (requiere API key)
@router.post("/", response_model=ChannelRead, status_code=status.HTTP_201_CREATED)
def create_channel(
    channel: ChannelCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    return crud_channels.create_channel(db, channel)

@router.put("/{channel_id}", response_model=ChannelRead)
def update_channel(
    channel_id: int,
    channel_update: ChannelUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    db_channel = crud_channels.update_channel(db, channel_id, channel_update)
    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return db_channel

@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(
    channel_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(require_api_key)
):
    success = crud_channels.delete_channel(db, channel_id)
    if not success:
        raise HTTPException(status_code=404, detail="Channel not found")
    return None
```

## Autenticación

### `app/auth.py`

```python
from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_api_key(api_key: str = Security(api_key_header)):
    if api_key is None or api_key != settings.SECRET_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )
    return api_key
```

## Configuración

### `app/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./bustaTv.db"
    SECRET_API_KEY: str = "bustatv-dev-secret-key-changeme"

    class Config:
        env_file = ".env"

settings = Settings()
```

### `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Main Entry Point

### `main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import channels, categories

# Crear tablas en la BD
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="bustaTv API",
    description="API para la plataforma de streaming bustaTv",
    version="1.0.0",
)

# CORS para React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(channels.router)
app.include_router(categories.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "bustaTv API v1.0"}
```

## Requirements.txt

```
fastapi==0.111.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.30
alembic==1.13.1
pydantic==2.7.0
pydantic-settings==2.2.1
python-dotenv==1.0.1
```

## .env (Development)

```
DATABASE_URL=sqlite:///./bustaTv.db
SECRET_API_KEY=bustatv-dev-secret-key-changeme
```

**IMPORTANTE:** En producción, cambiar la API key a algo seguro y usar secrets management.

## Correr el Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/seed.py     # Poblar BD con datos iniciales
uvicorn main:app --reload --port 8000
```

El backend estará disponible en `http://localhost:8000`
Documentación automática: `http://localhost:8000/docs` (Swagger UI)

## Endpoints Resumido

### Públicos (sin autenticación)
- `GET /api/channels` — lista de canales
- `GET /api/channels/{id}` — detalle canal por ID
- `GET /api/channels/slug/{slug}` — detalle canal por slug
- `GET /api/categories` — lista de categorías

### Admin (requieren header `X-API-Key: {value}`)
- `POST /api/channels` — crear canal
- `PUT /api/channels/{id}` — actualizar canal
- `DELETE /api/channels/{id}` — eliminar canal

### Health
- `GET /health` — estado del servidor
