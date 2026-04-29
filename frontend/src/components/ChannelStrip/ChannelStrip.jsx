import { useContext, useRef } from 'react';
import { ChannelContext } from '../../context/ChannelContext';
import styles from './ChannelStrip.module.css';

export default function ChannelStrip() {
  const { channels, currentChannel, setCurrentChannel, loadingMore, hasMore, loadMore, totalCount, loading } = useContext(ChannelContext);
  const stripRef = useRef(null);

  const scroll = (dir) => {
    if (stripRef.current) {
      stripRef.current.scrollBy({ left: dir * 300, behavior: 'smooth' });
    }
  };

  if (loading) {
    return (
      <div className={styles.strip}>
        <div className={styles.loadingMsg}>Cargando canales...</div>
      </div>
    );
  }

  if (!channels.length) {
    return (
      <div className={styles.strip}>
        <div className={styles.loadingMsg}>Sin resultados</div>
      </div>
    );
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.meta}>
        <span className={styles.count}>{totalCount.toLocaleString()} canales</span>
      </div>

      <div className={styles.scrollArea}>
        <button className={`${styles.arrow} ${styles.arrowLeft}`} onClick={() => scroll(-1)}>‹</button>

        <div className={styles.strip} ref={stripRef}>
          {channels.map(channel => (
            <button
              key={channel.id}
              className={`${styles.card} ${currentChannel?.id === channel.id ? styles.active : ''}`}
              onClick={() => setCurrentChannel(channel)}
              title={channel.name}
            >
              <div className={styles.logoBox}>
                {channel.logo_url ? (
                  <img
                    src={channel.logo_url}
                    alt={channel.name}
                    className={styles.logo}
                    onError={e => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
                  />
                ) : null}
                <div className={styles.logoFallback} style={{ display: channel.logo_url ? 'none' : 'flex' }}>
                  📺
                </div>
              </div>
              <span className={styles.name}>{channel.name}</span>
            </button>
          ))}

          {hasMore && (
            <button
              className={styles.loadMoreBtn}
              onClick={loadMore}
              disabled={loadingMore}
            >
              {loadingMore ? '...' : `+${(totalCount - channels.length).toLocaleString()}`}
            </button>
          )}
        </div>

        <button className={`${styles.arrow} ${styles.arrowRight}`} onClick={() => scroll(1)}>›</button>
      </div>
    </div>
  );
}
