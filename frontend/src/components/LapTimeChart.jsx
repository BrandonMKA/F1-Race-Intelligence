import { useMemo } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { formatLapTime } from "../utils/formatters";

const chartColors = [
  "#e10600",
  "#38bdf8",
  "#facc15",
  "#a78bfa",
];

function buildLapChartData(laps, selectedDriverCodes) {
  const lapsByNumber = new Map();

  for (const lap of laps) {
    if (!selectedDriverCodes.includes(lap.driver_code)) {
      continue;
    }

    const lapTime = Number(lap.lap_time_ms);

    if (!Number.isFinite(lapTime)) {
      continue;
    }

    if (lap.pit_in || lap.pit_out) {
      continue;
    }

    const lapNumber = Number(lap.lap_number);

    if (!lapsByNumber.has(lapNumber)) {
      lapsByNumber.set(lapNumber, {
        lapNumber,
      });
    }

    lapsByNumber.get(lapNumber)[lap.driver_code] = lapTime;
  }

  return [...lapsByNumber.values()].sort(
    (first, second) => first.lapNumber - second.lapNumber
  );
}

function LapTimeTooltip({ active, payload, label }) {
  if (!active || !payload?.length) {
    return null;
  }

  return (
    <div className="chart-tooltip">
      <strong>Lap {label}</strong>

      {payload.map((entry) => (
        <div key={entry.dataKey} className="tooltip-row">
          <span>{entry.dataKey}</span>
          <span>{formatLapTime(entry.value)}</span>
        </div>
      ))}
    </div>
  );
}

export default function LapTimeChart({
  laps,
  selectedDriverCodes,
}) {
  const chartData = useMemo(
    () => buildLapChartData(laps, selectedDriverCodes),
    [laps, selectedDriverCodes]
  );

  return (
    <section className="data-panel chart-panel data-panel-wide">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Race pace</p>
          <h3>Lap-time comparison</h3>
        </div>
      </div>

      {selectedDriverCodes.length === 0 ? (
        <div className="chart-empty-state">
          Select at least one driver to view lap times.
        </div>
      ) : (
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{
                top: 15,
                right: 20,
                left: 20,
                bottom: 5,
              }}
            >
              <CartesianGrid
                stroke="rgba(255, 255, 255, 0.08)"
                vertical={false}
              />

              <XAxis
                dataKey="lapNumber"
                tickLine={false}
                axisLine={false}
                label={{
                  value: "Lap",
                  position: "insideBottom",
                  offset: -2,
                }}
              />

              <YAxis
                tickFormatter={formatLapTime}
                tickLine={false}
                axisLine={false}
                width={78}
                domain={["auto", "auto"]}
              />

              <Tooltip content={<LapTimeTooltip />} />
              <Legend />

              {selectedDriverCodes.map((driverCode, index) => (
                <Line
                  key={driverCode}
                  type="monotone"
                  dataKey={driverCode}
                  stroke={chartColors[index % chartColors.length]}
                  strokeWidth={2}
                  dot={false}
                  connectNulls={false}
                  isAnimationActive={false}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </section>
  );
}