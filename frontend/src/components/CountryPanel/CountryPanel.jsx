import { useContext } from 'react';
import { ChannelContext } from '../../context/ChannelContext';
import styles from './CountryPanel.module.css';

function countryFlag(code) {
  if (!code || code.length !== 2) return '🌐';
  return String.fromCodePoint(
    ...code.toUpperCase().split('').map(c => 0x1F1E6 - 65 + c.charCodeAt(0))
  );
}

const COUNTRY_NAMES = {
  US: 'United States', MX: 'México', ES: 'España', BR: 'Brasil',
  AR: 'Argentina', CO: 'Colombia', CL: 'Chile', PE: 'Perú',
  VE: 'Venezuela', GB: 'UK', FR: 'France', DE: 'Germany',
  IT: 'Italy', RU: 'Russia', IN: 'India', CN: 'China',
  JP: 'Japan', KR: 'Korea', CA: 'Canada', AU: 'Australia',
  NL: 'Netherlands', TR: 'Turkey', PL: 'Poland', UA: 'Ukraine',
  DO: 'Dom. Rep.', EC: 'Ecuador', GT: 'Guatemala', HN: 'Honduras',
  CR: 'Costa Rica', CU: 'Cuba', PA: 'Panamá', PY: 'Paraguay',
  UY: 'Uruguay', BO: 'Bolivia', SV: 'El Salvador', NI: 'Nicaragua',
};

export default function CountryPanel() {
  const { countries, activeCountry, setActiveCountry } = useContext(ChannelContext);

  return (
    <aside className={styles.panel}>
      <h3 className={styles.title}>Países</h3>
      <div className={styles.list}>
        <button
          className={`${styles.item} ${!activeCountry ? styles.active : ''}`}
          onClick={() => setActiveCountry(null)}
        >
          <span className={styles.flag}>🌐</span>
          <span className={styles.name}>Todos</span>
        </button>

        {countries.map(({ country, count }) => (
          <button
            key={country}
            className={`${styles.item} ${activeCountry === country ? styles.active : ''}`}
            onClick={() => setActiveCountry(activeCountry === country ? null : country)}
            title={`${COUNTRY_NAMES[country] || country} (${count})`}
          >
            <span className={styles.flag}>{countryFlag(country)}</span>
            <span className={styles.name}>{COUNTRY_NAMES[country] || country}</span>
            <span className={styles.count}>{count}</span>
          </button>
        ))}
      </div>
    </aside>
  );
}
