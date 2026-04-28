import { useState } from 'react';
import ChannelSidebar from '../ChannelSidebar/ChannelSidebar';
import DailyEvents from '../DailyEvents/DailyEvents';
import styles from './SidebarWithTabs.module.css';

export default function SidebarWithTabs({ onStreamClick }) {
  const [activeTab, setActiveTab] = useState('canales');

  return (
    <aside className={styles.sidebar}>
      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'canales' ? styles.active : ''}`}
          onClick={() => setActiveTab('canales')}
        >
          Canales
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'eventos' ? styles.active : ''}`}
          onClick={() => setActiveTab('eventos')}
        >
          Eventos
        </button>
      </div>

      <div className={styles.content}>
        {activeTab === 'canales' ? <ChannelSidebar /> : <DailyEvents onStreamClick={onStreamClick} />}
      </div>
    </aside>
  );
}
