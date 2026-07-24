export default function ConstructorTable({ constructors }) {
  return (
    <section className="data-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Teams</p>
          <h3>Constructor performance</h3>
        </div>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Constructor</th>
              <th>Drivers</th>
              <th>Points</th>
              <th>Best finish</th>
              <th>Average finish</th>
            </tr>
          </thead>

          <tbody>
            {constructors.map((constructor) => (
              <tr key={constructor.constructor_id}>
                <td>
                  <strong>{constructor.constructor_name}</strong>
                </td>
                <td>{constructor.driver_count}</td>
                <td>{constructor.total_points}</td>
                <td>{constructor.best_finish ?? "—"}</td>
                <td>
                  {constructor.average_finish !== null
                    ? Number(
                        constructor.average_finish
                      ).toFixed(2)
                    : "—"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}