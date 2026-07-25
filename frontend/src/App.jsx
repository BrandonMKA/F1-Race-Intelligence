import { useEffect, useState } from "react";
import { Navigate, Route, Routes } from "react-router-dom";

import { getEvents } from "./api/f1Api";
import LoadingState from "./components/LoadingState";
import SiteHeader from "./components/SiteHeader";
import HomePage from "./pages/HomePage";
import RacePage from "./pages/RacePage";
import SeasonPage from "./pages/SeasonPage";

import "./App.css";

function getInitialTheme() {
  const savedTheme = window.localStorage.getItem("f1-theme");

  if (savedTheme === "light" || savedTheme === "dark") {
    return savedTheme;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function App() {
  const [events, setEvents] = useState([]);
  const [eventsLoading, setEventsLoading] = useState(true);
  const [eventsError, setEventsError] = useState("");
  const [theme, setTheme] = useState(getInitialTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    window.localStorage.setItem("f1-theme", theme);
  }, [theme]);

  useEffect(() => {
    async function loadEvents() {
      try {
        setEventsLoading(true);
        setEventsError("");

        const eventData = await getEvents();
        setEvents(Array.isArray(eventData) ? eventData : []);
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

  function toggleTheme() {
    setTheme((currentTheme) =>
      currentTheme === "dark" ? "light" : "dark"
    );
  }

  return (
    <div className="app-shell">
      <SiteHeader theme={theme} onToggleTheme={toggleTheme} />

      {eventsError && (
        <div className="error-panel" role="alert">
          <strong>Unable to load races</strong>
          <p>{eventsError}</p>
        </div>
      )}

      {!eventsError && eventsLoading && <LoadingState />}

      {!eventsLoading && !eventsError && events.length === 0 && (
        <div className="empty-panel">
          <h2>No races have been loaded</h2>
          <p>Run the ETL pipeline to add race data to PostgreSQL.</p>
        </div>
      )}

      {!eventsLoading && !eventsError && events.length > 0 && (
        <Routes>
          <Route path="/" element={<HomePage events={events} />} />
          <Route
            path="/seasons/:season"
            element={<SeasonPage events={events} />}
          />
          <Route
            path="/seasons/:season/races/:eventId"
            element={<RacePage events={events} />}
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      )}
    </div>
  );
}

export default App;
