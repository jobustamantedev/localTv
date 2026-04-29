import { useContext, useRef, useEffect, useCallback } from 'react';
import { ChannelContext } from '../../context/ChannelContext';
import { FavoritesContext } from '../../context/FavoritesContext';
import styles from './ChannelSidebar.module.css';

function countryFlag(code) {
  if (!code || code.length !== 2) return '';
  return String.fromCodePoint(
    ...code.toUpperCase().split('').map(c => 0x1F1E6 - 65 + c.charCodeAt(0))
  );
}

function ChannelRow({ channel, index, isActive, onSelect, isFav, onToggleFav }) {
  const num = index !== undefined ? String(index + 1).padStart(2, '0') : null;

  return (
    <button
      className={`${styles.row} ${isActive ? styles.rowActive : ''}`}
      onClick={() => onSelect(channel)}
      title={channel.name}
    >
      <div className={styles.rowLogo}>
        {channel.logo_url ? (
          <img
            src={channel.logo_url}
            alt={channel.name}
            className={styles.rowLogoImg}
            onError={e => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
          />
        ) : null}
        <div className={styles.rowLogoFallback} style={{ display: channel.logo_url ? 'none' : 'flex' }}>
          {channel.name.charAt(0)}
        </div>
      </div>

      <div className={styles.rowInfo}>
        {num && <span className={styles.rowNum}>CH {num}</span>}
        <span className={styles.rowName}>{channel.name}</span>
        {channel.country && (
          <span className={styles.rowCountry}>{countryFlag(channel.country)} {channel.country}</span>
        )}
      </div>

      <button
        className={`${styles.favBtn} ${isFav ? styles.favActive : ''}`}
        onClick={e => { e.stopPropagation(); onToggleFav(channel); }}
        title={isFav ? 'Quitar de favoritos' : 'Agregar a favoritos'}
      >
        {isFav ? '★' : '☆'}
      </button>
    </button>
  );
}

export default function ChannelSidebar() {
  const {
    channels, currentChannel, setCurrentChannel,
    hasMore, loadMore, loadingMore, totalCount, loading,
  } = useContext(ChannelContext);

  const { favorites, toggleFavorite, isFavorite } = useContext(FavoritesContext);
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
    <aside className={styles.sidebar}>

      {/* ── Favoritos ── */}
      {favorites.length > 0 && (
        <div className={styles.section}>
          <div className={styles.sectionHeader}>
            <span className={styles.sectionTitle}>// FAVORITOS</span>
            <span className={styles.sectionCount}>{favorites.length}</span>
          </div>
          <div className={styles.list}>
            {favorites.map(channel => (
              <ChannelRow
                key={channel.id}
                channel={channel}
                isActive={currentChannel?.id === channel.id}
                onSelect={setCurrentChannel}
                isFav={true}
                onToggleFav={toggleFavorite}
              />
            ))}
          </div>
          <div className={styles.divider} />
        </div>
      )}

      {/* ── Todos los canales ── */}
      <div className={styles.section} style={{ flex: 1, minHeight: 0 }}>
        <div className={styles.sectionHeader}>
          <span className={styles.sectionTitle}>// EN VIVO</span>
          <span className={styles.sectionCount}>{totalCount.toLocaleString()}</span>
        </div>

        <div className={styles.list}>
          {loading ? (
            <div className={styles.empty}>Cargando...</div>
          ) : !channels.length ? (
            <div className={styles.empty}>Sin resultados</div>
          ) : (
            <>
              {channels.map((channel, i) => (
                <ChannelRow
                  key={channel.id}
                  channel={channel}
                  index={i}
                  isActive={currentChannel?.id === channel.id}
                  onSelect={setCurrentChannel}
                  isFav={isFavorite(channel.id)}
                  onToggleFav={toggleFavorite}
                />
              ))}
              <div ref={sentinelRef} className={styles.sentinel} />
              {loadingMore && <div className={styles.loadingMore}>Cargando más...</div>}
            </>
          )}
        </div>
      </div>

    </aside>
  );
}
