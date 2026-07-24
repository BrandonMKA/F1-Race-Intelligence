import { useMemo } from "react";

const compoundClassNames = {
  SOFT: "compound-soft",
  MEDIUM: "compound-medium",
  HARD: "compound-hard",
  INTERMEDIATE: "compound-intermediate",
  WET: "compound-wet",
  UNKNOWN: "compound-unknown",
};

function getCompoundClass(compound) {
  const normalizedCompound =
    compound?.toUpperCase() || "UNKNOWN";

  return (
    compoundClassNames[normalizedCompound] ||
    compoundClassNames.UNKNOWN
  );
}

export default function StintStrategyChart({
  stints,
  selectedDriverCodes,
}) {
  const filteredStints = useMemo(
    () =>
      stints.filter((stint) =>
        selectedDriverCodes.includes(stint.driver_code)
      ),
    [stints, selectedDriverCodes]
  );

  const stintsByDriver = useMemo(() => {
    const groupedStints = new Map();

    for (const stint of filteredStints) {
      if (!groupedStints.has(stint.driver_code)) {
        groupedStints.set(stint.driver_code, []);
      }

      groupedStints.get(stint.driver_code).push(stint);
    }

    for (const driverStints of groupedStints.values()) {
      driverStints.sort(
        (first, second) =>
          first.stint_number - second.stint_number
      );
    }

    return groupedStints;
  }, [filteredStints]);

  return (
    <section className="data-panel data-panel-wide">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Strategy comparison</p>
          <h3>Tire-stint timeline</h3>
        </div>
      </div>

      {selectedDriverCodes.length === 0 ? (
        <div className="chart-empty-state">
          Select drivers to compare their tire strategies.
        </div>
      ) : (
        <div className="stint-chart">
          {selectedDriverCodes.map((driverCode) => {
            const driverStints =
              stintsByDriver.get(driverCode) || [];

            const totalLaps = driverStints.reduce(
              (maximum, stint) =>
                Math.max(maximum, Number(stint.last_lap)),
              0
            );

            return (
              <div className="stint-driver-row" key={driverCode}>
                <strong className="stint-driver-code">
                  {driverCode}
                </strong>

                <div className="stint-track">
                  {driverStints.map((stint) => {
                    const lapCount = Number(stint.lap_count);
                    const width =
                      totalLaps > 0
                        ? `${(lapCount / totalLaps) * 100}%`
                        : "0%";

                    return (
                      <div
                        key={`${driverCode}-${stint.stint_number}`}
                        className={`stint-segment ${getCompoundClass(
                          stint.compound
                        )}`}
                        style={{ width }}
                        title={`${stint.compound || "Unknown"}: laps ${
                          stint.first_lap
                        }–${stint.last_lap}`}
                      >
                        <span>
                          {stint.compound?.slice(0, 1) || "?"}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}