import re
import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.channels import get_channel_by_slug

router = APIRouter(prefix="/api/streams", tags=["streams"])

TVTVHD_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://tvtvhd.com/",
}


async def _scrape_tvtvhd(channel_slug: str) -> str:
    """Extrae la URL real del stream desde tvtvhd.com (solo canales legacy)."""
    tvtvhd_url = f"https://tvtvhd.com/vivo/canales.php?stream={channel_slug}"

    async with httpx.AsyncClient(timeout=10, headers=TVTVHD_HEADERS, follow_redirects=True) as client:
        response = await client.get(tvtvhd_url)
        html = response.text

    for pattern in [
        r'playbackURL\s*[=:]\s*["\']?([^"\'<>]+\.m3u8[^"\'<>]*)["\']?',
        r'<source[^>]+src=["\']([^"\']+\.m3u8[^"\']*)["\']',
        r'(https?://[^"\'<>\s]+\.m3u8[^"\'<>\s]*)',
    ]:
        match = re.search(pattern, html)
        if match:
            url = match.group(1)
            if url.startswith("http"):
                return url

    raise HTTPException(status_code=502, detail="No se encontró la URL del stream en la fuente")


@router.get("/{channel_slug}")
async def get_stream(channel_slug: str, db: Session = Depends(get_db)):
    """
    Devuelve la URL de stream para un canal.
    - Canales de iptv-org: URL directa desde la BD (sin scraping).
    - Canales legacy (tvtvhd.com): extrae la URL real vía scraping.
    """
    channel = get_channel_by_slug(db, channel_slug)
    if not channel:
        raise HTTPException(status_code=404, detail="Canal no encontrado")

    stream_url = channel.stream_url

    # Canales legacy cuya URL es una página de tvtvhd.com, no un m3u8 directo
    if "tvtvhd.com" in stream_url:
        stream_url = await _scrape_tvtvhd(channel_slug)

    return {
        "url": stream_url,
        "channel": channel_slug,
        "quality": channel.quality,
        "country": channel.country,
    }
