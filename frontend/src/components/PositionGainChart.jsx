import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { formatPositionChange } from "../utils/formatters";

function getBarColor(value) {
  if (value > 0) {
    return "#59c173";
  }

  if (value < 0) {
    return "#ef6a6a";
  }

  return "#98a2b3";
}

export default function PositionGainChart({ drivers }) {
  const chartData = drivers
    .filter(
      (driver) =>
        driver.positions_gained !== null &&
        driver.positions_gained !== undefined
    )
    .map((driver) => ({
      driverCode: driver.driver_code,
      positionsGained: Number(driver.positions_gained),
    }));

  return (
    <section className="data-panel chart-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Movement</p>
          <h3>Positions gained and lost</h3>
        </div>
      </div>

      <div className="chart-container chart-container-tall">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{
              top: 10,
              right: 35,
              bottom: 10,
              left: 5,
            }}
          >
            <CartesianGrid
              stroke="rgba(255, 255, 255, 0.08)"
              horizontal={false}
            />

            <XAxis
              type="number"
              tickLine={false}
              axisLine={false}
            />

            <YAxis
              type="category"
              dataKey="driverCode"
              tickLine={false}
              axisLine={false}
              width={42}
            />

            <Tooltip
              formatter={(value) => [
                formatPositionChange(value),
                "Position change",
              ]}
            />

            <Bar
              dataKey="positionsGained"
              radius={[0, 4, 4, 0]}
            >
              {chartData.map((entry) => (
                <Cell
                  key={entry.driverCode}
                  fill={getBarColor(entry.positionsGained)}
                />
              ))}

              <LabelList
                dataKey="positionsGained"
                position="right"
                formatter={formatPositionChange}
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}