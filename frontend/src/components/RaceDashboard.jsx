import { useEffect, useMemo, useState } from "react";

import ConstructorTable from "./ConstructorTable";
import DriverSelector from "./DriverSelector";
import EventHeader from "./EventHeader";
import FastestLapsTable from "./FastestLapsTable";
import LapTimeChart from "./LapTimeChart";
import LoadingState from "./LoadingState";
import PositionGainChart from "./PositionGainChart";
import PositionGainsTable from "./PositionGainsTable";
import RacePositionChart from "./RacePositionChart";
import ResultsTable from "./ResultsTable";
import StintStrategyChart from "./StintStrategyChart";
import StintsTable from "./StintsTable";
import { useEventData } from "../hooks/useEventData";

const detailTabs = [
  { id: "results", label: "Results" },
  { id: "fastest", label: "Fastest laps" },
  { id: "constructors", label: "Constructors" },
  { id: "movement", label: "Position change" },
  { id: "stints", label: "Stints" },
];

function RaceDashboard({ eventId }) {
  const [selectedDriverCodes, setSelectedDriverCodes] = useState([]);
  const [activeTab, setActiveTab] = useState("results");

  const {
    event,
    results,
    laps,
    fastestLaps,
    positionGains,
    constructors,
    stints,
    isLoading,
    error,
  } = useEventData(eventId);

  const availableDrivers = useMemo(
    () =>
      results
        .filter((result) => result.driver_code)
        .map((result) => ({
          driver_id: result.driver_id,
          driver_code: result.driver_code,
          full_name: result.full_name,
          constructor_name: result.constructor_name,
        })),
    [results]
  );

  const raceWinner = useMemo(
    () =>
      results.find((result) => Number(result.finish_position) === 1),
    [results]
  );

  const fastestDriver = fastestLaps[0];

  const biggestMover = useMemo(
    () =>
      [...positionGains]
        .filter(
          (driver) =>
            driver.positions_gained !== null &&
            driver.positions_gained !== undefined
        )
        .sort(
          (first, second) =>
            Number(second.positions_gained) -
            Number(first.positions_gained)
        )[0],
    [positionGains]
  );

  useEffect(() => {
    setActiveTab("results");

    if (results.length === 0) {
      setSelectedDriverCodes([]);
      return;
    }

    setSelectedDriverCodes(
      results
        .filter((result) => result.driver_code)
        .slice(0, 2)
        .map((result) => result.driver_code)
    );
  }, [eventId, results]);

  function toggleDriver(driverCode) {
    setSelectedDriverCodes((current) => {
      if (current.includes(driverCode)) {
        return current.filter((code) => code !== driverCode);
      }

      if (current.length >= 4) {
        return current;
      }

      return [...current, driverCode];
    });
  }

  function renderActiveTable() {
    switch (activeTab) {
      case "fastest":
        return <FastestLapsTable laps={fastestLaps} />;
      case "constructors":
        return <ConstructorTable constructors={constructors} />;
      case "movement":
        return <PositionGainsTable drivers={positionGains} />;
      case "stints":
        return <StintsTable stints={stints} />;
      default:
        return <ResultsTable results={results} />;
    }
  }

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return (
      <div className="error-panel" role="alert">
        <strong>Unable to load race data</strong>
        <p>{error}</p>
      </div>
    );
  }

  if (!event) {
    return null;
  }

  return (
    <>
      <EventHeader event={event} />

      <section className="summary-grid">
        <article className="summary-card">
          <span>Race winner</span>
          <strong>{raceWinner?.driver_code ?? "—"}</strong>
          <p>{raceWinner?.full_name ?? "No classification available"}</p>
        </article>

        <article className="summary-card">
          <span>Fastest lap</span>
          <strong>{fastestDriver?.driver_code ?? "—"}</strong>
          <p>
            {fastestDriver
              ? `Lap ${fastestDriver.lap_number}`
              : "No fastest lap available"}
          </p>
        </article>

        <article className="summary-card">
          <span>Biggest mover</span>
          <strong>{biggestMover?.driver_code ?? "—"}</strong>
          <p>
            {Number(biggestMover?.positions_gained) > 0
              ? `+${biggestMover.positions_gained} positions`
              : "No gain recorded"}
          </p>
        </article>

        <article className="summary-card">
          <span>Total race laps</span>
          <strong>{Number(event.lap_count ?? 0).toLocaleString()}</strong>
          <p>Race distance</p>
        </article>
      </section>

      <DriverSelector
        drivers={availableDrivers}
        selectedDriverCodes={selectedDriverCodes}
        onToggle={toggleDriver}
      />

      <section className="analysis-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Driver comparison</p>
            <h2>Race pace analysis</h2>
          </div>
          <p>
            Compare lap performance, track position, and tire strategy
            throughout the race.
          </p>
        </div>

        <LapTimeChart
          laps={laps}
          selectedDriverCodes={selectedDriverCodes}
        />

        <div className="chart-split">
          <RacePositionChart
            laps={laps}
            selectedDriverCodes={selectedDriverCodes}
          />
          <StintStrategyChart
            stints={stints}
            selectedDriverCodes={selectedDriverCodes}
          />
        </div>

        <PositionGainChart drivers={positionGains} />
      </section>

      <section className="details-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Race data</p>
            <h2>Detailed classification</h2>
          </div>
        </div>

        <div
          className="detail-tabs"
          role="tablist"
          aria-label="Race data tables"
        >
          {detailTabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              role="tab"
              aria-selected={activeTab === tab.id}
              className={
                activeTab === tab.id
                  ? "detail-tab detail-tab-active"
                  : "detail-tab"
              }
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="detail-content">{renderActiveTable()}</div>
      </section>
    </>
  );
}

export default RaceDashboard;
