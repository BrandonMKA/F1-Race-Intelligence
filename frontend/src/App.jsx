import { useEffect, useMemo, useState } from "react";

import { getEvents } from "./api/f1Api";
import ConstructorTable from "./components/ConstructorTable";
import EventHeader from "./components/EventHeader";
import EventSelector from "./components/EventSelector";
import FastestLapsTable from "./components/FastestLapsTable";
import LoadingState from "./components/LoadingState";
import PositionGainsTable from "./components/PositionGainsTable";
import ResultsTable from "./components/ResultsTable";
import StintsTable from "./components/StintsTable";
import { useEventData } from "./hooks/useEventData";
import DriverSelector from "./components/DriverSelector";
import LapTimeChart from "./components/LapTimeChart";
import PositionGainChart from "./components/PositionGainChart";
import RacePositionChart from "./components/RacePositionChart";
import StintStrategyChart from "./components/StintStrategyChart";

import "./App.css";

function App() {
  const [events, setEvents] = useState([]);
  const [selectedEventId, setSelectedEventId] = useState("");
  const [selectedDriverCodes, setSelectedDriverCodes] = useState([]);
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

  return (
    <div className="app-shell">
      <header className="site-header">
        <div>
          <p className="brand-kicker">Data Engineering Portfolio</p>
          <h1>F1 Race Intelligence</h1>
        </div>

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
              <p>
                Run the ETL pipeline to add an event to PostgreSQL.
              </p>
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
            <DriverSelector
              drivers={availableDrivers}
              selectedDriverCodes={selectedDriverCodes}
              onToggle={toggleDriver}
            />

            <div className="dashboard-grid">
              <LapTimeChart
                laps={laps}
                selectedDriverCodes={selectedDriverCodes}
              />

              <RacePositionChart
                laps={laps}
                selectedDriverCodes={selectedDriverCodes}
              />

              <StintStrategyChart
                stints={stints}
                selectedDriverCodes={selectedDriverCodes}
              />

              <PositionGainChart drivers={positionGains} />

              <ConstructorTable constructors={constructors} />

              <ResultsTable results={results} />

              <FastestLapsTable laps={fastestLaps} />

              <PositionGainsTable drivers={positionGains} />

              <StintsTable stints={stints} />
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;