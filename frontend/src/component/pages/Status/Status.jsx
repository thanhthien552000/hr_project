import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import "./Status.css";
import { statusApi } from "../../../services/hrApi";
import { formatPercent } from "../../../utils/formatters";

const COLORS = ["#51cf66", "#ffd43b", "#868e96", "#4dabf7", "#9775fa", "#ff6b6b"];

const Status = () => {
  const [overview, setOverview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    const loadStatus = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await statusApi.overview();
        if (!active) return;
        setOverview(data);
      } catch (err) {
        if (active) setError(err.message || "Could not load status overview.");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadStatus();
    return () => {
      active = false;
    };
  }, []);

  const chartData = (overview?.statuses || []).map((item) => ({
    name: item.status,
    value: item.count,
    percentage: item.percentage,
  }));

  return (
    <div className="status-page">
      <h2>Status Dashboard</h2>

      {error && <div className="state-message error">{error}</div>}

      <div className="chart-card hover-card">
        <div className="status-card-header">
          <h3>Employee Status</h3>
          <span>{overview?.total_employees || 0} employees</span>
        </div>

        {loading ? (
          <div className="chart-empty">Loading status...</div>
        ) : chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={320}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                outerRadius={110}
                label={({ name, percentage }) => `${name}: ${formatPercent(percentage)}`}
                isAnimationActive
                animationDuration={1000}
              >
                {chartData.map((entry, index) => (
                  <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value, _, item) => [
                  `${value} (${formatPercent(item.payload.percentage)})`,
                  "Employees",
                ]}
              />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div className="chart-empty">No status data.</div>
        )}

        <div className="status-summary-list">
          {chartData.map((item, index) => (
            <div className="status-summary-item" key={item.name}>
              <span
                className="status-dot"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              />
              <span>{item.name}</span>
              <strong>
                {item.value} nhân viên · {formatPercent(item.percentage)}
              </strong>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Status;
