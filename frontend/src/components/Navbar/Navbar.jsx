import { Link } from 'react-router-dom';
import styles from './Navbar.module.css';

export default function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={styles.container}>
        <Link to="/" className={styles.logoLink}>
          <img src="/logo.png" alt="Fútbol En Vivo" className={styles.logo} />
          <span className={styles.brandName}></span>
        </Link>
        <div className={styles.menu}>
          <Link to="/" className={styles.link}>Eventos</Link>
        </div>
      </div>
    </nav>
  );
}
