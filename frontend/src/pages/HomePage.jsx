import { Link } from "react-router-dom";

function HomePage({ events }) {
  const seasons = [...new Set(events.map((event) => Number(event.season)))]
    .filter(Number.isFinite)
    .sort((first, second) => second - first);

  return (
    <main>
      <section className="page-hero">
        <p className="eyebrow">Formula 1 analytics</p>
        <h1>Explore race intelligence by season.</h1>
        <p>
          Select a championship season to review every loaded race, then open a
          race dashboard for pace, strategy, position, and classification data.
        </p>
      </section>

      <section className="browse-section" aria-labelledby="season-heading">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Available data</p>
            <h2 id="season-heading">Choose a season</h2>
          </div>
          <p>{seasons.length} seasons currently loaded.</p>
        </div>

        <div className="season-grid">
          {seasons.map((season) => {
            const seasonEvents = events.filter(
              (event) => Number(event.season) === season
            );

            return (
              <Link
                key={season}
                to={`/seasons/${season}`}
                className="season-card"
              >
                <span className="season-year">{season}</span>
                <span>{seasonEvents.length} races</span>
                <strong>View season →</strong>
              </Link>
            );
          })}
        </div>
      </section>
    </main>
  );
}

export default HomePage;
