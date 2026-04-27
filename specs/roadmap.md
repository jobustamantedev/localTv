# bustaTv — Roadmap de Desarrollo

## Resumen de Fases

| Fase | Nombre | Estimación | Tareas | Estado |
|---|---|---|---|---|
| 1 | Setup del proyecto | 1-2h | 13 | Pendiente |
| 2 | Backend (FastAPI + SQLite) | 3-4h | 15 | Pendiente |
| 3 | Frontend (React + Clappr + UI) | 4-6h | 18 | Pendiente |
| 4 | Panel de Administración | 2-3h | 12 | Pendiente |
| 5 | Integración y pruebas | 2-3h | 10 | Pendiente |

**Total estimado: 12-18 horas de desarrollo**

---

## Fase 1: Setup del Proyecto
**Estimación: 1-2 horas**

### Tareas Backend

- [ ] **1.1.1** Crear entorno virtual Python
  - `cd backend && python -m venv venv`
  - Activar: `source venv/bin/activate` (Windows: `venv\Scripts\activate`)
  - Done: `python --version` muestra 3.11+

- [ ] **1.1.2** Crear `requirements.txt`
  - Copiar contenido de `specs/backend.md`
  - Done: archivo existe en `backend/requirements.txt`

- [ ] **1.1.3** Instalar dependencias
  - `pip install -r requirements.txt`
  - Done: pip list muestra fastapi, uvicorn, sqlalchemy, etc.

- [ ] **1.1.4** Crear estructura de carpetas `app/`
  - `mkdir -p app/{models,schemas,routers,crud}`
  - `touch app/__init__.py`
  - Done: estructura existe

- [ ] **1.1.5** Crear `app/config.py`
  - Copiar de `specs/backend.md`
  - Done: archivo existe y compila sin errores

- [ ] **1.1.6** Crear `app/database.py`
  - Copiar de `specs/backend.md`
  - Done: archivo existe

- [ ] **1.1.7** Crear `main.py` (entry point)
  - Copiar de `specs/backend.md`
  - Done: `uvicorn main:app --reload` arranca sin errores

- [ ] **1.1.8** Crear `backend/.env`
  ```
  DATABASE_URL=sqlite:///./bustaTv.db
  SECRET_API_KEY=bustatv-dev-secret-key-changeme
  ```
  - Done: archivo existe

- [ ] **1.1.9** Verificar conexión a BD
  - `uvicorn main:app --reload`
  - Acceder a `http://localhost:8000/health`
  - Done: responde `{"status": "ok"}`

### Tareas Frontend

- [ ] **1.2.1** Crear proyecto Vite+React
  - `cd frontend && npm create vite@latest . -- --template react`
  - Responder preguntas del prompt
  - Done: estructura de Vite existe

- [ ] **1.2.2** Instalar dependencias frontend
  - `npm install react-router-dom`
  - Done: `npm list` muestra react-router-dom

- [ ] **1.2.3** Crear estructura de carpetas
  - Crear: `src/{components,pages,context,hooks,services,utils}`
  - Done: carpetas existen

- [ ] **1.2.4** Configurar `vite.config.js`
  - Copiar de `specs/frontend.md` (con proxy a localhost:8000)
  - Done: archivo contiene `proxy: {'/api': {...}}`

- [ ] **1.2.5** Crear `.env.development`
  - `VITE_API_URL=http://localhost:8000`
  - Done: archivo existe

- [ ] **1.2.6** Agregar Clappr CDN en `index.html`
  - Añadir: `<script src="https://cdn.jsdelivr.net/npm/clappr@latest/dist/clappr.min.js"></script>`
  - Done: script está en `<head>`

- [ ] **1.2.7** Crear `src/index.css` con variables ESPN
  - Copiar de `specs/frontend.md`
  - Done: archivo contiene `--bg-primary`, `--bg-navbar`, `--accent`, etc.

- [ ] **1.2.8** Verificar dev server de Vite
  - `npm run dev`
  - Done: accesible en `http://localhost:5173` sin errores

### Tareas de Configuración General

- [ ] **1.3.1** Verificar `.gitignore`
  - Confirmar que excluye: `*.db`, `venv/`, `node_modules/`, `.env`, `dist/`
  - Done: `.gitignore` en raíz cubre backend y frontend

- [ ] **1.3.2** Primer commit
  - `git add .`
  - `git commit -m "Fase 1 completada: setup de proyecto"`
  - `git push`
  - Done: commit en main de GitHub

### Criterios de "Done" — Fase 1
- ✅ Backend arranca en `localhost:8000` sin errores
- ✅ `GET /health` responde `{"status": "ok"}`
- ✅ Swagger UI disponible en `/docs`
- ✅ Frontend arranca en `localhost:5173` sin errores
- ✅ Ambos servicios pueden correr simultáneamente
- ✅ No hay conflictos de puertos

---

## Fase 2: Backend (FastAPI + SQLite + Endpoints)
**Estimación: 3-4 horas**

### Tareas de Modelos y Schemas

- [ ] **2.1.1** Crear `app/models/category.py`
  - Copiar modelo Category de `specs/backend.md`
  - Done: archivo existe y sqlalchemy.orm.relationship funciona

- [ ] **2.1.2** Crear `app/models/channel.py`
  - Copiar modelo Channel de `specs/backend.md`
  - Done: archivo existe con todas las columnas

- [ ] **2.1.3** Crear `app/models/__init__.py`
  - Importar ambos modelos: `from . import category, channel`
  - Done: archivo existe y sin errores de importación

- [ ] **2.1.4** Crear `app/schemas/category.py`
  - Copiar schemas Pydantic de `specs/backend.md`
  - Done: CategoryCreate y CategoryRead existen

- [ ] **2.1.5** Crear `app/schemas/channel.py`
  - Copiar schemas de `specs/backend.md`
  - Done: ChannelCreate, ChannelRead, ChannelUpdate existen

### Tareas CRUD Layer

- [ ] **2.2.1** Crear `app/crud/categories.py`
  - Implementar: get_categories(), get_category_by_slug(), create_category()
  - Done: funciones existen y sin errores de sintaxis

- [ ] **2.2.2** Crear `app/crud/channels.py`
  - Implementar: get_channels(), get_channel(), get_channel_by_slug(), create_channel(), update_channel(), delete_channel()
  - Done: todas las funciones existen

- [ ] **2.2.3** Crear `app/crud/__init__.py`
  - Importar ambos módulos CRUD
  - Done: archivo existe

### Tareas Routers y Autenticación

- [ ] **2.3.1** Crear `app/auth.py`
  - Implementar `require_api_key()` con FastAPI Security
  - Done: función existe y valida header X-API-Key

- [ ] **2.3.2** Crear `app/routers/categories.py`
  - Implementar: `GET /api/categories`
  - Done: endpoint definido y retorna list[CategoryRead]

- [ ] **2.3.3** Crear `app/routers/channels.py`
  - Implementar 7 endpoints:
    - GET /api/channels (público)
    - GET /api/channels/{id} (público)
    - GET /api/channels/slug/{slug} (público)
    - POST /api/channels (admin)
    - PUT /api/channels/{id} (admin)
    - DELETE /api/channels/{id} (admin)
  - Done: todos los endpoints están definidos

- [ ] **2.3.4** Crear `app/routers/__init__.py`
  - Importar ambos routers
  - Done: archivo existe

- [ ] **2.3.5** Actualizar `main.py`
  - Añadir: `app.include_router(channels.router)` y `app.include_router(categories.router)`
  - Configurar CORS para localhost:5173
  - Done: routers están registrados y CORS configurado

### Tareas de Base de Datos y Seed

- [ ] **2.4.1** Crear tablas automáticamente
  - Ejecutar `uvicorn main:app --reload`
  - Confirmar que `bustaTv.db` se crea
  - Done: archivo DB existe

- [ ] **2.4.2** Crear `backend/scripts/seed.py`
  - Copiar script de `specs/database.md`
  - Done: archivo existe con 10 canales y 2 categorías

- [ ] **2.4.3** Ejecutar seed
  - `cd backend && python scripts/seed.py`
  - Done: output muestra "✅ Seed completado!" con conteo de categorías y canales

- [ ] **2.4.4** Verificar datos en BD
  - Abrir `bustaTv.db` con sqlite3 CLI o DB Browser
  - Confirmar: 10 canales + 2 categorías existen
  - Done: datos visibles en DB

### Tareas de Testing

- [ ] **2.5.1** Probar endpoints en Swagger UI
  - Abrir `http://localhost:8000/docs`
  - Probar: GET /api/channels → retorna 10 canales
  - Done: respuesta 200 con JSON válido

- [ ] **2.5.2** Probar autenticación admin
  - POST /api/channels SIN API key → error 401
  - POST /api/channels CON API key válida → crear canal nuevo
  - Confirmar nuevo canal en BD
  - Done: autenticación funciona

- [ ] **2.5.3** Probar actualización de canal
  - PUT /api/channels/{id} con datos → canal actualizado
  - Done: cambios reflejados en BD

- [ ] **2.5.4** Probar eliminación de canal
  - DELETE /api/channels/{id} → canal deletedo
  - Done: canal ya no aparece en GET /api/channels

### Criterios de "Done" — Fase 2
- ✅ Todos los 7 endpoints responden correctamente en Swagger UI
- ✅ BD contiene 10 canales + 2 categorías
- ✅ Endpoints GET son públicos (sin autenticación)
- ✅ Endpoints POST/PUT/DELETE requieren API key válida
- ✅ CORS permite peticiones desde localhost:5173
- ✅ Manejo de errores: 404 para recursos no encontrados, 401 para auth fallida
- ✅ Sin errores en logs de uvicorn

---

## Fase 3: Frontend (React + Clappr + UI ESPN)
**Estimación: 4-6 horas**

### Tareas de Infraestructura React

- [ ] **3.1.1** Crear `src/App.jsx`
  - Implementar Router, ChannelProvider, Navbar
  - Definir rutas: `/`, `/admin`, `/admin/dashboard`
  - Done: componente sin errores de React

- [ ] **3.1.2** Crear `src/context/ChannelContext.jsx`
  - Implementar: ChannelContext, ChannelProvider
  - Estado: channels[], categories[], currentChannel, activeCategory, loading, error
  - Done: contexto funciona y proporciona datos

- [ ] **3.1.3** Crear `src/services/api.js`
  - Implementar funciones: getChannels(), getCategories(), createChannel(), updateChannel(), deleteChannel()
  - Done: archivo existe y fetch requests van a localhost:8000/api

- [ ] **3.1.4** Crear `src/hooks/useChannels.js`
  - Hook personalizado para fetch de canales (encapsula estado, loading, error)
  - Done: hook funciona y se puede usar en componentes

- [ ] **3.1.5** Crear `src/hooks/useCategories.js`
  - Hook personalizado para fetch de categorías
  - Done: hook funciona

- [ ] **3.1.6** Crear `src/main.jsx`
  - Importar `<App />` y renderizar en `#root`
  - Done: app monta sin errores

### Tareas de Componentes Navbar

- [ ] **3.2.1** Crear `src/components/Navbar/Navbar.jsx`
  - Mostrar: logo "bustaTv", links (Inicio, Canales, Admin)
  - Styling: fondo rojo ESPN (#CC0000)
  - Done: componente renderiza sin errores

- [ ] **3.2.2** Crear `src/components/Navbar/Navbar.module.css`
  - Navbar rojo, padding, flexbox layout
  - Done: archivo existe con estilos

### Tareas de Componentes Video Player

- [ ] **3.3.1** Crear `src/components/VideoPlayer/VideoPlayer.jsx`
  - Implementar Clappr con useRef + useEffect (patrón crítico de specs/frontend.md)
  - Manejo: cambiar canal, destruir instancia anterior, crear nueva
  - Done: player monta y cambia de canal sin memory leaks

- [ ] **3.3.2** Crear `src/components/VideoPlayer/VideoPlayer.module.css`
  - Estilos: aspect ratio 16:9, 100% ancho, fondo negro
  - Done: archivo existe

- [ ] **3.3.3** Crear `src/components/ChannelInfo/ChannelInfo.jsx`
  - Mostrar: nombre del canal, descripción (ej. "LaLiga · Champions")
  - Done: componente muestra información del canal actual

### Tareas de Componentes Sidebar de Canales

- [ ] **3.4.1** Crear `src/components/ChannelSidebar/ChannelSidebar.jsx`
  - Lista vertical de canales filtrados
  - Cada canal clicable para seleccionar
  - Done: lista renderiza y es interactiva

- [ ] **3.4.2** Crear `src/components/ChannelCard/ChannelCard.jsx`
  - Tarjeta individual: nombre, indicador EN VIVO (rojo), logo (si existe)
  - Muestra 🔴 si activo, ⚪ si inactivo
  - Done: tarjetas renderizen correctamente

- [ ] **3.4.3** Crear CSS para ChannelSidebar y ChannelCard
  - Sidebar: lista vertical, scroll
  - Card: hover, selected state, border rojo en selección
  - Done: archivos .module.css existen

### Tareas de Componentes Filtros

- [ ] **3.5.1** Crear `src/components/CategoryFilter/CategoryFilter.jsx`
  - Tabs horizontales: "Todos", "Deportes", "Reality", etc.
  - Al clic, actualiza activeCategory en context
  - Done: filtros funcionan y modifican la lista

- [ ] **3.5.2** Crear CSS para CategoryFilter
  - Tabs con border-bottom cuando activo
  - Done: archivo .module.css existe

### Tareas de Componentes de Soporte

- [ ] **3.6.1** Crear `src/components/LoadingSpinner/LoadingSpinner.jsx`
  - Mostrar spinner/loader mientras carga la API
  - Done: componente renderiza durante loading

- [ ] **3.6.2** Crear `src/pages/Home.jsx`
  - Layout ESPN: player (70%) + sidebar (30%)
  - Incluir: VideoPlayer, ChannelInfo, CategoryFilter, ChannelSidebar
  - Manejo: loading state, error state
  - Done: Home renderiza sin errores

### Tareas de Responsive Design

- [ ] **3.7.1** Aplicar CSS responsivo
  - Desktop (1024px+): 2 columnas (70/30)
  - Mobile (<1024px): 1 columna (player arriba, canales abajo)
  - Media queries o CSS Grid
  - Done: layout es responsivo en Chrome DevTools (device emulation)

- [ ] **3.7.2** Probar en diferentes resoluciones
  - 1920x1080 (desktop grande)
  - 1024x768 (tablet)
  - 375x667 (mobile)
  - Done: layout se adapta correctamente

### Tareas de Dark Theme

- [ ] **3.8.1** Verificar variables CSS ESPN
  - `src/index.css` contiene: --bg-primary, --bg-navbar, --accent, --text-primary, etc.
  - Done: variables definidas y usadas en componentes

- [ ] **3.8.2** Aplicar tema a todos los componentes
  - Todos los .module.css usan variables CSS
  - Done: app es consistentemente dark theme rojo/negro

### Criterios de "Done" — Fase 3
- ✅ Home carga y muestra lista de 10 canales
- ✅ Al hacer clic en un canal, Clappr intenta reproducir
- ✅ Filtros por categoría funcionan (mostrando/ocultando canales)
- ✅ Dark theme ESPN aplicado consistentemente
- ✅ Layout responsive (desktop 70/30, mobile 100% vertical)
- ✅ No hay errores en console del browser (excepto CORS si tvtvhd.com bloqueado)
- ✅ No hay memory leaks al cambiar de canal (DevTools > Memory)

---

## Fase 4: Panel de Administración
**Estimación: 2-3 horas**

### Tareas de Login Admin

- [ ] **4.1.1** Crear `src/pages/Admin/AdminLogin.jsx`
  - Formulario: campo "API Key", botón "Ingresar"
  - Al submit: guardar API key en localStorage
  - Done: formulario renderiza

- [ ] **4.1.2** Validar API key
  - Al ingresar key: hacer fetch a GET /api/channels con header X-API-Key
  - Si 200: redirigir a /admin/dashboard y guardar key
  - Si 401: mostrar error "API Key inválida"
  - Done: validación funciona

### Tareas de Dashboard Admin

- [ ] **4.2.1** Crear `src/pages/Admin/AdminDashboard.jsx`
  - Tabla con columnas: id, nombre, slug, categoría, activo, acciones
  - Filas: uno por canal
  - Done: tabla renderiza con datos de la API

- [ ] **4.2.2** Implementar botón "Toggle" activo/inactivo
  - Al clic en toggle: PUT /api/channels/{id} con is_active = !is_active
  - Actualizar tabla sin refrescar página
  - Done: toggle funciona e inmediatamente refleja cambios

- [ ] **4.2.3** Implementar botón "Editar"
  - Al clic: abrir modal o ir a página de edición con `ChannelForm`
  - Pre-cargar datos del canal
  - Done: form carga datos del canal

- [ ] **4.2.4** Implementar botón "Eliminar"
  - Al clic: mostrar confirmación (confirm dialog)
  - Si confirmado: DELETE /api/channels/{id}
  - Remover fila de la tabla
  - Done: eliminación funciona

- [ ] **4.2.5** Implementar botón "Agregar canal"
  - Al clic: abrir `ChannelForm` vacío
  - Done: formulario se abre

### Tareas de Formulario de Canal

- [ ] **4.3.1** Crear `src/pages/Admin/ChannelForm.jsx`
  - Campos: nombre, slug (auto-generado), stream_url, logo_url, categoría (select), is_active
  - Validación básica: campos requeridos
  - Done: formulario renderiza

- [ ] **4.3.2** Implementar submit (crear)
  - POST /api/channels con datos del formulario + API key
  - Mostrar mensaje de éxito/error
  - Redirigir a /admin/dashboard
  - Done: crear canal funciona

- [ ] **4.3.3** Implementar submit (actualizar)
  - PUT /api/channels/{id} con datos del formulario + API key
  - Mostrar mensaje de éxito/error
  - Redirigir a /admin/dashboard
  - Done: actualizar canal funciona

- [ ] **4.3.4** Auto-generar slug desde nombre
  - Al cambiar nombre: slug = nombre.toLowerCase().replace(/\s+/g, '-')
  - Done: slug se actualiza en tiempo real

### Tareas de Protección de Rutas

- [ ] **4.4.1** Crear `src/components/ProtectedRoute.jsx`
  - Componente que verifica si API key existe en localStorage
  - Si no existe: redirigir a /admin
  - Si existe: renderizar componente
  - Done: componente funciona

- [ ] **4.4.2** Proteger rutas admin
  - `/admin/dashboard` dentro de `<ProtectedRoute>`
  - Done: acceso bloqueado sin API key

### Criterios de "Done" — Fase 4
- ✅ Login con API key correcta da acceso al dashboard
- ✅ Login con API key incorrecta muestra error y bloquea acceso
- ✅ Dashboard muestra tabla de canales
- ✅ Toggle on/off funciona (is_active cambio)
- ✅ Crear canal funciona y aparece en tabla
- ✅ Editar canal funciona
- ✅ Eliminar canal funciona (con confirmación)
- ✅ Rutas admin protegidas por localStorage

---

## Fase 5: Integración y Pruebas
**Estimación: 2-3 horas**

### Tareas de Testing Manual E2E

- [ ] **5.1.1** Flujo completo: usuario navega
  - Backend arranca en localhost:8000
  - Frontend arranca en localhost:5173
  - Usuario abre Home
  - Ver lista de 10 canales
  - Clic en ESPN → Clappr intenta reproducir
  - Done: todo funciona end-to-end

- [ ] **5.1.2** Probar en múltiples navegadores
  - Chrome
  - Firefox
  - Safari (si es posible)
  - Done: app funciona en todos

- [ ] **5.1.3** Probar en mobile
  - iPhone (iOS Safari)
  - Android (Chrome)
  - Emulador DevTools
  - Done: layout responsive funciona

- [ ] **5.1.4** Flujo admin: login y CRUD
  - Ingresar API key en /admin
  - Crear canal nuevo
  - Editar canal existente
  - Toggle activo/inactivo
  - Eliminar canal
  - Verificar en Home que cambios se reflejan
  - Done: admin panel fully functional

### Tareas de Manejo de Errores

- [ ] **5.2.1** Backend caído
  - Matar uvicorn
  - Intentar cargar Home
  - Mostrar mensaje amigable: "No se puede conectar al servidor"
  - Done: error message visible

- [ ] **5.2.2** Stream no carga
  - tvtvhd.com no disponible o URL inválida
  - Clappr muestra su error nativo
  - Player no queda en estado "stuck"
  - Done: user experience es acceptable

- [ ] **5.2.3** No hay canales
  - Eliminar todos los canales via admin
  - Home muestra: "No hay canales disponibles"
  - Done: no page crash, mensaje claro

- [ ] **5.2.4** Red lenta
  - Simular slow 3G en DevTools
  - Loading spinner aparece mientras carga
  - Done: UX clara durante espera

### Tareas de Optimizaciones Básicas

- [ ] **5.3.1** Lazy loading de logos
  - Imágenes de canales cargan solo cuando necesario
  - Done: no blocking en carga inicial

- [ ] **5.3.2** Evitar re-renders innecesarios
  - ChannelCard con React.memo
  - Done: console de React no muestra renders excesivos

- [ ] **5.3.3** Memory leaks de Clappr
  - Cambiar entre canales 10 veces
  - DevTools > Memory: tomar heap snapshot antes y después
  - Memory no crece linealmente
  - Done: no memory leaks

### Tareas de Documentación y Commits

- [ ] **5.4.1** Actualizar README.md
  - Instrucciones de instalación y ejecución
  - Stack usado (React, FastAPI, etc.)
  - Cómo acceder a endpoints
  - Done: README claro y completo

- [ ] **5.4.2** Actualizar CLAUDE.md
  - Documentar el stack final decidido
  - Notas sobre la integración Clappr
  - Done: CLAUDE.md actualizado

- [ ] **5.4.3** Crear `.env.example`
  - Backend: ejemplo de `.env`
  - Frontend: ejemplo de `.env.development`
  - Done: archivos existen sin valores sensibles

- [ ] **5.4.4** Crear script de inicio `scripts/start.sh` (opcional)
  - Script que inicia backend y frontend automáticamente
  - Done: script existe y funciona

### Tareas Finales

- [ ] **5.5.1** Último commit
  - `git add .`
  - `git commit -m "Fase 5: Integración completa y documentación"`
  - `git push`
  - Done: código en main de GitHub

- [ ] **5.5.2** Verificación final
  - Clonar repo en carpeta nueva
  - Seguir instrucciones del README
  - App funciona desde cero
  - Done: proyecto está listo para usar

### Criterios de "Done" — Fase 5 (Proyecto Completo)
- ✅ El proyecto se puede clonar y ejecutar con instrucciones del README
- ✅ Un usuario puede ver todos los canales disponibles en la Home
- ✅ Al seleccionar un canal, el video carga y reproduce (dependiente de tvtvhd.com)
- ✅ Panel admin permite crear, editar, activar/desactivar, eliminar canales
- ✅ No hay errores en la consola del browser (excepto CORS si tvtvhd.com bloqueado)
- ✅ No hay errores en los logs de uvicorn/fastapi
- ✅ App funciona en desktop y mobile
- ✅ Respeta el diseño ESPN (rojo navbar, dark theme)
- ✅ README tiene instrucciones claras
- ✅ CLAUDE.md documentado

---

## Dependencias entre Fases

```
Fase 1: Setup
    │
    ├─→ Fase 2: Backend ──────┐
    │                         │
    └─→ Fase 3: Frontend ◀────┤ (pueden ir en paralelo si hay 2 devs)
                              │
                    Fase 4: Admin ◀────┘
                        │
                        ▼
                   Fase 5: Integración & Pruebas
```

**Recomendación para un solo desarrollador:** Orden secuencial 1→2→3→4→5.

Para dos desarrolladores: Una persona hace Backend (Fase 2) mientras la otra hace Frontend básico (Fase 3, sin admin), luego se unen en Fase 4.

---

## Notas Importantes

### Streams de tvtvhd.com
- Los URLs base dependen de un servicio externo
- Si tvtvhd.com cae o cambia su API, los streams dejarán de funcionar
- **Esto es normal en un proyecto educativo**
- En producción, investigar proveedores de streams legales (Twitch, YouTube Live, etc.)
- Los URLs se pueden editar via el panel admin sin cambiar código

### Clappr y React
- Clappr NO es un componente React; es una librería imperativa
- La integración con `useRef + useEffect` es crítica (ver specs/frontend.md)
- Siempre llamar `.destroy()` antes de crear instancia nueva
- Cargar via CDN en `index.html`, no via npm

### API Key
- En desarrollo: `bustatv-dev-secret-key-changeme` es suficiente
- En producción: generar clave segura, usar variables de entorno, considerar JWT

### Testing
- No hay tests automatizados en este proyecto (educativo)
- Testing manual es suficiente para esta escala
- Si crece: agregar Vitest (frontend) + pytest (backend)

---

## Checklist Final

Cuando termines todas las fases:

- [ ] Todos los endpoints funcionan en Swagger UI
- [ ] Frontend carga lista de canales desde API
- [ ] Video plays al seleccionar canal
- [ ] Panel admin CRUD funciona
- [ ] Proyecto clonado en carpeta nueva funciona
- [ ] README tiene instrucciones claras
- [ ] Código está en GitHub main branch
- [ ] Puedes ejecutar `npm run dev` (frontend) + `uvicorn main:app` (backend) simultaneamente
- [ ] Dark theme ESPN está aplicado
- [ ] No hay console errors en browser
- [ ] No hay errors en uvicorn logs

**¡Si todo esto está hecho, bustaTv Fase 1 está COMPLETO!** 🚀
