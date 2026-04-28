import { useEffect, useState } from 'react';
import { api } from '../../services/api';
import styles from './DailyEvents.module.css';

export default function DailyEvents({ onStreamClick }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        setLoading(true);
        const data = await api.getDiaryEvents();
        const sortedEvents = (data.data || []).sort((a, b) => {
          const timeA = a.attributes.diary_hour || '00:00:00';
          const timeB = b.attributes.diary_hour || '00:00:00';
          return timeA.localeCompare(timeB);
        });
        setEvents(sortedEvents);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, []);

  if (loading) {
    return (
      <section className={styles.section}>
        <h2 className={styles.title}>Eventos del Día</h2>
        <div className={styles.loadingMessage}>Cargando eventos...</div>
      </section>
    );
  }

  if (error) {
    return (
      <section className={styles.section}>
        <h2 className={styles.title}>Eventos del Día</h2>
        <div className={styles.errorMessage}>No se pudieron cargar los eventos</div>
      </section>
    );
  }

  if (!events.length) {
    return (
      <section className={styles.section}>
        <h2 className={styles.title}>Eventos del Día</h2>
        <div className={styles.emptyMessage}>No hay eventos disponibles</div>
      </section>
    );
  }

  const filteredEvents = events.filter((event) => {
    const competitionName = event.attributes.country?.data?.attributes.name || 'Otros';
    const eventTitle = event.attributes.diary_description || '';
    const streamNames = event.attributes.embeds?.data?.map(e => e.attributes.embed_name).join(' ') || '';
    const searchLower = searchQuery.toLowerCase();

    return (
      competitionName.toLowerCase().includes(searchLower) ||
      eventTitle.toLowerCase().includes(searchLower) ||
      streamNames.toLowerCase().includes(searchLower)
    );
  });

  const groupedByCompetition = filteredEvents.reduce((acc, event) => {
    const competitionName = event.attributes.country?.data?.attributes.name || 'Otros';
    const competitionData = event.attributes.country?.data;

    if (!acc[competitionName]) {
      acc[competitionName] = {
        data: competitionData,
        events: [],
      };
    }
    acc[competitionName].events.push(event);
    return acc;
  }, {});

  return (
    <section className={styles.section}>
      <h2 className={styles.title}>Eventos del Día</h2>
      <input
        type="text"
        placeholder="Buscar evento..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className={styles.searchInput}
      />
      {Object.keys(groupedByCompetition).length === 0 && !loading ? (
        <div className={styles.emptyMessage}>No hay eventos que coincidan con tu búsqueda</div>
      ) : (
      <div className={styles.competitionsContainer}>
        {Object.entries(groupedByCompetition).map(([competitionName, { data: competitionData, events: competitionEvents }]) => (
          <div key={competitionName} className={styles.competitionGroup}>
            <div className={styles.competitionHeader}>
              {competitionData?.attributes.image?.data?.attributes?.url && (
                <img
                  src={`https://pltvhd.com${competitionData.attributes.image.data.attributes.url}`}
                  alt={competitionName}
                  className={styles.competitionLogo}
                  onError={(e) => {
                    e.target.style.display = 'none';
                  }}
                />
              )}
              <h3 className={styles.competitionTitle}>{competitionName}</h3>
            </div>
            <div className={styles.eventsList}>
              {competitionEvents.map((event) => (
                <div key={event.id} className={styles.eventCard}>
                  <h4 className={styles.eventTitle}>
                    {event.attributes.diary_description}
                  </h4>
                  <div className={styles.eventTime}>
                    {event.attributes.diary_hour.substring(0, 5)}
                  </div>
                  {event.attributes.embeds?.data && event.attributes.embeds.data.length > 0 && (
                    <div className={styles.streamsList}>
                      {event.attributes.embeds.data.map((embed) => (
                        <button
                          key={embed.id}
                          className={styles.streamBadge}
                          onClick={() => onStreamClick && onStreamClick(embed.attributes.embed_name)}
                        >
                          {embed.attributes.embed_name}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      )}
    </section>
  );
}
