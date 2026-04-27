# bustaTv — Especificación Frontend

## Stack
- React 18
- Vite 5
- React Router DOM 6
- Clappr (via CDN)
- CSS Modules

## Estructura de Carpetas

```
frontend/
├── index.html                  # Entry point de Vite (incluye Clappr CDN)
├── vite.config.js              # Config Vite (proxy, alias)
├── package.json
├── .env.development            # VITE_API_URL=http://localhost:8000
├── public/
│   └── favicon.ico
└── src/
    ├── main.jsx                # Monta <App /> en #root
    ├── App.jsx                 # Router principal + ChannelProvider
    ├── index.css               # Variables CSS dark theme ESPN
    │
    ├── components/
    │   ├── Navbar/
    │   │   ├── Navbar.jsx
    │   │   └── Navbar.module.css
    │   ├── VideoPlayer/
    │   │   ├── VideoPlayer.jsx  # Wrapper Clappr (useRef + useEffect)
    │   │   └── VideoPlayer.module.css
    │   ├── ChannelSidebar/
    │   │   ├── ChannelSidebar.jsx  # Lista vertical de canales
    │   │   └── ChannelSidebar.module.css
    │   ├── ChannelList/
    │   │   ├── ChannelList.jsx     # Grid de canales en mobile
    │   │   └── ChannelList.module.css
    │   ├── ChannelCard/
    │   │   ├── ChannelCard.jsx     # Tarjeta individual
    │   │   └── ChannelCard.module.css
    │   ├── CategoryFilter/
    │   │   ├── CategoryFilter.jsx
    │   │   └── CategoryFilter.module.css
    │   ├── LoadingSpinner/
    │   │   └── LoadingSpinner.jsx
    │   └── ChannelInfo/
    │       ├── ChannelInfo.jsx     # Detalles del canal actual
    │       └── ChannelInfo.module.css
    │
    ├── pages/
    │   ├── Home.jsx             # Vista principal
    │   └── Admin/
    │       ├── AdminLogin.jsx
    │       ├── AdminDashboard.jsx
    │       ├── ChannelForm.jsx
    │       └── Admin.module.css
    │
    ├── context/
    │   └── ChannelContext.jsx   # Estado global
    │
    ├── hooks/
    │   ├── useChannels.js       # Fetch canales
    │   └── useCategories.js     # Fetch categorías
    │
    ├── services/
    │   └── api.js               # Funciones fetch
    │
    └── utils/
        └── constants.js         # API_BASE_URL, colores, etc
```

## Componentes Principales

### `App.jsx`
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ChannelProvider } from './context/ChannelContext';
import Navbar from './components/Navbar/Navbar';
import Home from './pages/Home';
import AdminLogin from './pages/Admin/AdminLogin';
import AdminDashboard from './pages/Admin/AdminDashboard';

export default function App() {
  return (
    <ChannelProvider>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/admin" element={<AdminLogin />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
        </Routes>
      </BrowserRouter>
    </ChannelProvider>
  );
}
```

### `VideoPlayer.jsx` — Integración Clappr con React (CRÍTICA)

```jsx
import { useEffect, useRef } from 'react';
import styles from './VideoPlayer.module.css';

export default function VideoPlayer({ channel }) {
  const playerRef = useRef(null);
  const clapprRef = useRef(null);

  useEffect(() => {
    if (!channel?.stream_url) {
      // Sin canal seleccionado
      if (clapprRef.current) {
        clapprRef.current.destroy();
        clapprRef.current = null;
      }
      return;
    }

    // Limpiar instancia anterior
    if (clapprRef.current) {
      clapprRef.current.destroy();
      clapprRef.current = null;
    }

    // Crear nueva instancia de Clappr
    // IMPORTANTE: Clappr debe estar disponible como window.Clappr
    // (cargado via <script> en index.html)
    if (window.Clappr) {
      clapprRef.current = new window.Clappr.Player({
        source: channel.stream_url,
        parentId: '#video-player',
        width: '100%',
        height: '100%',
        autoPlay: true,
        mute: false,
        poster: channel.logo_url || '',
      });
    } else {
      console.error('Clappr no está disponible en window');
    }

    // Cleanup al desmontar o cambiar canal
    return () => {
      if (clapprRef.current) {
        clapprRef.current.destroy();
        clapprRef.current = null;
      }
    };
  }, [channel?.stream_url]); // Solo re-ejecuta cuando cambia la URL del stream

  return (
    <div className={styles.playerWrapper}>
      <div id="video-player" ref={playerRef} className={styles.player} />
      {!channel && (
        <div className={styles.placeholder}>
          <p>Selecciona un canal para ver el stream</p>
        </div>
      )}
    </div>
  );
}
```

**Notas críticas:**
1. Clappr debe cargarse como script global en `index.html`:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/clappr@latest/dist/clappr.min.js"></script>
   ```
2. **NUNCA** intentar renderizar Clappr como componente React estándar
3. Siempre llamar `destroy()` antes de crear nueva instancia para evitar memory leaks
4. La opción `parentId` o `el` apunta al div contenedor

### `ChannelContext.jsx`

```jsx
import { createContext, useState, useEffect } from 'react';
import { api } from '../services/api';

export const ChannelContext = createContext();

export function ChannelProvider({ children }) {
  const [channels, setChannels] = useState([]);
  const [categories, setCategories] = useState([]);
  const [currentChannel, setCurrentChannel] = useState(null);
  const [activeCategory, setActiveCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch inicial
  useEffect(() => {
    Promise.all([
      api.getChannels(),
      api.getCategories(),
    ])
      .then(([channelsData, categoriesData]) => {
        setChannels(channelsData);
        setCategories(categoriesData);
        // Auto-seleccionar primer canal activo
        if (channelsData.length > 0) {
          setCurrentChannel(channelsData[0]);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error('Error fetching data:', err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Filtrar canales por categoría
  const filteredChannels = activeCategory === 'all'
    ? channels.filter(ch => ch.is_active)
    : channels.filter(ch => 
        ch.category_id === activeCategory && ch.is_active
      );

  const value = {
    channels,
    categories,
    currentChannel,
    setCurrentChannel,
    activeCategory,
    setActiveCategory,
    filteredChannels,
    loading,
    error,
  };

  return (
    <ChannelContext.Provider value={value}>
      {children}
    </ChannelContext.Provider>
  );
}
```

### `Home.jsx` — Layout ESPN

```jsx
import { useContext } from 'react';
import { ChannelContext } from '../context/ChannelContext';
import VideoPlayer from '../components/VideoPlayer/VideoPlayer';
import ChannelSidebar from '../components/ChannelSidebar/ChannelSidebar';
import ChannelInfo from '../components/ChannelInfo/ChannelInfo';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import CategoryFilter from '../components/CategoryFilter/CategoryFilter';
import styles from './Home.module.css';

export default function Home() {
  const { currentChannel, loading, error } = useContext(ChannelContext);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className={styles.error}>Error: {error}</div>;

  return (
    <div className={styles.home}>
      {/* Layout desktop: player 70% + sidebar 30% */}
      <div className={styles.mainContent}>
        <div className={styles.playerSection}>
          <VideoPlayer channel={currentChannel} />
          <ChannelInfo channel={currentChannel} />
        </div>
        <aside className={styles.sidebar}>
          <CategoryFilter />
          <ChannelSidebar />
        </aside>
      </div>

      {/* Mobile: mostrar ChannelList debajo */}
      <div className={styles.mobileList}>
        <ChannelList />
      </div>
    </div>
  );
}
```

### `ChannelSidebar.jsx` — Lista Vertical de Canales

```jsx
import { useContext } from 'react';
import { ChannelContext } from '../context/ChannelContext';
import ChannelCard from './ChannelCard/ChannelCard';
import styles from './ChannelSidebar.module.css';

export default function ChannelSidebar() {
  const { filteredChannels, currentChannel, setCurrentChannel } = useContext(ChannelContext);

  return (
    <div className={styles.sidebar}>
      <h3 className={styles.title}>Canales</h3>
      <div className={styles.list}>
        {filteredChannels.map((channel) => (
          <ChannelCard
            key={channel.id}
            channel={channel}
            isSelected={currentChannel?.id === channel.id}
            onSelect={() => setCurrentChannel(channel)}
          />
        ))}
      </div>
    </div>
  );
}
```

**CSS (ChannelSidebar.module.css):**
```css
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-secondary);
  height: 100%;
  overflow-y: auto;
}

.title {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
```

### `ChannelCard.jsx` — Tarjeta Individual

```jsx
import styles from './ChannelCard.module.css';

export default function ChannelCard({ channel, isSelected, onSelect }) {
  return (
    <button
      className={`${styles.card} ${isSelected ? styles.selected : ''}`}
      onClick={onSelect}
      aria-pressed={isSelected}
    >
      <div className={styles.content}>
        <div className={styles.liveIndicator}>
          {channel.is_active ? (
            <span className={styles.liveBadge}>🔴 EN VIVO</span>
          ) : (
            <span className={styles.offlineBadge}>⚪ Offline</span>
          )}
        </div>
        <div className={styles.name}>{channel.name}</div>
        {channel.logo_url && (
          <img src={channel.logo_url} alt={channel.name} className={styles.logo} />
        )}
      </div>
    </button>
  );
}
```

**CSS (ChannelCard.module.css):**
```css
.card {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: var(--bg-card);
  border: 2px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-primary);
  font-family: inherit;
  font-size: 0.9rem;
}

.card:hover {
  background: var(--bg-card-hover);
  border-color: var(--accent);
}

.card.selected {
  border-color: var(--accent);
  background: var(--bg-card-hover);
}

.content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
}

.liveIndicator {
  font-size: 0.75rem;
  font-weight: bold;
}

.liveBadge {
  color: #CC0000;
  animation: pulse 2s infinite;
}

.offlineBadge {
  color: #606060;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.logo {
  width: 24px;
  height: 24px;
  object-fit: contain;
  margin-left: auto;
}

.name {
  flex: 1;
  text-align: left;
  font-weight: 500;
}
```

### `CategoryFilter.jsx`

```jsx
import { useContext } from 'react';
import { ChannelContext } from '../context/ChannelContext';
import styles from './CategoryFilter.module.css';

export default function CategoryFilter() {
  const { categories, activeCategory, setActiveCategory } = useContext(ChannelContext);

  return (
    <div className={styles.filter}>
      <button
        className={`${styles.btn} ${activeCategory === 'all' ? styles.active : ''}`}
        onClick={() => setActiveCategory('all')}
      >
        Todos
      </button>
      {categories.map((cat) => (
        <button
          key={cat.id}
          className={`${styles.btn} ${activeCategory === cat.id ? styles.active : ''}`}
          onClick={() => setActiveCategory(cat.id)}
        >
          {cat.name}
        </button>
      ))}
    </div>
  );
}
```

**CSS (CategoryFilter.module.css):**
```css
.filter {
  display: flex;
  gap: 0.5rem;
  padding: 0 1rem;
  border-bottom: 1px solid var(--border);
  overflow-x: auto;
}

.btn {
  padding: 0.5rem 1rem;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.btn:hover {
  color: var(--text-primary);
}

.btn.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}
```

### `Navbar.jsx`

```jsx
import { Link } from 'react-router-dom';
import styles from './Navbar.module.css';

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <Link to="/" className={styles.logo}>
          bustaTv
        </Link>
        <div className={styles.menu}>
          <Link to="/" className={styles.link}>Inicio</Link>
          <Link to="/" className={styles.link}>Canales</Link>
          <Link to="/admin" className={styles.link}>Admin</Link>
        </div>
      </div>
    </nav>
  );
}
```

**CSS (Navbar.module.css):**
```css
.navbar {
  background: var(--bg-navbar);
  padding: 1rem 0;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #FFFFFF;
  text-decoration: none;
  letter-spacing: 1px;
}

.menu {
  display: flex;
  gap: 2rem;
}

.link {
  color: #FFFFFF;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.link:hover {
  opacity: 0.8;
}
```

## Paleta de Colores (ESPN-style)

```css
:root {
  /* Fondos */
  --bg-primary: #0a0a0a;       /* fondo general */
  --bg-secondary: #1a1a1a;     /* cards y sidebar */
  --bg-card: #1a1a1a;          /* tarjetas de canal */
  --bg-card-hover: #252525;    /* hover en tarjeta */

  /* Navbar */
  --bg-navbar: #CC0000;        /* rojo ESPN */

  /* Texto */
  --text-primary: #FFFFFF;
  --text-secondary: #A0A0A0;
  --text-muted: #606060;

  /* Acentos */
  --accent: #CC0000;           /* botones principales, EN VIVO */
  --accent-hover: #990000;     /* hover en botones */

  /* Bordes */
  --border: #2a2a2a;

  /* Player */
  --player-bg: #000000;
}
```

## Layout Principal (Desktop vs Mobile)

### Desktop (1024px+)
```
┌────────────────────────────────────────────────────┐
│  NAVBAR (rojo ESPN)                                │
├──────────────────────┬────────────────────────────┤
│                      │ [CategoryFilter]            │
│   VIDEO PLAYER       │ ┌──────────────────────┐   │
│   (70% ancho)        │ │ 🔴 ESPN              │   │
│   Aspect ratio 16:9  │ │ 🔴 ESPN 2            │   │
│                      │ │ 🔴 DSports           │   │
├──────────────────────┤ │ 🔴 DSports+          │   │
│ Channel Info         │ │ ⚪ DSports 2         │   │
│ "ESPN EN VIVO"       │ └──────────────────────┘   │
│ LaLiga · Champions   │ SIDEBAR (30% ancho)        │
└──────────────────────┴────────────────────────────┘
```

### Mobile (< 1024px)
```
┌──────────────────────────────┐
│  NAVBAR (rojo ESPN)          │
├──────────────────────────────┤
│  VIDEO PLAYER                │
│  (100% ancho, 16:9)          │
├──────────────────────────────┤
│  Channel Info                │
│  "ESPN EN VIVO"              │
├──────────────────────────────┤
│ [CategoryFilter] (scroll h.) │
├──────────────────────────────┤
│ Canales (scroll vertical):   │
│ □ ESPN   □ ESPN2  □ DSP+     │
│ □ ESPN3  □ DSP    □ DSP2     │
└──────────────────────────────┘
```

## Dependencias (`package.json`)

```json
{
  "name": "bustatv-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.26.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.0",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.0",
    "vite": "^5.4.0"
  }
}
```

**Nota:** Clappr se carga via CDN en `index.html`, no via npm.

## `vite.config.js`

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

El proxy de Vite redirige `/api/*` al backend, evitando CORS issues en desarrollo.

## `index.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>bustaTv | Streaming Deportivo en Vivo</title>

    <!-- Clappr Player (via CDN) -->
    <script src="https://cdn.jsdelivr.net/npm/clappr@latest/dist/clappr.min.js"></script>

    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

## `services/api.js`

```javascript
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  // Canales (públicos)
  getChannels: async () => {
    const res = await fetch(`${BASE_URL}/api/channels`);
    if (!res.ok) throw new Error('Error fetching channels');
    return res.json();
  },

  getChannel: async (id) => {
    const res = await fetch(`${BASE_URL}/api/channels/${id}`);
    if (!res.ok) throw new Error('Error fetching channel');
    return res.json();
  },

  // Categorías (públicas)
  getCategories: async () => {
    const res = await fetch(`${BASE_URL}/api/categories`);
    if (!res.ok) throw new Error('Error fetching categories');
    return res.json();
  },

  // Admin (requiere API key)
  createChannel: async (data, apiKey) => {
    const res = await fetch(`${BASE_URL}/api/channels`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Error creating channel');
    return res.json();
  },

  updateChannel: async (id, data, apiKey) => {
    const res = await fetch(`${BASE_URL}/api/channels/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey,
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Error updating channel');
    return res.json();
  },

  deleteChannel: async (id, apiKey) => {
    const res = await fetch(`${BASE_URL}/api/channels/${id}`, {
      method: 'DELETE',
      headers: { 'X-API-Key': apiKey },
    });
    if (!res.ok) throw new Error('Error deleting channel');
  },
};
```

## Notas Importantes

### Integración Clappr con React
1. **Clappr NO es un componente React.** Es una API imperativa que manipula el DOM directamente.
2. Siempre usar `useRef` para el contenedor del player.
3. Siempre llamar `destroy()` en el cleanup para evitar memory leaks.
4. Cargar Clappr via **CDN en index.html**, no npm. Esto evita conflictos con Vite's ESM.
5. Acceder via `window.Clappr.Player`.

### Dark Theme ESPN
- Colores deliberadamente oscuros (fondo `#0a0a0a`) para contrastar con el video
- Rojo ESPN (`#CC0000`) solo en navbar y elementos highlight (EN VIVO)
- Sin gradientes complicados: simplicidad y claridad

### Responsive Design
- Breakpoint mobile: 768px
- Desktop: 2-columnas (player + sidebar)
- Mobile: 1-columna (player + lista horizontal o vertical)
- No usar Media Queries complicadas: CSS Grid + Flex son suficientes
