import React from 'react';

const formatEvent = (event) => {
  const date = new Date(event.timestamp).toUTCString();
  switch (event.action) {
    case 'PUSH':
      return `${event.author} pushed to ${event.to_branch} on ${date}`;
    case 'PULL_REQUEST':
      return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${date}`;
    case 'MERGE':
      return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${date}`;
    default:
      return '';
  }
};

const EventList = ({ events }) => {
  const styles = {
    list: {
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
      padding: 0,
      listStyle: 'none',
    },
    item: {
      backgroundColor: '#1c1c1e',
      padding: '1.2rem',
      borderRadius: '12px',
      boxShadow: '0 0 10px rgba(0, 191, 166, 0.2)',
      transition: 'transform 0.2s ease, box-shadow 0.3s ease',
      fontSize: '1rem',
      lineHeight: '1.5',
    },
    itemHover: {
      transform: 'scale(1.02)',
      boxShadow: '0 0 20px rgba(0, 191, 166, 0.35)',
    }
  };

  return (
    <ul style={styles.list}>
      {events.map((event) => (
        <li
          key={event.request_id}
          style={{
            ...styles.item,
            ':hover': styles.itemHover, // pseudo-hover effect using JS can't work here, so we keep it simple
          }}
        >
          {formatEvent(event)}
        </li>
      ))}
    </ul>
  );
};

export default EventList;
