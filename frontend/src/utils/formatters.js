export function formatLapTime(milliseconds) {
  const numericValue = Number(milliseconds);

  if (!Number.isFinite(numericValue)) {
    return "—";
  }

  const totalSeconds = numericValue / 1000;
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return `${minutes}:${seconds.toFixed(3).padStart(6, "0")}`;
}

export function formatDelta(milliseconds) {
  const numericValue = Number(milliseconds);

  if (!Number.isFinite(numericValue)) {
    return "—";
  }

  const seconds = numericValue / 1000;
  const prefix = seconds > 0 ? "+" : "";

  return `${prefix}${seconds.toFixed(3)}s`;
}

export function formatPositionChange(value) {
  const numericValue = Number(value);

  if (!Number.isFinite(numericValue)) {
    return "—";
  }

  return numericValue > 0
    ? `+${numericValue}`
    : String(numericValue);
}