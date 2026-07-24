export default function ResultsTable({ results }) {
  return (
    <section className="data-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Classification</p>
          <h3>Race results</h3>
        </div>

        <span className="record-count">
          {results.length} drivers
        </span>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Finish</th>
              <th>Driver</th>
              <th>Constructor</th>
              <th>Grid</th>
              <th>Points</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {results.map((result) => (
              <tr key={result.driver_id}>
                <td className="position-cell">
                  {result.finish_position ?? "—"}
                </td>

                <td>
                  <div className="driver-cell">
                    <strong>{result.driver_code}</strong>
                    <span>{result.full_name}</span>
                  </div>
                </td>

                <td>{result.constructor_name ?? "—"}</td>
                <td>{result.grid_position ?? "Pit lane"}</td>
                <td>{result.points ?? 0}</td>
                <td>{result.status ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}