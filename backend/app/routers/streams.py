import re
import httpx
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.responses import StreamingResponse
from app.database import get_db
from app.crud.channels import get_channel_by_slug

router = APIRouter(prefix="/api/streams", tags=["streams"])

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://tvtvhd.com/",
}

async def get_stream_url_from_tvtvhd(channel_slug: str) -> str:
    """Extrae la URL real del stream desde tvtvhd.com"""
    tvtvhd_url = f"https://tvtvhd.com/vivo/canales.php?stream={channel_slug}"

    try:
        async with httpx.AsyncClient(timeout=10, headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(tvtvhd_url)
            html_content = response.text

        # Buscar playbackURL en el HTML
        match = re.search(r'playbackURL\s*[=:]\s*["\']?([^"\'<>]+\.m3u8[^"\'<>]*)["\']?', html_content)
        if match:
            url = match.group(1)
            if url.startswith('http'):
                return url

        # Buscar en etiqueta source
        match = re.search(r'<source[^>]+src=["\']([^"\']+\.m3u8[^"\']*)["\']', html_content)
        if match:
            return match.group(1)

        # Buscar en data-src
        match = re.search(r'data-src=["\']?([https://][^"\'<>]+\.m3u8[^"\'<>]*)["\']?', html_content)
        if match:
            return match.group(1)

        # Último intento: buscar cualquier m3u8
        match = re.search(r'(https?://[^"\'<>\s]+\.m3u8[^"\'<>\s]*)', html_content)
        if match:
            return match.group(1)

        raise ValueError("No se encontró la URL del stream en tvtvhd.com")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extrayendo stream: {str(e)}")

@router.get("/{channel_slug}")
async def get_stream(channel_slug: str, db: Session = Depends(get_db)):
    """Obtiene la URL del stream para un canal específico"""
    try:
        # Buscar el canal en la BD para verificar que exista
        channel = get_channel_by_slug(db, channel_slug)
        if not channel:
            raise HTTPException(status_code=404, detail="Canal no encontrado")

        # Retornar URL del proxy que actúa como stream directo
        return {
            "url": f"/api/streams/proxy/{channel_slug}",
            "channel": channel_slug,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/proxy/{channel_slug}")
async def stream_proxy(channel_slug: str, db: Session = Depends(get_db)):
    """Proxy real para servir el contenido del stream sin restricciones CORS"""
    try:
        # Buscar el canal en la BD
        channel = get_channel_by_slug(db, channel_slug)
        if not channel:
            raise HTTPException(status_code=404, detail="Canal no encontrado")

        stream_url = channel.stream_url

        # Si es URL de tvtvhd.com, intentar extraer la URL real
        if "tvtvhd.com" in stream_url:
            try:
                stream_url = await get_stream_url_from_tvtvhd(channel_slug)
            except:
                pass

        # Hacer proxy de la solicitud
        async with httpx.AsyncClient(timeout=30, headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(stream_url)

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"Error obteniendo stream: {response.status_code}")

            # Retornar el contenido del m3u8 directamente
            return StreamingResponse(
                iter([response.content]),
                media_type="application/vnd.apple.mpegurl",
                headers={"Access-Control-Allow-Origin": "*"}
            )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proxy: {str(e)}")
