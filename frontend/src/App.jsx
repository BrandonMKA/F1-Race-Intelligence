import { useEffect, useMemo, useState } from "react";

import { getEvents } from "./api/f1Api";
import ConstructorTable from "./components/ConstructorTable";
import DriverSelector from "./components/DriverSelector";
import EventHeader from "./components/EventHeader";
import EventSelector from "./components/EventSelector";
import FastestLapsTable from "./components/FastestLapsTable";
import LapTimeChart from "./components/LapTimeChart";
import LoadingState from "./components/LoadingState";
import PositionGainChart from "./components/PositionGainChart";
import PositionGainsTable from "./components/PositionGainsTable";
import RacePositionChart from "./components/RacePositionChart";
import ResultsTable from "./components/ResultsTable";
import StintStrategyChart from "./components/StintStrategyChart";
import StintsTable from "./components/StintsTable";
import { useEventData } from "./hooks/useEventData";

import "./App.css";

const detailTabs = [
  { id: "results", label: "Results" },
  { id: "fastest", label: "Fastest laps" },
  { id: "constructors", label: "Constructors" },
  { id: "movement", label: "Position change" },
  { id: "stints", label: "Stints" },
];

function App() {
  const [events, setEvents] = useState([]);
  const [selectedEventId, setSelectedEventId] = useState("");
  const [selectedDriverCodes, setSelectedDriverCodes] = useState([]);
  const [activeTab, setActiveTab] = useState("results");
  const [eventsLoading, setEventsLoading] = useState(true);
  const [eventsError, setEventsError] = useState("");

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
  } = useEventData(selectedEventId);

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

  const raceWinner = results.find(
    (result) => Number(result.finish_position) === 1
  );

  const fastestDriver = fastestLaps[0];

  const biggestMover = positionGains
    .filter((driver) => driver.positions_gained !== null)
    .sort(
      (first, second) =>
        Number(second.positions_gained) -
        Number(first.positions_gained)
    )[0];

  useEffect(() => {
    async function loadEvents() {
      try {
        const eventData = await getEvents();

        setEvents(eventData);

        if (eventData.length > 0) {
          setSelectedEventId(String(eventData[0].event_id));
        }
      } catch (requestError) {
        setEventsError(
          requestError instanceof Error
            ? requestError.message
            : "Unable to load events."
        );
      } finally {
        setEventsLoading(false);
      }
    }

    loadEvents();
  }, []);

  useEffect(() => {
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
  }, [selectedEventId, results]);

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

  return (
    <div className="app-shell">
      <header className="site-header">
        <a href="/" className="brand-mark">
          <span className="brand-icon">F1</span>

          <span>
            <strong>Race Intelligence</strong>
            <small>Data Engineering Project</small>
          </span>
        </a>

        <EventSelector
          events={events}
          selectedEventId={selectedEventId}
          onChange={setSelectedEventId}
          disabled={eventsLoading}
        />
      </header>

      <main>
        {eventsError && (
          <div className="error-panel" role="alert">
            <strong>Unable to load races</strong>
            <p>{eventsError}</p>
          </div>
        )}

        {!eventsError && eventsLoading && <LoadingState />}

        {!eventsLoading &&
          !eventsError &&
          events.length === 0 && (
            <div className="empty-panel">
              <h2>No races have been loaded</h2>
              <p>Run the ETL pipeline to add a race to PostgreSQL.</p>
            </div>
          )}

        {isLoading && <LoadingState />}

        {error && (
          <div className="error-panel" role="alert">
            <strong>Unable to load race data</strong>
            <p>{error}</p>
          </div>
        )}

        {!isLoading && !error && event && (
          <>
            <EventHeader event={event} />

            <section className="summary-grid">
              <article className="summary-card">
                <span>Race winner</span>
                <strong>{raceWinner?.driver_code ?? "—"}</strong>
                <p>
                  {raceWinner?.full_name ??
                    "No classification available"}
                </p>
              </article>

              <article className="summary-card">
                <span>Fastest lap</span>
                <strong>{fastestDriver?.driver_code ?? "—"}</strong>
                <p>
                  Lap {fastestDriver?.lap_number ?? "—"}
                </p>
              </article>

              <article className="summary-card">
                <span>Biggest mover</span>
                <strong>{biggestMover?.driver_code ?? "—"}</strong>
                <p>
                  {biggestMover?.positions_gained > 0
                    ? `+${biggestMover.positions_gained} positions`
                    : "No gain recorded"}
                </p>
              </article>

              <article className="summary-card">
                <span>Total race laps</span>
                <strong>
                  {Number(event.lap_count ?? 0).toLocaleString()}
                </strong>
                <p>Driver-lap records</p>
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
                  Compare lap performance, track position, and tire
                  strategy throughout the race.
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

              <div className="detail-tabs" role="tablist">
                {detailTabs.map((tab) => (
                  <button
                    key={tab.id}
                    type="button"
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

              <div className="detail-content">
                {renderActiveTable()}
              </div>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

export default App;