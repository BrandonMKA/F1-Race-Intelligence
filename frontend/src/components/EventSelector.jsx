export default function EventSelector({
  events,
  selectedEventId,
  onChange,
  disabled = false,
}) {
  return (
    <label className="event-selector">
      <span>Select race</span>

      <select
        value={selectedEventId}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
      >
        <option value="">Choose an event</option>

        {events.map((event) => (
          <option key={event.event_id} value={event.event_id}>
            {event.season} — {event.event_name}
          </option>
        ))}
      </select>
    </label>
  );
}