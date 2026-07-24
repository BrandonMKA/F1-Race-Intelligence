function formatGain(value) {
  if (value === null || value === undefined) {
    return "—";
  }

  if (value > 0) {
    return `+${value}`;
  }

  return String(value);
}

export default function PositionGainsTable({ drivers }) {
  return (
    <section className="data-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Race movement</p>
          <h3>Position gains</h3>
        </div>
      </div>

      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Driver</th>
              <th>Grid</th>
              <th>Finish</th>
              <th>Change</th>
            </tr>
          </thead>

          <tbody>
            {drivers.map((driver) => (
              <tr key={driver.driver_id}>
                <td>
                  <div className="driver-cell">
                    <strong>{driver.driver_code}</strong>
                    <span>{driver.constructor_name ?? "—"}</span>
                  </div>
                </td>
                <td>{driver.grid_position ?? "—"}</td>
                <td>{driver.finish_position ?? "—"}</td>
                <td
                  className={
                    driver.positions_gained > 0
                      ? "gain-positive"
                      : driver.positions_gained < 0
                        ? "gain-negative"
                        : ""
                  }
                >
                  {formatGain(driver.positions_gained)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}