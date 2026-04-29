import { useContext } from 'react';
import { ChannelContext } from '../../context/ChannelContext';
import styles from './SearchBar.module.css';

const regionNames = new Intl.DisplayNames(['es'], { type: 'region' });

function countryName(code) {
  try { return regionNames.of(code.toUpperCase()); } catch { return code; }
}

export default function SearchBar() {
  const {
    search, setSearch,
    categories, activeCategory, setActiveCategory,
    countries, activeCountry, setActiveCountry,
  } = useContext(ChannelContext);

  const hasFilters = search || activeCountry || activeCategory;
  const clearAll = () => { setSearch(''); setActiveCountry(null); setActiveCategory(null); };

  return (
    <div className={styles.bar}>
      <div className={styles.searchWrapper}>
        <svg className={styles.icon} viewBox="0 0 20 20" fill="none">
          <circle cx="8.5" cy="8.5" r="5.5" stroke="currentColor" strokeWidth="1.6"/>
          <path d="M13 13l3.5 3.5" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round"/>
        </svg>
        <input
          type="text"
          className={styles.input}
          placeholder="Buscar canal..."
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        {search && (
          <button className={styles.clear} onClick={() => setSearch('')}>✕</button>
        )}
      </div>

      {/* País — solo visible cuando panel lateral está oculto */}
      <select
        className={`${styles.select} ${styles.selectCountry}`}
        value={activeCountry || ''}
        onChange={e => setActiveCountry(e.target.value || null)}
      >
        <option value="">🌐 País</option>
        {countries.map(({ country, count }) => (
          <option key={country} value={country}>{countryName(country)} ({count})</option>
        ))}
      </select>

      <select
        className={styles.select}
        value={activeCategory || ''}
        onChange={e => setActiveCategory(e.target.value || null)}
      >
        <option value="">Categoría</option>
        {categories.map(cat => (
          <option key={cat.id} value={cat.slug}>{cat.name}</option>
        ))}
      </select>

      <button
        className={`${styles.clearAll} ${!hasFilters ? styles.clearAllDisabled : ''}`}
        onClick={clearAll}
        disabled={!hasFilters}
      >
        ✕ Limpiar
      </button>
    </div>
  );
}
