import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, RefreshCw } from "lucide-react";
import "./Alerts.css";
import { alertsApi } from "../../../services/hrApi";
import { currentMonthValue, displayText, employeeCode } from "../../../utils/formatters";

const pageSize = 10;

const ALERT_TYPES = [
  { value: "", label: "All" },
  { value: "excessive_absence", label: "Excessive absence" },
  { value: "salary_change", label: "Salary change" },
  { value: "salary_anomaly", label: "Salary anomaly" },
];

const READ_FILTERS = [
  { value: "", label: "All statuses" },
  { value: "false", label: "Unread" },
  { value: "true", label: "Read" },
];

const typeLabel = (value) =>
  ALERT_TYPES.find((item) => item.value === value)?.label || value;

const getLevelClass = (severity) => {
  if (severity === "high") return "alert high";
  if (severity === "warning") return "alert medium";
  return "alert low";
};

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    total_pages: 1,
  });
  const [alertType, setAlertType] = useState("");
  const [readFilter, setReadFilter] = useState("");
  const [month, setMonth] = useState(currentMonthValue());
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let active = true;

    const loadAlerts = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await alertsApi.list({
          page: currentPage,
          page_size: pageSize,
          alert_type: alertType,
          is_read: readFilter === "" ? "" : readFilter === "true",
        });

        if (!active) return;
        setAlerts(data.items || []);
        setPagination({
          total: data.total || 0,
          page: data.page || currentPage,
          total_pages: data.total_pages || 1,
        });
      } catch (err) {
        if (active) setError(err.message || "Could not load alerts.");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadAlerts();
    return () => {
      active = false;
    };
  }, [alertType, currentPage, readFilter, reloadKey]);

  const handleGenerateAlerts = async () => {
    setGenerating(true);
    setNotice("");
    setError("");
    try {
      const result = await alertsApi.generate({ month });
      setNotice(
        `${result.alerts_generated || 0} alerts generated for ${result.month}.`,
      );
      setCurrentPage(1);
      setReloadKey((key) => key + 1);
    } catch (err) {
      setError(err.message || "Could not generate alerts.");
    } finally {
      setGenerating(false);
    }
  };

  const totalPages = Math.max(pagination.total_pages || 1, 1);

  return (
    <div className="alerts-page">
      <h2>Warning Dashboard</h2>

      <div className="filter-bar">
        <select
          value={alertType}
          onChange={(e) => {
            setAlertType(e.target.value);
            setCurrentPage(1);
          }}
        >
          {ALERT_TYPES.map((option) => (
            <option key={option.label} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <select
          value={readFilter}
          onChange={(e) => {
            setReadFilter(e.target.value);
            setCurrentPage(1);
          }}
        >
          {READ_FILTERS.map((option) => (
            <option key={option.label} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <input
          type="month"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        />
        <button
          className="btn btn-add"
          type="button"
          onClick={handleGenerateAlerts}
          disabled={generating}
        >
          <RefreshCw size={18} /> {generating ? "Generating..." : "Generate"}
        </button>
      </div>

      {notice && <div className="state-message success">{notice}</div>}
      {error && <div className="state-message error">{error}</div>}

      <div className="alert-list">
        {loading ? (
          <div className="table-state">Loading alerts...</div>
        ) : alerts.length > 0 ? (
          alerts.map((item) => (
            <div key={item.id} className={getLevelClass(item.severity)}>
              <span className="icon">!</span>
              <div className="alert-content">
                <p>{item.message}</p>
                <span>
                  {typeLabel(item.alert_type)} ·{" "}
                  {displayText(item.employee_name)} ({employeeCode(item.employee_id)})
                </span>
              </div>
              <span className="read-state">{item.is_read ? "Read" : "Unread"}</span>
            </div>
          ))
        ) : (
          <div className="table-state">No alerts found.</div>
        )}
      </div>

      <div className="pagination-container">
        <p>
          Page {pagination.page} of {totalPages} · {pagination.total} alerts
        </p>
        <div className="pagination-buttons">
          <button
            disabled={currentPage === 1 || loading}
            onClick={() => setCurrentPage((page) => page - 1)}
            className="p-btn"
            type="button"
          >
            <ChevronLeft size={18} />
          </button>
          <button className="p-btn active" type="button">
            {currentPage}
          </button>
          <button
            disabled={currentPage >= totalPages || loading}
            onClick={() => setCurrentPage((page) => page + 1)}
            className="p-btn"
            type="button"
          >
            <ChevronRight size={18} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Alerts;
