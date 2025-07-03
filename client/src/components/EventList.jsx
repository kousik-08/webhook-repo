import React from 'react';

const formatEvent = (event) => {
  let dateStr = "Invalid Date";
  try {
    const rawTimestamp = event.timestamp?.$date || event.timestamp;
    const parsedDate = new Date(rawTimestamp);
    if (!isNaN(parsedDate.getTime())) {
      dateStr = parsedDate.toLocaleString("en-US", {
        dateStyle: "medium",
        timeStyle: "short",
        timeZone: "UTC"
      });
    } else {
      console.warn("Unparseable date:", rawTimestamp);
    }
  } catch (error) {
    console.error("Error formatting timestamp:", event.timestamp, error);
  }

  switch (event.action) {
    case 'PUSH':
      return `${event.author} pushed to ${event.to_branch} on ${dateStr}`;
    case 'PULL_REQUEST':
      return `${event.author} submitted a pull request from ${event.from_branch} to ${event.to_branch} on ${dateStr}`;
    case 'MERGE':
      return `${event.author} merged branch ${event.from_branch} to ${event.to_branch} on ${dateStr}`;
    default:
      return `Unknown event on ${dateStr}`;
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
      color: '#e0e0e0', // Added for better readability on dark background
    },
    // itemHover: { // This needs a proper CSS setup or state management for true hover effects in inline styles
    //   transform: 'scale(1.02)',
    //   boxShadow: '0 0 20px rgba(0, 191, 166, 0.35)',
    // }
  };

  return (
    <ul style={styles.list}>
      {events.map((event) => (
        <li
          key={event.request_id}
          style={styles.item} // Apply base style
          // For hover effects, it's generally better to use CSS classes or a library
          // If you *must* use inline styles for hover, you'd need state management
          // or a more complex solution.
        >
          {formatEvent(event)}
        </li>
      ))}
    </ul>
  );
};

export default EventList;