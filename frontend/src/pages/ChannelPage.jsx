import { useContext, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChannelContext } from '../context/ChannelContext';
import { api } from '../services/api';
import Home from './Home';

export default function ChannelPage() {
  const { channelId } = useParams();
  const { setCurrentChannel } = useContext(ChannelContext);
  const navigate = useNavigate();

  useEffect(() => {
    api.getChannel(parseInt(channelId))
      .then(channel => {
        setCurrentChannel(channel);
        navigate('/', { replace: true });
      })
      .catch(() => navigate('/', { replace: true }));
  }, [channelId, setCurrentChannel, navigate]);

  return <Home />;
}
