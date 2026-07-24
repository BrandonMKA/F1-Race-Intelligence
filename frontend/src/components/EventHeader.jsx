function formatDate(value) {
  if (!value) {
    return "Date unavailable";
  }

  return new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(value));
}

export default function EventHeader({ event }) {
  if (!event) {
    return null;
  }

  return (
    <section className="event-header">
      <div>
        <p className="eyebrow">
          {event.season} Formula 1 · Round {event.round_number}
        </p>

        <h2>{event.event_name}</h2>

        <p className="event-meta">
          {event.session_name}
          <span>•</span>
          {formatDate(event.session_date)}
        </p>
      </div>

      <div className="event-stat-grid">
        <article className="event-stat">
          <span>Results</span>
          <strong>{event.result_count ?? 0}</strong>
        </article>

        <article className="event-stat">
          <span>Laps</span>
          <strong>
            {Number(event.lap_count ?? 0).toLocaleString()}
          </strong>
        </article>
      </div>
    </section>
  );
}