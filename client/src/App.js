import React, { useEffect, useState } from 'react';
import axios from 'axios';
import EventList from './components/EventList';

function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const res = await axios.get('http://localhost:5000/events');
        setEvents(res.data);
      } catch (err) {
        console.error('Error fetching events:', err.message);
      }
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1 style={styles.title}>🚀 GitHub Webhook Dashboard</h1>
        <p style={styles.subtitle}>Auto-updating every 15 seconds</p>
      </header>
      <main style={styles.main}>
        <EventList events={events} />
      </main>
    </div>
  );
}

const styles = {
  app: {
    backgroundColor: '#0e0e0e',
    color: '#f1f1f1',
    minHeight: '100vh',
    padding: '2rem',
    fontFamily: 'Inter, Segoe UI, sans-serif',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    textAlign: 'center',
    marginBottom: '2rem',
  },
  title: {
    fontSize: '2.5rem',
    margin: 0,
    color: '#00bfa6',
  },
  subtitle: {
    color: '#aaaaaa',
    marginTop: '0.5rem',
  },
  main: {
    maxWidth: '800px',
    margin: '0 auto',
    width: '100%',
  }
};

export default App;
