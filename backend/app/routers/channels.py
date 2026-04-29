from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.crud import channels as crud_channels
from app.schemas.channel import ChannelCreate, ChannelRead, ChannelUpdate
from app.auth import require_api_key

router = APIRouter(prefix="/api/channels", tags=["channels"])

# Público
@router.get("/countries")
def read_countries(db: Session = Depends(get_db)):
    return crud_channels.get_countries(db)

@router.get("/", response_model=list[ChannelRead])
def read_channels(
    db: Session = Depends(get_db),
    active_only: bool = True,
    category_slug: Optional[str] = None,
    country: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    return crud_channels.get_channels(
        db, active_only, category_slug, country, search, limit, offset
    )

@router.get("/count")
def read_channels_count(
    db: Session = Depends(get_db),
    active_only: bool = True,
    category_slug: Optional[str] = None,
    country: Optional[str] = None,
    search: Optional[str] = None,
):
    return {
        "count": crud_channels.get_channels_count(
            db, active_only, category_slug, country, search
        )
    }

@router.get("/slug/{slug}", response_model=ChannelRead)
def read_channel_by_slug(slug: str, db: Session = Depends(get_db)):
    db_channel = crud_channels.get_channel_by_slug(db, slug)
    if not db_channel:
        raise HTTPException(status_code=404, detail="Channel not found")
    return db_channel

@router.get("/{channel_id}", response_model=ChannelRead)
def read_channel(channel_id: int, db: Session = Depends(get_db)):
    db_channel = crud_channels.get_channel(db, channel_id)
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
