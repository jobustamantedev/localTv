import { useContext } from 'react';
import { ChannelContext } from '../../context/ChannelContext';
import { FavoritesContext } from '../../context/FavoritesContext';
import styles from './ChannelInfoPanel.module.css';

function countryFlag(code) {
  if (!code || code.length !== 2) return '';
  return String.fromCodePoint(
    ...code.toUpperCase().split('').map(c => 0x1F1E6 - 65 + c.charCodeAt(0))
  );
}

export default function ChannelInfoPanel() {
  const { currentChannel, categories } = useContext(ChannelContext);
  const { isFavorite, toggleFavorite } = useContext(FavoritesContext);

  if (!currentChannel) {
    return (
      <aside className={styles.panel}>
        <div className={styles.empty}>
          <span className={styles.emptyIcon}>📺</span>
          <p>Selecciona un canal</p>
        </div>
      </aside>
    );
  }

  const category = categories.find(c => c.id === currentChannel.category_id);
  const favorite = isFavorite(currentChannel.id);

  return (
    <aside className={styles.panel}>
      <div className={styles.sectionLabel}>// AHORA AL AIRE</div>

      <div className={styles.logoArea}>
        {currentChannel.logo_url ? (
          <img
            src={currentChannel.logo_url}
            alt={currentChannel.name}
            className={styles.logo}
            onError={e => { e.target.style.display = 'none'; }}
          />
        ) : (
          <div className={styles.logoFallback}>📺</div>
        )}
      </div>

      <div className={styles.body}>
        <h2 className={styles.channelName}>{currentChannel.name}</h2>

        <div className={styles.badges}>
          <span className={styles.badgeLive}>EN VIVO</span>
          {category && <span className={styles.badge}>{category.name.toUpperCase()}</span>}
          {currentChannel.quality && <span className={styles.badge}>{currentChannel.quality.toUpperCase()}</span>}
          {currentChannel.country && <span className={styles.badge}>{currentChannel.country}</span>}
        </div>

        <div className={styles.stats}>
          <div className={styles.stat}>
            <span className={styles.statLabel}>PAÍS</span>
            <span className={styles.statValue}>
              {currentChannel.country
                ? `${countryFlag(currentChannel.country)} ${currentChannel.country}`
                : '—'}
            </span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statLabel}>CALIDAD</span>
            <span className={styles.statValue}>{currentChannel.quality || '—'}</span>
          </div>
          <div className={styles.stat}>
            <span className={styles.statLabel}>CATEGORÍA</span>
            <span className={styles.statValue}>{category?.name || '—'}</span>
          </div>
        </div>

        <button className={styles.playBtn}>
          ▶ REPRODUCIR
        </button>

        <button
          className={`${styles.favBtn} ${favorite ? styles.favActive : ''}`}
          onClick={() => toggleFavorite(currentChannel)}
        >
          {favorite ? '★ FAVORITO' : '☆ AGREGAR A FAVORITOS'}
        </button>

        {currentChannel.source_id && (
          <div className={styles.feedId}>
            FEED ID: {currentChannel.source_id}
          </div>
        )}
      </div>
    </aside>
  );
}
