import { createContext, useState, useEffect, useCallback, useRef } from 'react';
import { api } from '../services/api';

export const ChannelContext = createContext();

const LIMIT = 100;

export function ChannelProvider({ children }) {
  const [categories, setCategories] = useState([]);
  const [countries, setCountries] = useState([]);
  const [channels, setChannels] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [currentChannel, setCurrentChannel] = useState(null);

  const [search, setSearch] = useState('');
  const [activeCountry, setActiveCountry] = useState(null);
  const [activeCategory, setActiveCategory] = useState(null);
  const [offset, setOffset] = useState(0);

  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(null);

  const debounceRef = useRef(null);

  // Carga inicial: categorías y países (una sola vez)
  useEffect(() => {
    Promise.all([api.getCategories(), api.getCountries()])
      .then(([cats, ctrs]) => {
        setCategories(cats);
        setCountries(ctrs);
      })
      .catch(console.error);
  }, []);

  const fetchChannels = useCallback(async ({ searchVal, country, category, newOffset, append }) => {
    try {
      if (append) setLoadingMore(true);
      else setLoading(true);

      const [data, countData] = await Promise.all([
        api.getChannels({ search: searchVal, country, categorySlug: category, limit: LIMIT, offset: newOffset }),
        newOffset === 0
          ? api.getChannelsCount({ search: searchVal, country, categorySlug: category })
          : Promise.resolve(null),
      ]);

      setChannels(prev => append ? [...prev, ...data] : data);
      if (countData) setTotalCount(countData.count);

      if (!append && data.length > 0 && newOffset === 0) {
        setCurrentChannel(data[0]);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, []);

  // Re-fetch cuando cambian los filtros (con debounce en la búsqueda)
  useEffect(() => {
    setOffset(0);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      fetchChannels({ searchVal: search, country: activeCountry, category: activeCategory, newOffset: 0, append: false });
    }, search ? 300 : 0);

    return () => clearTimeout(debounceRef.current);
  }, [search, activeCountry, activeCategory, fetchChannels]);

  const loadMore = useCallback(() => {
    const newOffset = offset + LIMIT;
    setOffset(newOffset);
    fetchChannels({ searchVal: search, country: activeCountry, category: activeCategory, newOffset, append: true });
  }, [offset, search, activeCountry, activeCategory, fetchChannels]);

  const hasMore = channels.length < totalCount;

  return (
    <ChannelContext.Provider value={{
      channels,
      categories,
      countries,
      currentChannel,
      setCurrentChannel,
      search,
      setSearch,
      activeCountry,
      setActiveCountry,
      activeCategory,
      setActiveCategory,
      loading,
      loadingMore,
      error,
      totalCount,
      hasMore,
      loadMore,
    }}>
      {children}
    </ChannelContext.Provider>
  );
}
