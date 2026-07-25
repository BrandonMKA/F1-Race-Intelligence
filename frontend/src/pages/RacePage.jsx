import { Link, useParams } from "react-router-dom";

import RaceDashboard from "../components/RaceDashboard";

function RacePage({ events }) {
  const { season, eventId } = useParams();
  const selectedEvent = events.find(
    (event) => String(event.event_id) === String(eventId)
  );

  if (!selectedEvent) {
    return (
      <main>
        <div className="empty-panel">
          <h2>Race not found</h2>
          <p>The requested race is not available in the loaded dataset.</p>
          <Link className="text-link" to={`/seasons/${season}`}>
            Return to the season
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main>
      <div className="breadcrumb-row">
        <Link to="/">Seasons</Link>
        <span aria-hidden="true">/</span>
        <Link to={`/seasons/${season}`}>{season}</Link>
        <span aria-hidden="true">/</span>
        <span>{selectedEvent.event_name}</span>
      </div>

      <RaceDashboard eventId={eventId} />
    </main>
  );
}

export default RacePage;
