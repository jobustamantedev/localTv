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
    source_id: Optional[str] = None
    country: Optional[str] = None
    quality: Optional[str] = None

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
    source_id: Optional[str] = None
    country: Optional[str] = None
    quality: Optional[str] = None

    model_config = {"from_attributes": True}
