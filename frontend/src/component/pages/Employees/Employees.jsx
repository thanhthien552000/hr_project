import { useEffect, useState } from "react";
import "./Employees.css";
import SearchEmployees from "../InputSearch/Search";
import { Plus, Edit2, Trash2, FileText, ChevronLeft, ChevronRight } from "lucide-react";
import EditEmployeeModal from "../EditRemove/Edit";
import AddEmployee from "../AddEmployee_PDF/AddEmployee";
import {
  departmentsApi,
  employeesApi,
  positionsApi,
} from "../../../services/hrApi";
import { displayText, employeeCode } from "../../../utils/formatters";
import {
  EMPLOYEE_STATUSES,
  normalizeEmployeeStatus,
} from "../../../utils/employeeStatus";

const STATUS_OPTIONS = [
  { value: "", label: "All statuses" },
  ...EMPLOYEE_STATUSES.map((status) => ({ value: status, label: status })),
];

const normalizeEmployeePayload = (payload) => ({
  ...payload,
  gender: payload.gender || null,
  phone_number: payload.phone_number || null,
  email: payload.email || null,
  department_id: payload.department_id || null,
  position_id: payload.position_id || null,
  status: normalizeEmployeeStatus(payload.status, null),
});

const getStatusClass = (status = "") => {
  if (status.includes("Nghỉ")) return "on-leave";
  if (status.includes("Đang")) return "active";
  return "neutral";
};

const Employees = () => {
  const [employees, setEmployees] = useState([]);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    page_size: 5,
    total_pages: 1,
  });
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [departmentFilter, setDepartmentFilter] = useState("");
  const [sortValue, setSortValue] = useState("id-asc");
  const [departments, setDepartments] = useState([]);
  const [positions, setPositions] = useState([]);
  const [selectedEmp, setSelectedEmp] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");
  const [saving, setSaving] = useState(false);
  const [reloadKey, setReloadKey] = useState(0);

  const itemsPerPage = 5;
  const [sortBy, sortOrder] = sortValue.split("-");

  useEffect(() => {
    let active = true;

    const loadReferenceData = async () => {
      try {
        const [departmentData, positionData] = await Promise.all([
          departmentsApi.list(),
          positionsApi.list(),
        ]);
        if (!active) return;
        setDepartments(departmentData || []);
        setPositions(positionData || []);
      } catch (err) {
        if (active) {
          setError(
            err.message || "Could not load departments and positions.",
          );
        }
      }
    };

    loadReferenceData();
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;

    const loadEmployees = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await employeesApi.list({
          page: currentPage,
          page_size: itemsPerPage,
          search,
          department_id: departmentFilter,
          status: statusFilter,
          sort_by: sortBy,
          sort_order: sortOrder,
        });

        if (!active) return;
        setEmployees(data.items || []);
        setPagination({
          total: data.total || 0,
          page: data.page || currentPage,
          page_size: data.page_size || itemsPerPage,
          total_pages: data.total_pages || 1,
        });
      } catch (err) {
        if (active) setError(err.message || "Could not load employees.");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadEmployees();
    return () => {
      active = false;
    };
  }, [
    currentPage,
    departmentFilter,
    itemsPerPage,
    reloadKey,
    search,
    sortBy,
    sortOrder,
    statusFilter,
  ]);

  const handleSearch = (value) => {
    setSearch(value);
    setCurrentPage(1);
  };

  const handleEditClick = (emp) => {
    setSelectedEmp(emp);
    setFormError("");
    setIsModalOpen(true);
  };

  const handleSaveEmployee = async (employeeId, updatedEmp) => {
    setSaving(true);
    setFormError("");
    try {
      await employeesApi.update(
        employeeId,
        normalizeEmployeePayload(updatedEmp),
      );
      setIsModalOpen(false);
      setSelectedEmp(null);
      setReloadKey((key) => key + 1);
    } catch (err) {
      setFormError(err.message || "Could not update employee.");
    } finally {
      setSaving(false);
    }
  };

  const handleSaveNewEmployee = async (newEmpData) => {
    setSaving(true);
    setFormError("");
    try {
      await employeesApi.create(normalizeEmployeePayload(newEmpData));
      setIsAddModalOpen(false);
      setCurrentPage(1);
      setReloadKey((key) => key + 1);
    } catch (err) {
      setFormError(err.message || "Could not create employee.");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this employee?")) {
      return;
    }

    setError("");
    try {
      await employeesApi.remove(id);
      setReloadKey((key) => key + 1);
    } catch (err) {
      setError(err.message || "Could not delete employee.");
    }
  };

  const exportPDF = async () => {
    setError("");
    try {
      const blob = await employeesApi.exportPdf({
        department_id: departmentFilter,
        status: statusFilter,
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "employees.pdf";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message || "Could not export PDF.");
    }
  };

  const totalPages = Math.max(pagination.total_pages || 1, 1);

  return (
    <div className="employees-page-container">
      <header className="employees-header">
        <h2>Employee Management</h2>
        <div className="header-actions">
          <button className="btn btn-pdf" onClick={exportPDF} type="button">
            <FileText size={18} /> Export PDF
          </button>
          <button
            className="btn btn-add"
            onClick={() => {
              setFormError("");
              setIsAddModalOpen(true);
            }}
            type="button"
          >
            <Plus size={18} /> Add Employee
          </button>
        </div>
      </header>

      <div className="employees-card">
        <div className="table-top-actions">
          <div className="title-search-group">
            <h3>All Employees ({pagination.total})</h3>
            <SearchEmployees onSearch={handleSearch} />
          </div>
          <div className="controls">
            <select
              className="select-sort"
              value={departmentFilter}
              onChange={(e) => {
                setDepartmentFilter(e.target.value);
                setCurrentPage(1);
              }}
            >
              <option value="">All departments</option>
              {departments.map((department) => (
                <option key={department.id} value={department.id}>
                  {department.department_name}
                </option>
              ))}
            </select>
            <select
              className="select-sort"
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value);
                setCurrentPage(1);
              }}
            >
              {STATUS_OPTIONS.map((option) => (
                <option key={option.label} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <select
              className="select-sort"
              value={sortValue}
              onChange={(e) => {
                setSortValue(e.target.value);
                setCurrentPage(1);
              }}
            >
              <option value="id-asc">ID Asc</option>
              <option value="id-desc">ID Desc</option>
              <option value="full_name-asc">Name A-Z</option>
              <option value="full_name-desc">Name Z-A</option>
              <option value="hire_date-desc">Newest Hire</option>
            </select>
          </div>
        </div>

        {error && <div className="state-message error">{error}</div>}

        <div className="table-wrapper">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>ID</th>
                <th>Phone</th>
                <th>Email</th>
                <th>Department</th>
                <th>Position</th>
                <th>Status</th>
                <th style={{ textAlign: "center" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="8" className="table-state">
                    Loading employees...
                  </td>
                </tr>
              ) : employees.length > 0 ? (
                employees.map((emp) => (
                  <tr key={emp.id}>
                    <td className="fw-medium">{emp.full_name}</td>
                    <td>{employeeCode(emp.id)}</td>
                    <td className="contact-cell">
                      {emp.phone_number ? (
                        <a href={`tel:${emp.phone_number}`}>
                          {emp.phone_number}
                        </a>
                      ) : (
                        displayText(emp.phone_number)
                      )}
                    </td>
                    <td className="contact-cell">
                      {emp.email ? (
                        <a href={`mailto:${emp.email}`}>{emp.email}</a>
                      ) : (
                        displayText(emp.email)
                      )}
                    </td>
                    <td>{displayText(emp.department_name)}</td>
                    <td>{displayText(emp.position_name)}</td>
                    <td>
                      <span className={`badge ${getStatusClass(emp.status)}`}>
                        {displayText(emp.status)}
                      </span>
                    </td>
                    <td>
                      <div className="row-actions">
                        <button
                          className="btn-icon btn-edit"
                          onClick={() => handleEditClick(emp)}
                          type="button"
                          title="Edit employee"
                        >
                          <Edit2 size={16} />
                        </button>
                        <button
                          className="btn-icon btn-delete"
                          onClick={() => handleDelete(emp.id)}
                          type="button"
                          title="Delete employee"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="8" className="table-state">
                    No employees found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        <div className="pagination-container">
          <p>
            Page {pagination.page} of {totalPages} · {pagination.total} employees
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

      {isModalOpen && (
        <EditEmployeeModal
          isOpen={isModalOpen}
          employee={selectedEmp}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSaveEmployee}
          saving={saving}
          error={formError}
          departments={departments}
          positions={positions}
        />
      )}
      {isAddModalOpen && (
        <AddEmployee
          onClose={() => setIsAddModalOpen(false)}
          onSave={handleSaveNewEmployee}
          saving={saving}
          error={formError}
          departments={departments}
          positions={positions}
        />
      )}
    </div>
  );
};

export default Employees;
