const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`);
  } catch {
    throw new Error(
      "The race data service is currently unavailable. Please try again shortly."
    );
  }

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const errorBody = await response.json();

      if (errorBody.detail) {
        message = errorBody.detail;
      }
    } catch {
      // Keep the fallback message when the API has no JSON body.
    }

    throw new Error(message);
  }

  return response.json();
}

export function getEvents() {
  return request("/api/events");
}

export function getEvent(eventId) {
  return request(`/api/events/${eventId}`);
}

export function getResults(eventId) {
  return request(`/api/events/${eventId}/results`);
}

export function getFastestLaps(eventId) {
  return request(
    `/api/analytics/events/${eventId}/fastest-laps?limit=20`
  );
}

export function getPositionGains(eventId) {
  return request(
    `/api/analytics/events/${eventId}/position-gains`
  );
}

export function getConstructors(eventId) {
  return request(
    `/api/analytics/events/${eventId}/constructors`
  );
}

export function getStints(eventId) {
  return request(`/api/analytics/events/${eventId}/stints`);
}

export function getLaps(eventId) {
  return request(`/api/events/${eventId}/laps?limit=5000`);
}