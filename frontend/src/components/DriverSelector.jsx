export default function DriverSelector({
  drivers,
  selectedDriverCodes,
  onToggle,
  maxSelections = 4,
}) {
  function handleToggle(driverCode) {
    const isSelected = selectedDriverCodes.includes(driverCode);

    if (!isSelected && selectedDriverCodes.length >= maxSelections) {
      return;
    }

    onToggle(driverCode);
  }

  return (
    <section className="driver-selector-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Comparison</p>
          <h3>Select drivers</h3>
        </div>

        <span className="record-count">
          {selectedDriverCodes.length}/{maxSelections} selected
        </span>
      </div>

      <div className="driver-selector-grid">
        {drivers.map((driver) => {
          const isSelected = selectedDriverCodes.includes(
            driver.driver_code
          );

          const selectionLimitReached =
            !isSelected &&
            selectedDriverCodes.length >= maxSelections;

          return (
            <button
              key={driver.driver_id}
              type="button"
              className={
                isSelected
                  ? "driver-filter driver-filter-selected"
                  : "driver-filter"
              }
              disabled={selectionLimitReached}
              onClick={() => handleToggle(driver.driver_code)}
            >
              <strong>{driver.driver_code}</strong>

              <span>
                {driver.full_name || driver.constructor_name || "Driver"}
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}