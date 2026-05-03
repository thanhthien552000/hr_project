import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, Edit2, Plus, X } from "lucide-react";
import SearchEmployees from "../InputSearch/Search";
import "./Payroll.css";
import { payrollApi } from "../../../services/hrApi";
import {
  displayText,
  employeeCode,
  formatCurrency,
  formatPercent,
  toOptionalNumber,
} from "../../../utils/formatters";

const pageSize = 10;

const buildSalaryForm = (salary) => ({
  employee_id: salary?.employee_id || "",
  salary_month: salary?.salary_month || salary?.current_month?.salary_month || "",
  base_salary: salary?.base_salary || salary?.current_month?.base_salary || "",
  bonus: salary?.bonus || salary?.current_month?.bonus || 0,
  deductions: salary?.deductions || salary?.current_month?.deductions || 0,
  net_salary: salary?.net_salary || salary?.current_month?.net_salary || "",
});

const normalizeSalaryPayload = (payload, isEdit) => {
  const base = {
    base_salary: Number(payload.base_salary),
    bonus: Number(payload.bonus || 0),
    deductions: Number(payload.deductions || 0),
    net_salary: Number(payload.net_salary),
  };

  if (isEdit) return base;

  return {
    ...base,
    employee_id: toOptionalNumber(payload.employee_id),
    salary_month: payload.salary_month,
  };
};

const SalaryFormModal = ({ salary, onClose, onSave, saving, error }) => {
  const [formData, setFormData] = useState(() => buildSalaryForm(salary));
  const isEdit = Boolean(salary);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
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
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div className="form-error">{error}</div>}

            <div className="form-row">
              <div className="form-group">
                <label>Employee ID</label>
                <input
                  type="number"
                  min="1"
                  name="employee_id"
                  value={formData.employee_id}
                  onChange={handleChange}
                  disabled={isEdit}
                  required={!isEdit}
                />
              </div>
              <div className="form-group">
                <label>Salary month</label>
                <input
                  type="month"
                  name="salary_month"
                  value={formData.salary_month}
                  onChange={handleChange}
                  disabled={isEdit}
                  required={!isEdit}
                />
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
                  required
                />
              </div>
              <div className="form-group">
                <label>Net salary</label>
                <input
                  type="number"
                  min="0"
                  name="net_salary"
                  value={formData.net_salary}
                  onChange={handleChange}
                  required
                />
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
                />
              </div>
              <div className="form-group">
                <label>Deductions</label>
                <input
                  type="number"
                  min="0"
                  name="deductions"
                  value={formData.deductions}
                  onChange={handleChange}
                />
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
            <button type="submit" className="btn-save" disabled={saving}>
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
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    total_pages: 1,
  });
  const [searchTerm, setSearchTerm] = useState("");
  const [monthFilter, setMonthFilter] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");
  const [selectedSalary, setSelectedSalary] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [reloadKey, setReloadKey] = useState(0);

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
        />
      )}
    </div>
  );
};

export default Payroll;
