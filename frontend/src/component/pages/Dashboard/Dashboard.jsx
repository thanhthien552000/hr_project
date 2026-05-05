import { useEffect, useMemo, useState } from "react";
import "./Dashboard.css";
import SearchEmployees from "../InputSearch/Search";
import {
  Users,
  DollarSign,
  Activity,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
  CartesianGrid,
  BarChart,
  Bar,
} from "recharts";
import { dashboardApi } from "../../../services/hrApi";
import {
  currentMonthValue,
  displayText,
  employeeCode,
  formatCurrency,
  formatPercent,
} from "../../../utils/formatters";

const COLORS = [
  "#4dabf7",
  "#51cf66",
  "#fcc419",
  "#ff6b6b",
  "#9775fa",
  "#20c997",
  "#ff922b",
  "#748ffc",
  "#f06595",
  "#15aabf",
];
const itemsPerPage = 5;

const renderPayrollLabel = () => null;

const Dashboard = () => {
  const [month, setMonth] = useState(currentMonthValue());
  const [summary, setSummary] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [payrollByDepartment, setPayrollByDepartment] = useState(null);
  const [recentActivities, setRecentActivities] = useState([]);
  const [topAbsent, setTopAbsent] = useState([]);
  const [search, setSearch] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("All");
  const [sortType, setSortType] = useState("name-asc");
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;

    const loadDashboard = async () => {
      setLoading(true);
      setError("");
      try {
        const [
          summaryData,
          performanceData,
          payrollData,
          recentData,
          absentData,
        ] = await Promise.all([
          dashboardApi.getSummary({ month }),
          dashboardApi.getPerformance({ month }),
          dashboardApi.getPayrollByDepartment({ month }),
          dashboardApi.getRecentActivities({ limit: 20 }),
          dashboardApi.getTopAbsentEmployees({ month, limit: 5 }),
        ]);

        if (!active) return;
        setSummary(summaryData);
        setPerformance(performanceData);
        setPayrollByDepartment(payrollData);
        setRecentActivities(recentData.items || []);
        setTopAbsent(absentData.employees || []);
        setCurrentPage(1);
      } catch (err) {
        if (active) setError(err.message || "Could not load dashboard data.");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadDashboard();
    return () => {
      active = false;
    };
  }, [month]);

  const lineData = useMemo(() => {
    if (!performance) return [];
    return [
      { month: "Previous", value: performance.previous_performance || 0 },
      {
        month: performance.current_month || month,
        value: performance.current_performance || 0,
      },
    ];
  }, [month, performance]);

  const pieData = useMemo(() => {
    const departments = payrollByDepartment?.departments || [];
    return [...departments]
      .sort((a, b) => Number(b.total_salary || 0) - Number(a.total_salary || 0))
      .map((department) => ({
        id: department.department_id,
        name: department.department_name,
        value: Number(department.total_salary || 0),
        percentage: department.percentage,
      }));
  }, [payrollByDepartment]);

  const departmentOptions = useMemo(() => {
    const options = new Set(
      recentActivities
        .map((item) => item.department_name)
        .filter(Boolean),
    );
    return ["All", ...options];
  }, [recentActivities]);

  const filteredEmployees = recentActivities.filter((emp) => {
    const keyword = search.toLowerCase();
    const matchSearch =
      (emp.full_name || "").toLowerCase().includes(keyword) ||
      (emp.department_name || "").toLowerCase().includes(keyword);
    const matchDepartment =
      departmentFilter === "All" || emp.department_name === departmentFilter;
    return matchSearch && matchDepartment;
  });

  const sortedEmployees = [...filteredEmployees].sort((a, b) => {
    if (sortType.includes("name")) {
      return sortType === "name-asc"
        ? (a.full_name || "").localeCompare(b.full_name || "")
        : (b.full_name || "").localeCompare(a.full_name || "");
    }
    const salaryA = Number(a.net_salary || 0);
    const salaryB = Number(b.net_salary || 0);
    return sortType === "salary-asc" ? salaryA - salaryB : salaryB - salaryA;
  });

  const totalPages = Math.max(Math.ceil(sortedEmployees.length / itemsPerPage), 1);
  const paginatedEmployees = sortedEmployees.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage,
  );

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h2>Dashboard Overview</h2>
        <input
          className="date-picker"
          type="month"
          value={month}
          onChange={(e) => setMonth(e.target.value)}
        />
      </header>

      {error && <div className="state-message error">{error}</div>}

      <div className="stats-grid">
        <div className="stat-card blue">
          <div className="stat-content">
            <p>Total Employees</p>
            <h3>{loading ? "..." : summary?.total_employees || 0}</h3>
          </div>
          <Users className="stat-icon" />
        </div>
        <div className="stat-card green">
          <div className="stat-content">
            <p>Total Payroll</p>
            <h3>
              {loading
                ? "..."
                : formatCurrency(payrollByDepartment?.total_payroll)}
            </h3>
          </div>
          <DollarSign className="stat-icon" />
        </div>
        <div className="stat-card orange">
          <div className="stat-content">
            <p>Attendance Rate</p>
            <h3>{loading ? "..." : formatPercent(performance?.current_performance)}</h3>
            <span
              className={`stat-change ${performance?.change_direction === "down" ? "down" : "up"}`}
            >
              {performance?.change_direction === "down" ? "↓" : "↑"}{" "}
              {formatPercent(performance?.change_percentage)}
            </span>
          </div>
          <Activity className="stat-icon" />
        </div>
      </div>

      <div className="visuals-grid">
        <div className="chart-card main-chart">
          <h4>Performance Trend</h4>
          {lineData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart
                data={lineData}
                margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                  stroke="#eee"
                />
                <XAxis dataKey="month" axisLine={false} tickLine={false} />
                <YAxis axisLine={false} tickLine={false} />
                <Tooltip
                  formatter={(value) => formatPercent(value)}
                  contentStyle={{
                    borderRadius: "10px",
                    border: "none",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  }}
                />
                <Legend verticalAlign="top" align="right" height={36} />
                <Line
                  type="monotone"
                  dataKey="value"
                  name="Performance"
                  stroke="#4dabf7"
                  strokeWidth={3}
                  dot={{ r: 6 }}
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="chart-empty">No performance data.</div>
          )}
        </div>

        <div className="chart-card side-chart">
          <div className="chart-title-row">
            <h4>Payroll by Department</h4>
            <span>{payrollByDepartment?.month || month}</span>
          </div>
          {pieData.length > 0 ? (
            <div className="payroll-department-layout">
              <div className="payroll-pie-wrap">
                <ResponsiveContainer width="100%" height={240}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      dataKey="value"
                      nameKey="name"
                      innerRadius={70}
                      outerRadius={100}
                      paddingAngle={pieData.length > 1 ? 2 : 0}
                      label={false}
                      labelLine={false}
                    >
                      {pieData.map((item, index) => (
                        <Cell
                          key={item.id}
                          fill={COLORS[index % COLORS.length]}
                        />
                      ))}
                    </Pie>
                    <Tooltip
                      formatter={(value, _, item) => [
                        formatCurrency(value),
                        `${item.payload.name} (${formatPercent(item.payload.percentage)})`,
                      ]}
                    />
                  </PieChart>
                </ResponsiveContainer>
                <div className="payroll-pie-center">
                  <span>TOTAL</span>
                  <strong>
                    {formatCurrency(payrollByDepartment?.total_payroll)}
                  </strong>
                </div>
              </div>

              <div className="payroll-breakdown">
                {pieData.map((department, index) => (
                  <div className="payroll-breakdown-row" key={department.id}>
                    <span
                      className="payroll-color"
                      style={{ backgroundColor: COLORS[index % COLORS.length] }}
                    />
                    <div>
                      <strong>{department.name}</strong>
                      <span>{formatCurrency(department.value)}</span>
                    </div>
                    <em>{formatPercent(department.percentage)}</em>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="chart-empty">No payroll data.</div>
          )}
        </div>
      </div>

      <div className="chart-card top-absent-card">
        <h4>Top Absent Employees</h4>
        {topAbsent.length > 0 ? (
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={topAbsent}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="full_name" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              <Bar dataKey="absent_days" name="Absent days" fill="#ff6b6b" />
              <Bar dataKey="leave_days" name="Leave days" fill="#fcc419" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="chart-empty">No absence data.</div>
        )}
      </div>

      <div className="table-section">
        <div className="table-controls">
          <div className="left-controls">
            <h3>Recent Activities</h3>
            <SearchEmployees
              onSearch={(value) => {
                setSearch(value);
                setCurrentPage(1);
              }}
            />
          </div>
          <div className="right-controls">
            <select
              value={departmentFilter}
              onChange={(e) => {
                setDepartmentFilter(e.target.value);
                setCurrentPage(1);
              }}
              className="modern-select"
            >
              {departmentOptions.map((department) => (
                <option key={department} value={department}>
                  {department === "All" ? "All Departments" : department}
                </option>
              ))}
            </select>

            <select
              value={sortType}
              onChange={(e) => setSortType(e.target.value)}
              className="modern-select"
            >
              <option value="name-asc">Name A-Z</option>
              <option value="name-desc">Name Z-A</option>
              <option value="salary-asc">Salary Low-High</option>
              <option value="salary-desc">Salary High-Low</option>
            </select>
          </div>
        </div>

        <div className="table-wrapper">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Employee</th>
                <th>ID</th>
                <th>Department</th>
                <th>Net Salary</th>
                <th>Last Activity</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="5" className="table-state">
                    Loading activities...
                  </td>
                </tr>
              ) : paginatedEmployees.length > 0 ? (
                paginatedEmployees.map((emp) => (
                  <tr key={emp.employee_id}>
                    <td className="emp-name">{emp.full_name}</td>
                    <td>{employeeCode(emp.employee_id)}</td>
                    <td>{displayText(emp.department_name)}</td>
                    <td className="salary-cell">{formatCurrency(emp.net_salary)}</td>
                    <td>{displayText(emp.last_activity_date)}</td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="table-state">
                    No recent activities found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="pagination-container">
          <p>
            Showing {paginatedEmployees.length} of {sortedEmployees.length}{" "}
            employees
          </p>
          <div className="pagination-buttons">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage((prev) => prev - 1)}
              className="p-btn"
              type="button"
            >
              <ChevronLeft size={18} />
            </button>

            <button className="p-btn active" type="button">
              {currentPage}
            </button>

            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage((prev) => prev + 1)}
              className="p-btn"
              type="button"
            >
              <ChevronRight size={18} />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
