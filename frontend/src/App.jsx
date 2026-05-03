import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./component/Slidebar/Slide";
import "@fortawesome/fontawesome-free/css/all.min.css";
import Dashboard from "./component/pages/Dashboard/Dashboard";
import Employees from "./component/pages/Employees/Employees";
import Payroll from "./component/pages/Payroll/Payroll";
import Attendance from "./component/pages/Attendence/Attendance";
import Status from "./component/pages/Status/Status";
import Alerts from "./component/pages/Alerts/Alerts";

function App() {
  return (
    <Router>
      <div style={{ display: "flex" }}>
        <Sidebar />

        {/* Nội dung bên phải */}
        <div
          style={{
            width: "100%",
            padding: "0",
            backgroundColor: "#f0f2f5",
            marginLeft: "17%",
          }}
        >
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employees" element={<Employees />} />
            <Route path="/payroll" element={<Payroll />} />
            <Route path="/attendance" element={<Attendance />} />
            <Route path="/status" element={<Status />} />
            <Route path="/alerts" element={<Alerts />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
