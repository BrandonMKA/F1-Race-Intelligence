import { useEffect, useState } from "react";

import {
  getConstructors,
  getEvent,
  getFastestLaps,
  getPositionGains,
  getResults,
  getStints,
} from "../api/f1Api";

const initialData = {
  event: null,
  results: [],
  fastestLaps: [],
  positionGains: [],
  constructors: [],
  stints: [],
};

export function useEventData(eventId) {
  const [data, setData] = useState(initialData);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!eventId) {
      setData(initialData);
      return;
    }

    const controller = new AbortController();

    async function loadEventData() {
      setIsLoading(true);
      setError("");

      try {
        const [
          event,
          results,
          fastestLaps,
          positionGains,
          constructors,
          stints,
        ] = await Promise.all([
          getEvent(eventId),
          getResults(eventId),
          getFastestLaps(eventId),
          getPositionGains(eventId),
          getConstructors(eventId),
          getStints(eventId),
        ]);

        if (!controller.signal.aborted) {
          setData({
            event,
            results,
            fastestLaps,
            positionGains,
            constructors,
            stints,
          });
        }
      } catch (requestError) {
        if (!controller.signal.aborted) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : "Unable to load event data."
          );
        }
      } finally {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      }
    }

    loadEventData();

    return () => {
      controller.abort();
    };
  }, [eventId]);

  return {
    ...data,
    isLoading,
    error,
  };
}