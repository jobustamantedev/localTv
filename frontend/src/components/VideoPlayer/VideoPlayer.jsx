import { useEffect, useRef, useState, useContext } from 'react';
import CastButton from '../CastButton/CastButton';
import { ChannelContext } from '../../context/ChannelContext';
import styles from './VideoPlayer.module.css';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function VideoPlayer() {
  const { currentChannel: channel } = useContext(ChannelContext);
  const playerRef = useRef(null);
  const clapprRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [streamUrl, setStreamUrl] = useState(null);

  useEffect(() => {
    if (!channel?.slug) {
      // Sin canal seleccionado
      if (clapprRef.current) {
        try {
          clapprRef.current.destroy();
        } catch (e) {
          console.error('Error destroying player:', e);
        }
        clapprRef.current = null;
      }
      // Limpiar contenido del div
      const playerDiv = document.getElementById('video-player');
      if (playerDiv) {
        playerDiv.innerHTML = '';
      }
      setError(null);
      return;
    }

    // Limpiar instancia anterior completamente
    if (clapprRef.current) {
      try {
        clapprRef.current.destroy();
      } catch (e) {
        console.error('Error destroying previous player:', e);
      }
      clapprRef.current = null;
    }

    // Limpiar el contenido del div antes de crear nuevo player
    const playerDiv = document.getElementById('video-player');
    if (playerDiv) {
      playerDiv.innerHTML = '';
    }

    setLoading(true);
    setError(null);

    // Obtener la URL real del stream desde el backend
    const fetchStreamUrl = async () => {
      try {
        const response = await fetch(`${BASE_URL}/api/streams/${channel.slug}`);
        if (!response.ok) {
          throw new Error('Error obteniendo URL del stream');
        }

        const data = await response.json();
        const realStreamUrl = data.url;
        setStreamUrl(realStreamUrl);

        // Crear nueva instancia de Clappr con la URL real del m3u8
        if (window.Clappr) {
          clapprRef.current = new window.Clappr.Player({
            source: realStreamUrl,
            parentId: '#video-player',
            width: '100%',
            height: '100%',
            autoPlay: true,
            mute: false,
            hlsjsConfig: {},
          });
          setError(null);
        } else {
          console.error('Clappr no está disponible en window');
          setError('Player no disponible');
        }
      } catch (err) {
        console.error('Error cargando stream:', err);
        setError(`Error: ${err.message}`);
      } finally {
        setLoading(false);
      }
    };

    fetchStreamUrl();

    // Cleanup al desmontar o cambiar canal
    return () => {
      if (clapprRef.current) {
        try {
          clapprRef.current.destroy();
        } catch (e) {
          console.error('Error in cleanup:', e);
        }
        clapprRef.current = null;
      }
      const playerDiv = document.getElementById('video-player');
      if (playerDiv) {
        playerDiv.innerHTML = '';
      }
    };
  }, [channel?.slug]); // Solo re-ejecuta cuando cambia el slug del canal

  return (
    <div className={styles.playerWrapper}>
      <div id="video-player" ref={playerRef} className={styles.player} />
      {channel && streamUrl && (
        <div className={styles.controls}>
          <CastButton
            streamUrl={streamUrl}
            channelName={channel.name}
            logoUrl={channel.logo_url}
            loading={loading}
          />
        </div>
      )}
      {!channel && (
        <div className={styles.placeholder}>
          <span className={styles.placeholderIcon}>▶</span>
          <p>Selecciona un canal</p>
        </div>
      )}
      {loading && (
        <div className={styles.overlay}>
          <div className={styles.spinner} />
          <p className={styles.loadingText}>Conectando...</p>
        </div>
      )}
      {error && (
        <div className={styles.error}>
          <span className={styles.errorIcon}>⚠</span>
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}
