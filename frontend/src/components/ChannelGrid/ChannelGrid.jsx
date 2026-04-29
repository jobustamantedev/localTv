import { useContext, useRef, useEffect, useCallback } from 'react';
import { ChannelContext } from '../../context/ChannelContext';
import styles from './ChannelGrid.module.css';

export default function ChannelGrid() {
  const {
    channels, currentChannel, setCurrentChannel,
    hasMore, loadMore, loadingMore, totalCount, loading,
  } = useContext(ChannelContext);

  const sentinelRef = useRef(null);

  const handleIntersect = useCallback(entries => {
    if (entries[0].isIntersecting && hasMore && !loadingMore) loadMore();
  }, [hasMore, loadingMore, loadMore]);

  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(handleIntersect, { threshold: 0.1 });
    observer.observe(el);
    return () => observer.disconnect();
  }, [handleIntersect]);

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <span className={styles.sectionTitle}>// EN VIVO AHORA</span>
        <span className={styles.count}>{totalCount.toLocaleString()} CANALES</span>
      </div>

      {loading ? (
        <div className={styles.empty}>Cargando canales...</div>
      ) : !channels.length ? (
        <div className={styles.empty}>Sin resultados</div>
      ) : (
        <div className={styles.grid}>
          {channels.map((channel, index) => {
            const num = String(index + 1).padStart(2, '0');
            const isActive = currentChannel?.id === channel.id;
            return (
              <button
                key={channel.id}
                className={`${styles.card} ${isActive ? styles.active : ''}`}
                onClick={() => setCurrentChannel(channel)}
                title={channel.name}
              >
                <div className={styles.cardTop}>
                  <span className={styles.chNum}>CH {num}</span>
                  <span className={styles.liveBadge}>LIVE</span>
                </div>

                <div className={styles.logoBox}>
                  {channel.logo_url ? (
                    <img
                      src={channel.logo_url}
                      alt={channel.name}
                      className={styles.logo}
                      onError={e => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div
                    className={styles.logoFallback}
                    style={{ display: channel.logo_url ? 'none' : 'flex' }}
                  >
                    {channel.name.charAt(0).toUpperCase()}
                  </div>
                </div>

                <div className={styles.cardBottom}>
                  <span className={styles.name}>{channel.name}</span>
                  {channel.country && (
                    <span className={styles.country}>{channel.country}</span>
                  )}
                </div>
              </button>
            );
          })}
          <div ref={sentinelRef} className={styles.sentinel} />
        </div>
      )}

      {loadingMore && <div className={styles.loadingMore}>Cargando más canales...</div>}
    </div>
  );
}
