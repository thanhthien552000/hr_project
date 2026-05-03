import { NavLink, useNavigate } from "react-router-dom";
import "../Slidebar/slide.css";

const Sidebar = () => {
  const navigate = useNavigate();

  return (
    <div className="sidebar">
      <h2 className="logo" onClick={() => navigate("/")}>
        PeopleX
      </h2>

      <ul>
        <li>
          <NavLink to="/" end>
            <i className="fas fa-chart-line"></i> Dashboard
          </NavLink>
        </li>

        <li>
          <NavLink to="/employees">
            <i className="fas fa-users"></i> Employee
          </NavLink>
        </li>

        <li>
          <NavLink to="/payroll">
            <i className="fas fa-money-bill-wave"></i> Payroll
          </NavLink>
        </li>

        <li>
          <NavLink to="/attendance">
            <i className="fas fa-clock"></i> Attendance
          </NavLink>
        </li>

        <li>
          <NavLink to="/status">
            <i className="fas fa-chart-bar"></i> Status
          </NavLink>
        </li>

        <li>
          <NavLink to="/alerts">
            <i className="fas fa-bell"></i> Alerts
          </NavLink>
        </li>
      </ul>
    </div>
  );
};

export default Sidebar;
