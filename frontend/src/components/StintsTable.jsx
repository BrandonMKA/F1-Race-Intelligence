function formatLapTime(milliseconds) {
  if (milliseconds === null || milliseconds === undefined) {
    return "—";
  }

  const totalSeconds = milliseconds / 1000;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return `${minutes}:${seconds.toFixed(3).padStart(6, "0")}`;
}

export default function StintsTable({ stints }) {
  return (
    <section className="data-panel data-panel-wide">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Strategy</p>
          <h3>Tire stints</h3>
        </div>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Driver</th>
              <th>Stint</th>
              <th>Compound</th>
              <th>Lap range</th>
              <th>Laps</th>
              <th>Average pace</th>
              <th>Fastest lap</th>
            </tr>
          </thead>

          <tbody>
            {stints.map((stint) => (
              <tr
                key={`${stint.driver_id}-${stint.stint_number}-${stint.compound}`}
              >
                <td>
                  <strong>{stint.driver_code}</strong>
                </td>
                <td>{stint.stint_number}</td>
                <td>{stint.compound ?? "Unknown"}</td>
                <td>
                  {stint.first_lap}–{stint.last_lap}
                </td>
                <td>{stint.lap_count}</td>
                <td>
                  {formatLapTime(stint.average_lap_time_ms)}
                </td>
                <td>
                  {formatLapTime(stint.fastest_lap_time_ms)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}