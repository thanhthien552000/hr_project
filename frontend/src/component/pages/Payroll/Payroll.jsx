import { useEffect, useMemo, useState } from "react";
import { ChevronLeft, ChevronRight, Edit2, Plus, X } from "lucide-react";
import SearchEmployees from "../InputSearch/Search";
import "./Payroll.css";
import { payrollApi, employeesApi } from "../../../services/hrApi";
import {
  currentMonthValue,
  displayText,
  employeeCode,
  formatCurrency,
  formatPercent,
  toOptionalNumber,
} from "../../../utils/formatters";
import {
  calculateNetSalary,
  hasErrors,
  validatePayrollForm,
  validatePayrollWarnings,
  visibleErrors,
} from "../../../utils/validators";

const pageSize = 10;

const buildSalaryForm = (salary) => ({
  employee_id: salary?.employee_id || "",
  salary_month: salary?.salary_month || salary?.current_month?.salary_month || "",
  base_salary: salary?.base_salary ?? salary?.current_month?.base_salary ?? "",
  bonus: salary?.bonus ?? salary?.current_month?.bonus ?? 0,
  deductions: salary?.deductions ?? salary?.current_month?.deductions ?? 0,
  net_salary: salary?.net_salary ?? salary?.current_month?.net_salary ?? "",
});

const normalizeSalaryPayload = (payload, isEdit) => {
  const base = {
    base_salary: Number(payload.base_salary),
    bonus: Number(payload.bonus || 0),
    deductions: Number(payload.deductions || 0),
    net_salary: calculateNetSalary(payload),
  };

  if (isEdit) return base;

  return {
    ...base,
    employee_id: toOptionalNumber(payload.employee_id),
    salary_month: payload.salary_month,
  };
};

const SalaryFormModal = ({ salary, onClose, onSave, saving, error, employees = [] }) => {
  const [formData, setFormData] = useState(() => {
    const initial = buildSalaryForm(salary);
    // Default salary_month to current month for create
    if (!initial.salary_month) {
      initial.salary_month = currentMonthValue();
    }
    if (initial.net_salary === "" && initial.base_salary !== "") {
      initial.net_salary = calculateNetSalary(initial);
    }
    return initial;
  });
  const [touchedFields, setTouchedFields] = useState({});
  const [submitAttempted, setSubmitAttempted] = useState(false);
  const isEdit = Boolean(salary);
  const validationErrors = useMemo(
    () => validatePayrollForm(formData, isEdit),
    [formData, isEdit]
  );
  const fieldErrors = useMemo(
    () => visibleErrors(validationErrors, touchedFields, submitAttempted),
    [submitAttempted, touchedFields, validationErrors]
  );
  const payrollWarnings = useMemo(
    () => validatePayrollWarnings(formData),
    [formData]
  );
  const isSubmitDisabled = saving || hasErrors(validationErrors);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((current) => {
      const updated = { ...current, [name]: value };
      // Auto-calculate net_salary
      if (["base_salary", "bonus", "deductions"].includes(name)) {
        updated.net_salary = calculateNetSalary(updated);
      }
      return updated;
    });
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouchedFields((current) => ({ ...current, [name]: true }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitAttempted(true);
    if (hasErrors(validationErrors)) return;
    onSave(normalizeSalaryPayload(formData, isEdit));
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content scale-in">
        <div className="modal-header">
          <h3>{isEdit ? "Update Payroll" : "Create Payroll"}</h3>
          <button className="close-btn" onClick={onClose} type="button">
            <X size={20} />
          </button>
        </div>
        <form onSubmit={handleSubmit} noValidate>
          <div className="modal-body">
            {error && <div className="form-error">{error}</div>}

            <div className="form-row">
              <div className="form-group">
                <label>Nhân viên</label>
                <select
                  name="employee_id"
                  value={formData.employee_id}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  disabled={isEdit}
                  className={fieldErrors.employee_id ? "input-error" : ""}
                  required={!isEdit}
                >
                  <option value="">-- Chọn nhân viên --</option>
                  {employees.map((emp) => (
                    <option key={emp.id} value={emp.id}>
                      {employeeCode(emp.id)} - {emp.full_name}
                    </option>
                  ))}
                </select>
                {fieldErrors.employee_id && <span className="field-error">{fieldErrors.employee_id}</span>}
              </div>
              <div className="form-group">
                <label>Tháng lương</label>
                <input
                  type="month"
                  name="salary_month"
                  value={formData.salary_month}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  disabled={isEdit}
                  className={fieldErrors.salary_month ? "input-error" : ""}
                  required={!isEdit}
                />
                {fieldErrors.salary_month && <span className="field-error">{fieldErrors.salary_month}</span>}
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Base salary</label>
                <input
                  type="number"
                  min="0"
                  name="base_salary"
                  value={formData.base_salary}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={fieldErrors.base_salary ? "input-error" : ""}
                  required
                />
                {fieldErrors.base_salary && <span className="field-error">{fieldErrors.base_salary}</span>}
              </div>
              <div className="form-group">
                <label>Net salary (auto)</label>
                <input
                  type="number"
                  name="net_salary"
                  value={formData.net_salary}
                  readOnly
                  className={`readonly-input ${payrollWarnings.net_salary ? "input-warning" : ""}`}
                />
                {payrollWarnings.net_salary && <span className="field-warning">{payrollWarnings.net_salary}</span>}
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Bonus</label>
                <input
                  type="number"
                  min="0"
                  name="bonus"
                  value={formData.bonus}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={fieldErrors.bonus ? "input-error" : ""}
                />
                {fieldErrors.bonus && <span className="field-error">{fieldErrors.bonus}</span>}
              </div>
              <div className="form-group">
                <label>Deductions</label>
                <input
                  type="number"
                  min="0"
                  name="deductions"
                  value={formData.deductions}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={fieldErrors.deductions ? "input-error" : ""}
                />
                {fieldErrors.deductions && <span className="field-error">{fieldErrors.deductions}</span>}
              </div>
            </div>
          </div>
          <div className="modal-footer">
            <button
              type="button"
              className="btn-cancel"
              onClick={onClose}
              disabled={saving}
            >
              Cancel
            </button>
            <button type="submit" className="btn-save" disabled={isSubmitDisabled}>
              {saving ? "Saving..." : "Save"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const Payroll = () => {
  const [rows, setRows] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    total_pages: 1,
  });
  const [searchTerm, setSearchTerm] = useState("");
  const [monthFilter, setMonthFilter] = useState(currentMonthValue());
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");
  const [selectedSalary, setSelectedSalary] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    employeesApi.list({ page: 1, page_size: 100 }).then((data) => {
      setEmployees(data?.items || data || []);
    }).catch((err) => {
      console.error("Failed to load employees for payroll:", err);
    });
  }, []);

  useEffect(() => {
    let active = true;

    const loadPayroll = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await payrollApi.list({
          page: currentPage,
          page_size: pageSize,
          month: monthFilter,
        });

        if (!active) return;
        setRows(data.items || []);
        setPagination({
          total: data.total || 0,
          page: data.page || currentPage,
          total_pages: data.total_pages || 1,
        });
      } catch (err) {
        if (active) setError(err.message || "Could not load payroll.");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadPayroll();
    return () => {
      active = false;
    };
  }, [currentPage, monthFilter, reloadKey]);

  const filteredRows = rows.filter((row) => {
    const keyword = searchTerm.toLowerCase();
    return (
      (row.full_name || row.employee_name || "").toLowerCase().includes(keyword) ||
      employeeCode(row.employee_id).toLowerCase().includes(keyword)
    );
  });

  const openCreateModal = () => {
    setSelectedSalary(null);
    setFormError("");
    setIsModalOpen(true);
  };

  const openEditModal = (row) => {
    setSelectedSalary(row);
    setFormError("");
    setIsModalOpen(true);
  };

  const handleSaveSalary = async (payload) => {
    setSaving(true);
    setFormError("");
    try {
      if (selectedSalary) {
        await payrollApi.update(selectedSalary.salary_id || selectedSalary.id, payload);
      } else {
        await payrollApi.create(payload);
      }
      setIsModalOpen(false);
      setReloadKey((key) => key + 1);
    } catch (err) {
      setFormError(err.message || "Could not save payroll.");
    } finally {
      setSaving(false);
    }
  };

  const totalPages = Math.max(pagination.total_pages || 1, 1);

  return (
    <div className="payroll-page">
      <header className="payroll-header">
        <h2>Payroll Employee Management</h2>
        <button className="btn btn-add" type="button" onClick={openCreateModal}>
          <Plus size={18} /> Add Payroll
        </button>
      </header>

      <div className="payroll-table-container">
        <div className="table-header">
          <h3>Payroll Information ({pagination.total})</h3>
          <div className="payroll-controls">
            <input
              className="search-input"
              type="month"
              value={monthFilter}
              onChange={(e) => {
                setMonthFilter(e.target.value);
                setCurrentPage(1);
              }}
            />
            <SearchEmployees onSearch={setSearchTerm} />
          </div>
        </div>

        {error && <div className="state-message error">{error}</div>}

        <table className="payroll-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Employee ID</th>
              <th>Department</th>
              <th>Previous Month Salary</th>
              <th>Current Month Salary</th>
              <th>Change</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {loading ? (
              <tr>
                <td colSpan="7" className="table-state">
                  Loading payroll...
                </td>
              </tr>
            ) : filteredRows.length > 0 ? (
              filteredRows.map((row) => {
                const currentSalary = row.current_month?.net_salary ?? row.net_salary;
                const previousSalary = row.previous_month?.net_salary;
                const isUp = row.change_direction !== "down";

                return (
                  <tr key={row.salary_id || row.id}>
                    <td data-label="Name">
                      {displayText(row.full_name || row.employee_name)}
                    </td>
                    <td data-label="Employee ID">{employeeCode(row.employee_id)}</td>
                    <td data-label="Department">
                      {displayText(row.department_name)}
                    </td>
                    <td data-label="Previous">
                      {previousSalary === null || previousSalary === undefined
                        ? "-"
                        : formatCurrency(previousSalary)}
                    </td>
                    <td
                      data-label="Current"
                      className={isUp ? "salary-up" : "salary-down"}
                    >
                      {formatCurrency(currentSalary)}
                    </td>
                    <td data-label="Change">
                      {row.change_percentage === null ||
                      row.change_percentage === undefined ? (
                        "-"
                      ) : (
                        <span className={isUp ? "salary-up" : "salary-down"}>
                          {isUp ? "↑" : "↓"} {formatPercent(row.change_percentage)}
                        </span>
                      )}
                    </td>
                    <td data-label="Actions">
                      <button
                        className="btn-icon btn-edit"
                        type="button"
                        onClick={() => openEditModal(row)}
                        title="Edit payroll"
                      >
                        <Edit2 size={16} />
                      </button>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="7" className="table-state">
                  No payroll records found.
                </td>
              </tr>
            )}
          </tbody>
        </table>

        <div className="pagination-container">
          <p>
            Page {pagination.page} of {totalPages} · {pagination.total} records
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
        <SalaryFormModal
          salary={selectedSalary}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSaveSalary}
          saving={saving}
          error={formError}
          employees={employees}
        />
      )}
    </div>
  );
};

export default Payroll;
