import { useContext, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import { ChannelContext } from '../context/ChannelContext';
import { api } from '../services/api';
import VideoPlayer from '../components/VideoPlayer/VideoPlayer';
import SearchBar from '../components/SearchBar/SearchBar';
import ChannelInfoPanel from '../components/ChannelInfoPanel/ChannelInfoPanel';
import ChannelSidebar from '../components/ChannelSidebar/ChannelSidebar';
import styles from './Home.module.css';

function countryFlag(code) {
  if (!code || code.length !== 2) return '';
  return String.fromCodePoint(
    ...code.toUpperCase().split('').map(c => 0x1F1E6 - 65 + c.charCodeAt(0))
  );
}

export default function Home() {
  const { error, currentChannel, setCurrentChannel } = useContext(ChannelContext);
  const [searchParams, setSearchParams] = useSearchParams();
  const initializedRef = useRef(false);

  useEffect(() => {
    if (initializedRef.current) return;
    initializedRef.current = true;
    const slug = searchParams.get('channel');
    if (!slug) return;
    api.getChannelBySlug(slug)
      .then(channel => setCurrentChannel(channel))
      .catch(() => {});
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!currentChannel?.slug) return;
    setSearchParams({ channel: currentChannel.slug }, { replace: true });
  }, [currentChannel?.slug]); // eslint-disable-line react-hooks/exhaustive-deps

  if (error) return <div className={styles.error}>Error: {error}</div>;

  return (
    <div className={styles.home}>

      {/* ── Barra de búsqueda ── */}
      <SearchBar />

      {/* ── Cuerpo principal: sidebar + player + info ── */}
      <div className={styles.body}>

        {/* wrapper transparente en desktop; en mobile se convierte en columna ordenada al final */}
        <div className={styles.sidebarCol}>
          <ChannelSidebar />
        </div>

        <div className={styles.playerSection}>
          <VideoPlayer />
        </div>

        {/* canal activo: oculto en desktop, visible en mobile entre player y lista */}
        {currentChannel && (
          <div className={styles.mobileChannelBar}>
            <span className={styles.mobileLive} />
            <span className={styles.mobileChannelName}>{currentChannel.name}</span>
            {currentChannel.country && (
              <span className={styles.mobileChannelCountry}>
                {countryFlag(currentChannel.country)} {currentChannel.country}
              </span>
            )}
          </div>
        )}

        <ChannelInfoPanel />

      </div>

    </div>
  );
}
