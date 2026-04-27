# bustaTv — Arquitectura General

## Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USUARIO (Browser)                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTP / HLS
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND — React + Vite                           │
│                    localhost:5173 (ESPN-style)                       │
│                                                                     │
│   ┌──────────────┐         ┌──────────────────────────────┐        │
│   │ Navbar Rojo  │         │ Layout: Player (70%) +       │        │
│   │ ESPN         │         │ Sidebar Canales (30%)        │        │
│   └──────────────┘         │                              │        │
│                            │ [VideoPlayer]  [ChannelList] │        │
│                            │  (Clappr)      ┌──────────┐  │        │
│                            │                │ ESPN  🔴 │  │        │
│                            │                │ ESPN2 🔴 │  │        │
│                            │                │ DSP+  🔴 │  │        │
│                            │                └──────────┘  │        │
│                            └──────────────────────────────┘        │
│                                  ▲                                  │
│                          React Context Store                       │
│                   (currentChannel, channels[], etc)                │
│                                                                     │
└──────────────────────────┬──────────────────────────────────────────┘
                           │ REST API (fetch / axios)
                           │ proxy: /api → localhost:8000
                           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND — FastAPI (Python)                        │
│                    localhost:8000                                    │
│                                                                     │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐        │
│   │ GET /api/    │  │ GET /api/    │  │ POST/PUT/DELETE  │        │
│   │ channels     │  │ categories   │  │ /api/channels    │        │
│   │ (públicos)   │  │ (públicos)   │  │ (requieren key)  │        │
│   └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘        │
│          │                 │                    │                  │
│   ┌──────▼─────────────────▼────────────────────▼──────────┐      │
│   │              SQLAlchemy ORM Layer                        │      │
│   │         (mapeo a tablas SQLite)                         │      │
│   └──────────────────────────┬──────────────────────────────┘      │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS — SQLite                           │
│                    ./backend/bustaTv.db                             │
│                                                                     │
│   ┌──────────────────────┐        ┌─────────────────────┐         │
│   │  TABLE: channels     │───────▶│ TABLE: categories   │         │
│   │  - id (PK)           │  1:N   │ - id (PK)           │         │
│   │  - name              │        │ - name              │         │
│   │  - slug              │        │ - slug              │         │
│   │  - stream_url        │        │ - icon              │         │
│   │  - logo_url          │        └─────────────────────┘         │
│   │  - is_active         │                                        │
│   │  - category_id (FK)  │                                        │
│   │  - created_at        │                                        │
│   └──────────────────────┘                                        │
└─────────────────────────────────────────────────────────────────────┘
                                 │
         stream_url apunta a:    │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│              FUENTE DE STREAMS EXTERNA (tvtvhd.com)                 │
│   https://tvtvhd.com/vivo/canales.php?stream={canal}               │
│                                                                     │
│   Clappr en el browser consume directamente esta URL               │
│   (el backend solo almacena y sirve la URL, no hace proxy)         │
└─────────────────────────────────────────────────────────────────────┘
```

## Descripción de Capas

### 1. Frontend (React + Vite — localhost:5173)
**Responsabilidad:** Toda la interfaz de usuario.
- Consume la API REST del backend para obtener la lista de canales y categorías
- Renderiza el reproductor Clappr directamente en el browser
- Mantiene el estado global de canales, categoría activa y canal seleccionado en React Context
- Diseño ESPN: navbar rojo, layout player (70%) + sidebar (30%), indicadores EN VIVO

**Tecnologías:**
- React 18 con Hooks (useState, useContext, useRef, useEffect)
- Vite como bundler (dev server proxy a /api)
- React Router DOM para navegación
- Clappr via CDN (no npm, para evitar problemas ESM)

### 2. Backend (FastAPI — localhost:8000)
**Responsabilidad:** API REST stateless.
- Servir lista de canales y categorías desde la BD
- Exponer endpoints de administración (CRUD) protegidos por API key
- Configurar CORS para permitir peticiones desde localhost:5173
- No hace proxy de video: el backend nunca toca el stream

**Endpoints públicos:**
- `GET /api/channels` — lista de canales (filtrable por categoría)
- `GET /api/channels/{id}` — detalle de un canal
- `GET /api/channels/slug/{slug}` — por slug (útil para React Router)
- `GET /api/categories` — lista de categorías

**Endpoints admin (requieren header `X-API-Key`):**
- `POST /api/channels` — crear
- `PUT /api/channels/{id}` — actualizar
- `DELETE /api/channels/{id}` — eliminar

### 3. Base de Datos (SQLite)
**Responsabilidad:** Almacén persistente local.
- Tabla `categories`: id, name, slug, icon
- Tabla `channels`: id, name, slug, stream_url, logo_url, category_id, is_active, created_at
- Relación 1:N (una categoría → muchos canales)
- Se accede exclusivamente via SQLAlchemy ORM
- Migraciones gestionadas con Alembic

**Datos iniciales (seed):**
- 2 categorías: Deportes, Reality (extensible)
- 10 canales: ESPN 1-7, DSports, DSports+, DSports 2

### 4. Streaming (Clappr + tvtvhd.com)
**Responsabilidad:** Reproducción de video.
El video nunca pasa por nuestros servidores. El flow:
1. Browser carga Clappr como script global (via CDN)
2. React renderiza un div contenedor
3. VideoPlayer.jsx instancia Clappr apuntando a `channel.stream_url`
4. Clappr consume el manifest HLS/DASH directamente desde tvtvhd.com
5. Streaming directo: usuario → tvtvhd.com

---

## Flujo de Datos: Usuario Selecciona un Canal

```
1. App React monta y hace GET /api/channels
   ▼
2. Backend consulta SQLite → retorna JSON con 10 canales
   ▼
3. React renderiza ChannelSidebar con tarjetas de cada canal
   Cada tarjeta muestra:
   - Logo del canal
   - Nombre: "ESPN"
   - Indicador: 🔴 (rojo si activo) o ⚪ (gris si inactivo)
   ▼
4. Usuario clica en "ESPN"
   - ChannelCard llama onSelectChannel(channel)
   - React Context actualiza currentChannel = channel
   ▼
5. VideoPlayer.jsx detecta cambio en currentChannel via useEffect
   - Destruye instancia anterior de Clappr (clapprInstance.destroy())
   - Crea nueva instancia: new Clappr.Player({ source: channel.stream_url })
   ▼
6. Clappr hace petición a:
   https://tvtvhd.com/vivo/canales.php?stream=espn
   ▼
7. tvtvhd.com retorna el manifest HLS/DASH
   ▼
8. Clappr inicia reproducción del stream en vivo
   Usuario ve el video en el player (Clappr UI nativa)
```

---

## Decisiones Técnicas y Justificación

| Decisión | Alternativa considerada | Justificación |
|---|---|---|
| **React + Vite** | Vanilla JS (como miralotv.com) | Escalabilidad, componentes reutilizables, Hot Module Replacement en desarrollo, gran comunidad |
| **FastAPI** | Node.js/Express | Python es el lenguaje base (Firecrawl, Playwright ya instalados), FastAPI es moderno y rápido para prototipos, excelente validación con Pydantic |
| **SQLite** | PostgreSQL / MySQL | Deployment local, cero configuración de servidor, suficiente para escala educativa. Fácil de migrar si crece |
| **Clappr** | Video.js, Plyr, JW Player | Es lo que usa miralotv.com (confirmado en análisis); soporte nativo HLS/DASH; open source; UI minimalista |
| **API Key simple** | JWT completo | Suficiente para uso local/educativo; implementación mínima; panel admin no requiere login de usuario |
| **Sin proxy de video** | Proxy via backend | Simplicidad, menor latencia, menor carga en servidor local, streaming directo más rápido |
| **React Context** | Redux, Zustand | El estado es simple (canal activo + lista de canales); no justifica overhead de dependencia externa |
| **SQLAlchemy + Alembic** | Tortoise ORM, Piccolo | Más maduro, mayor documentación, compatible con FastAPI, mejor para migraciones |
| **Diseño ESPN** | Netflix, Twitch, YouTube | Enfoque deportivo como se requiere; colores (rojo ESPN) transmiten marca; layout sidebar es intuitivo para listas de canales |

---

## Consideraciones de Escalabilidad

Si el proyecto crece (de MVP a producción):

1. **Frontend:** Migrar a TypeScript, agregar testing con Vitest/React Testing Library, lazy loading de componentes
2. **Backend:** Agregar autenticación JWT real, rate limiting, logging centralizado, tests con pytest
3. **BD:** Migrar a PostgreSQL, agregar índices, caché con Redis
4. **Video:** Implementar proxy de streams para DRM, analytics de visualización
5. **Hosting:** Vercel (frontend), Railway/AWS (backend), CloudFlare (CDN)

Por ahora, el stack actual es óptimo para desarrollo rápido y educativo.
