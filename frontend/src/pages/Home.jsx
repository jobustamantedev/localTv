import { useContext } from 'react';
import { ChannelContext } from '../context/ChannelContext';
import VideoPlayer from '../components/VideoPlayer/VideoPlayer';
import SidebarWithTabs from '../components/SidebarWithTabs/SidebarWithTabs';
import ChannelInfo from '../components/ChannelInfo/ChannelInfo';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import ChannelList from '../components/ChannelList/ChannelList';
import styles from './Home.module.css';

export default function Home() {
  const { currentChannel, loading, error, channels, setCurrentChannel } = useContext(ChannelContext);

  const handleStreamClick = (streamName) => {
    // Buscar canal que coincida con el nombre del stream
    const matchedChannel = channels.find(
      (channel) => streamName.toLowerCase().includes(channel.name.toLowerCase()) ||
                   channel.name.toLowerCase().includes(streamName.toLowerCase())
    );

    if (matchedChannel) {
      setCurrentChannel(matchedChannel);
    }
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className={styles.error}>Error: {error}</div>;

  return (
    <div className={styles.home}>
      {/* Layout desktop: player 70% + sidebar 30% */}
      <div className={styles.mainContent}>
        <div className={styles.playerSection}>
          {currentChannel && (
            <h2 className={styles.channelTitle}>{currentChannel.name}</h2>
          )}
          <div className={styles.videoContainer}>
            <VideoPlayer channel={currentChannel} />
          </div>
          {currentChannel && (
            <p className={styles.liveStatus}>
              {currentChannel.is_active ? '🔴 EN VIVO' : '⚪ Offline'}
            </p>
          )}
        </div>
        <SidebarWithTabs onStreamClick={handleStreamClick} />
      </div>

      {/* Mobile: mostrar ChannelList debajo */}
      <div className={styles.mobileList}>
        <ChannelList />
      </div>
    </div>
  );
}
