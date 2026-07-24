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

const chartColors = [
  "#e10600",
  "#38bdf8",
  "#facc15",
  "#a78bfa",
];

function buildPositionData(laps, selectedDriverCodes) {
  const positionsByLap = new Map();

  for (const lap of laps) {
    if (!selectedDriverCodes.includes(lap.driver_code)) {
      continue;
    }

    const position = Number(lap.position);
    const lapNumber = Number(lap.lap_number);

    if (
      !Number.isFinite(position) ||
      !Number.isFinite(lapNumber)
    ) {
      continue;
    }

    if (!positionsByLap.has(lapNumber)) {
      positionsByLap.set(lapNumber, {
        lapNumber,
      });
    }

    positionsByLap.get(lapNumber)[lap.driver_code] = position;
  }

  return [...positionsByLap.values()].sort(
    (first, second) => first.lapNumber - second.lapNumber
  );
}

export default function RacePositionChart({
  laps,
  selectedDriverCodes,
}) {
  const chartData = useMemo(
    () => buildPositionData(laps, selectedDriverCodes),
    [laps, selectedDriverCodes]
  );

  return (
    <section className="data-panel chart-panel data-panel-wide">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Track position</p>
          <h3>Race-position progression</h3>
        </div>
      </div>

      {selectedDriverCodes.length === 0 ? (
        <div className="chart-empty-state">
          Select at least one driver to view race positions.
        </div>
      ) : (
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart
              data={chartData}
              margin={{
                top: 15,
                right: 20,
                left: 5,
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
              />

              <YAxis
                reversed
                domain={[1, 20]}
                allowDecimals={false}
                tickLine={false}
                axisLine={false}
                width={36}
              />

              <Tooltip
                labelFormatter={(lapNumber) => `Lap ${lapNumber}`}
                formatter={(value, name) => [
                  `P${value}`,
                  name,
                ]}
              />

              <Legend />

              {selectedDriverCodes.map((driverCode, index) => (
                <Line
                  key={driverCode}
                  type="linear"
                  dataKey={driverCode}
                  stroke={chartColors[index % chartColors.length]}
                  strokeWidth={2}
                  dot={false}
                  connectNulls
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