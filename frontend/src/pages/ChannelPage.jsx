import { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ChannelContext } from '../context/ChannelContext';
import VideoPlayer from '../components/VideoPlayer/VideoPlayer';
import ChannelInfo from '../components/ChannelInfo/ChannelInfo';
import SidebarWithTabs from '../components/SidebarWithTabs/SidebarWithTabs';
import ChannelList from '../components/ChannelList/ChannelList';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import styles from './Home.module.css';

export default function ChannelPage() {
  const { channelId } = useParams();
  const { channels, setCurrentChannel, loading: contextLoading } = useContext(ChannelContext);
  const [channel, setChannel] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleStreamClick = (streamName) => {
    const matchedChannel = channels.find(
      (ch) => streamName.toLowerCase().includes(ch.name.toLowerCase()) ||
              ch.name.toLowerCase().includes(streamName.toLowerCase())
    );

    if (matchedChannel) {
      setCurrentChannel(matchedChannel);
    }
  };

  useEffect(() => {
    setLoading(true);
    setError(null);

    const foundChannel = channels.find(ch => ch.id === parseInt(channelId));

    if (foundChannel) {
      setChannel(foundChannel);
      setCurrentChannel(foundChannel);
      setLoading(false);
    } else if (channels.length > 0 && !contextLoading) {
      setError(`Canal con ID ${channelId} no encontrado`);
      setLoading(false);
    } else if (!contextLoading) {
      setError(`Canal con ID ${channelId} no encontrado`);
      setLoading(false);
    }
  }, [channelId, channels, contextLoading, setCurrentChannel]);

  if (loading || contextLoading) return <LoadingSpinner />;
  if (error) return <div className={styles.error}>Error: {error}</div>;
  if (!channel) return <div className={styles.error}>Canal no encontrado</div>;

  return (
    <div className={styles.home}>
      <div className={styles.mainContent}>
        <div className={styles.playerSection}>
          {channel && (
            <h2 className={styles.channelTitle}>{channel.name}</h2>
          )}
          <div className={styles.videoContainer}>
            <VideoPlayer channel={channel} />
          </div>
          {channel && (
            <p className={styles.liveStatus}>
              {channel.is_active ? '🔴 EN VIVO' : '⚪ Offline'}
            </p>
          )}
        </div>
        <SidebarWithTabs onStreamClick={handleStreamClick} />
      </div>

      <div className={styles.mobileList}>
        <ChannelList />
      </div>
    </div>
  );
}
