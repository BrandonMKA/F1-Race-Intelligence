function formatLapTime(milliseconds) {
  if (milliseconds === null || milliseconds === undefined) {
    return "—";
  }

  const totalSeconds = milliseconds / 1000;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return `${minutes}:${seconds.toFixed(3).padStart(6, "0")}`;
}

export default function FastestLapsTable({ laps }) {
  return (
    <section className="data-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Pace</p>
          <h3>Fastest laps</h3>
        </div>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>Driver</th>
              <th>Lap</th>
              <th>Compound</th>
              <th>Time</th>
            </tr>
          </thead>

          <tbody>
            {laps.map((lap) => (
              <tr key={lap.driver_id}>
                <td className="position-cell">{lap.position}</td>
                <td>
                  <div className="driver-cell">
                    <strong>{lap.driver_code}</strong>
                    <span>{lap.constructor_name ?? "—"}</span>
                  </div>
                </td>
                <td>{lap.lap_number}</td>
                <td>{lap.compound ?? "Unknown"}</td>
                <td className="lap-time">
                  {formatLapTime(lap.lap_time_ms)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}