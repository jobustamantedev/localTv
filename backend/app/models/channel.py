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
    source_id = Column(String(150), nullable=True, index=True)  # iptv-org channel id, eg: "CNN.us"
    country = Column(String(2), nullable=True, index=True)       # ISO 3166-1 alpha-2, eg: "US"
    quality = Column(String(10), nullable=True)                  # "1080p", "720p", "480p"

    category = relationship("Category", back_populates="channels")
