import re
import os
import httpx
from urllib.parse import quote, unquote, urljoin
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, StreamingResponse

router = APIRouter(prefix="/api/streams", tags=["streams"])

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://tvtvhd.com/",
}

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

async def get_stream_url(channel_slug: str) -> str:
    """Extrae la URL real del stream desde tvtvhd.com"""
    tvtvhd_url = f"https://tvtvhd.com/vivo/canales.php?stream={channel_slug}"

    try:
        async with httpx.AsyncClient(timeout=10, headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(tvtvhd_url)
            html_content = response.text

        # Buscar playbackURL en el HTML - patrón más preciso
        match = re.search(r'playbackURL\s*[=:]\s*["\']?([^"\'<>]+\.m3u8[^"\'<>]*)["\']?', html_content)
        if match:
            url = match.group(1)
            if url.startswith('http'):
                return url

        # Buscar en etiqueta source
        match = re.search(r'<source[^>]+src=["\']([^"\']+\.m3u8[^"\']*)["\']', html_content)
        if match:
            return match.group(1)

        # Buscar en data-src o atributos similares
        match = re.search(r'data-src=["\']?([https://][^"\'<>]+\.m3u8[^"\'<>]*)["\']?', html_content)
        if match:
            return match.group(1)

        # Último intento: buscar cualquier URL que contenga m3u8
        match = re.search(r'(https?://[^"\'<>\s]+\.m3u8[^"\'<>\s]*)', html_content)
        if match:
            return match.group(1)

        raise ValueError("No se encontró la URL del stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extrayendo stream: {str(e)}")

@router.get("/{channel_slug}")
async def get_stream(channel_slug: str):
    """Obtiene la URL proxy del stream para un canal específico"""
    try:
        # Verificar que el slug sea válido (intenta extraer la URL real)
        _ = await get_stream_url(channel_slug)

        # Devolver la URL del proxy en lugar de la URL real
        return {
            "url": f"{BACKEND_URL}/api/streams/proxy/{channel_slug}",
            "channel": channel_slug,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/proxy/{channel_slug}")
async def stream_proxy(channel_slug: str):
    """Proxy del m3u8: descarga y reescribe URLs de segmentos para pasar por el backend"""
    try:
        # Obtener la URL real del m3u8
        m3u8_url = await get_stream_url(channel_slug)

        # Descargar el contenido del m3u8
        async with httpx.AsyncClient(timeout=10, headers=HEADERS, follow_redirects=True) as client:
            response = await client.get(m3u8_url)
            m3u8_content = response.text

        # Calcular la URL base del m3u8 para resolver URLs relativas
        # Ej: https://qzv4jmsc.fubohd.com/azteca7/mono.m3u8 → https://qzv4jmsc.fubohd.com/azteca7/
        m3u8_base_url = '/'.join(m3u8_url.split('/')[:-1]) + '/'

        # Reescribir las URLs de segmentos para que pasen por el proxy del backend
        lines = m3u8_content.split('\n')
        rewritten_lines = []

        for line in lines:
            stripped = line.strip()

            # Detectar si es una URL de segmento (absoluta o relativa)
            is_segment = '.ts' in line or '.m4s' in line or '.mp4' in line
            is_absolute_url = line.startswith('http')
            is_relative_url = (line.startswith('/') or (not line.startswith('#') and not line.startswith('http'))) and is_segment

            if is_absolute_url and is_segment:
                # URL absoluta: reescribir directamente
                encoded_url = quote(line, safe='')
                proxy_url = f"{BACKEND_URL}/api/streams/segment?url={encoded_url}"
                rewritten_lines.append(proxy_url)
            elif is_relative_url:
                # URL relativa: resolver a absoluta primero, luego reescribir
                absolute_url = urljoin(m3u8_base_url, line)
                encoded_url = quote(absolute_url, safe='')
                proxy_url = f"{BACKEND_URL}/api/streams/segment?url={encoded_url}"
                rewritten_lines.append(proxy_url)
            else:
                # Mantener la línea original (comentarios, líneas de configuración, etc.)
                rewritten_lines.append(line)

        rewritten_m3u8 = '\n'.join(rewritten_lines)

        # Devolver el m3u8 reescrito
        return Response(content=rewritten_m3u8, media_type="application/vnd.apple.mpegurl")

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proxy m3u8: {str(e)}")

@router.get("/segment")
async def stream_segment(url: str):
    """Proxy de segmentos HLS: descarga el segmento y hace streaming al cliente"""
    try:
        # Decodear la URL del segmento
        segment_url = unquote(url)

        # Descargar el segmento con headers spoofed
        async with httpx.AsyncClient(timeout=30, headers=HEADERS, follow_redirects=True) as client:
            async with client.stream("GET", segment_url) as response:
                if response.status_code != 200:
                    raise HTTPException(status_code=response.status_code, detail="Error descargando segmento")

                # Hacer streaming del contenido al cliente
                return StreamingResponse(
                    response.aiter_bytes(),
                    media_type="video/MP2T",
                    headers={"Cache-Control": "public, max-age=3600"}
                )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en proxy de segmento: {str(e)}")
