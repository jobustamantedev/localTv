import { createContext, useState, useEffect, useRef } from 'react';

export const FavoritesContext = createContext();

const STORAGE_KEY = 'bustaTv_favorites_v2';

export function FavoritesProvider({ children }) {
  const [favorites, setFavorites] = useState([]); // array de objetos canal completos
  const initialized = useRef(false);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) setFavorites(JSON.parse(stored));
    } catch {}
    initialized.current = true;
  }, []);

  useEffect(() => {
    if (!initialized.current) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(favorites));
    } catch {}
  }, [favorites]);

  const isFavorite = (channelId) => favorites.some(ch => ch.id === channelId);

  const toggleFavorite = (channel) => {
    setFavorites(prev =>
      prev.some(ch => ch.id === channel.id)
        ? prev.filter(ch => ch.id !== channel.id)
        : [...prev, channel]
    );
  };

  return (
    <FavoritesContext.Provider value={{ favorites, toggleFavorite, isFavorite }}>
      {children}
    </FavoritesContext.Provider>
  );
}
