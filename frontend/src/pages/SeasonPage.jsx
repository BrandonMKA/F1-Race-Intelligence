import { Link, useParams } from "react-router-dom";

function SeasonPage({ events }) {
  const { season } = useParams();
  const races = events
    .filter((event) => String(event.season) === String(season))
    .sort(
      (first, second) =>
        Number(first.round_number) - Number(second.round_number)
    );

  if (races.length === 0) {
    return (
      <main>
        <div className="empty-panel">
          <h2>No races found for {season}</h2>
          <p>This season has not been loaded into the database.</p>
          <Link className="text-link" to="/">
            Return to seasons
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
        <span>{season}</span>
      </div>

      <section className="page-hero page-hero-compact">
        <p className="eyebrow">Championship season</p>
        <h1>{season} Formula 1 season</h1>
        <p>Select a race to open its complete race-intelligence dashboard.</p>
      </section>

      <section className="race-grid" aria-label={`${season} races`}>
        {races.map((race) => (
          <Link
            key={race.event_id}
            to={`/seasons/${season}/races/${race.event_id}`}
            className="race-card"
          >
            <div className="race-card-topline">
              <span>Round {race.round_number}</span>
              <span>{race.country ?? race.location ?? "Grand Prix"}</span>
            </div>
            <h2>{race.event_name}</h2>
            <p>{race.circuit_name ?? race.location ?? "Circuit information"}</p>
            <strong>View race dashboard →</strong>
          </Link>
        ))}
      </section>
    </main>
  );
}

export default SeasonPage;
