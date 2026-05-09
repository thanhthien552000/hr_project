import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, Edit2, Plus, X, CalendarDays } from "lucide-react";
import SearchEmployees from "../InputSearch/Search";
import "./Attendance.css";
import { attendanceApi, employeesApi } from "../../../services/hrApi";
import { displayText, employeeCode, toOptionalNumber } from "../../../utils/formatters";

const pageSize = 10;

const buildAttendanceForm = (record) => ({
  employee_id: record?.employee_id || "",
  attendance_month: record?.attendance_month || "",
  work_days: record?.work_days ?? "",
  absent_days: record?.absent_days ?? 0,
  leave_days: record?.leave_days ?? 0,
  late_days: record?.late_days ?? 0,
});

const normalizeAttendancePayload = (payload, isEdit) => {
  const base = {
    work_days: Number(payload.work_days),
    absent_days: Number(payload.absent_days || 0),
    leave_days: Number(payload.leave_days || 0),
    late_days: Number(payload.late_days || 0),
  };

  if (isEdit) return base;

  return {
    ...base,
    employee_id: toOptionalNumber(payload.employee_id),
    attendance_month: payload.attendance_month,
  };
};

const AttendanceFormModal = ({ record, onClose, onSave, saving, error }) => {
  const [formData, setFormData] = useState(() => buildAttendanceForm(record));
  const [employees, setEmployees] = useState([]);
  const isEdit = Boolean(record);

  useEffect(() => {
    if (!isEdit) {
      employeesApi.list({ page_size: 100 }).then((res) => {
        setEmployees(res.items || []);
      }).catch(() => {});
    }
  }, [isEdit]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(normalizeAttendancePayload(formData, isEdit));
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content scale-in">
        <div className="modal-header">
          <h3>{isEdit ? "Update Attendance" : "Create Attendance"}</h3>
          <button className="close-btn" onClick={onClose} type="button">
            <X size={20} />
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div className="form-error">{error}</div>}

            <div className="form-row">
              <div className="form-group">
                <label>Employee</label>
                {isEdit ? (
                  <input
                    type="text"
                    value={formData.employee_id}
                    disabled
                  />
                ) : (
                  <select
                    name="employee_id"
                    value={formData.employee_id}
                    onChange={handleChange}
                    required
                  >
                    <option value="">-- Select employee --</option>
                    {employees.map((emp) => (
                      <option key={emp.id} value={emp.id}>
                        {emp.full_name} ({employeeCode(emp.id)})
                      </option>
                    ))}
                  </select>
                )}
              </div>
              <div className="form-group">
                <label>Attendance month</label>
                <div className="month-input-wrapper">
                  <CalendarDays size={18} className="month-icon" />
                  <input
                    type="month"
                    name="attendance_month"
                    value={formData.attendance_month}
                    onChange={handleChange}
                    disabled={isEdit}
                    required={!isEdit}
                  />
                </div>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Working days</label>
                <input
                  type="number"
                  min="0"
                  name="work_days"
                  value={formData.work_days}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Absent days</label>
                <input
                  type="number"
                  min="0"
                  name="absent_days"
                  value={formData.absent_days}
                  onChange={handleChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Leave days</label>
                <input
                  type="number"
                  min="0"
                  name="leave_days"
                  value={formData.leave_days}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Late days</label>
                <input
                  type="number"
                  min="0"
                  name="late_days"
                  value={formData.late_days}
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

const Attendance = () => {
  const [records, setRecords] = useState([]);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    total_pages: 1,
  });
  const [search, setSearch] = useState("");
  const [monthFilter, setMonthFilter] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [formError, setFormError] = useState("");
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let active = true;

    const loadAttendance = async () => {
      setLoading(true);
      setError("");
      try {
        const data = await attendanceApi.list({
          page: currentPage,
          page_size: pageSize,
          month: monthFilter,
        });

        if (!active) return;
        setRecords(data.items || []);
        setPagination({
          total: data.total || 0,
          page: data.page || currentPage,
          total_pages: data.total_pages || 1,
        });
      } catch (err) {
        if (active) setError(err.message || "Could not load attendance.");
      } finally {
        if (active) setLoading(false);
      }
    };

    loadAttendance();
    return () => {
      active = false;
    };
  }, [currentPage, monthFilter, reloadKey]);

  const filteredRecords = records.filter((record) => {
    const keyword = search.toLowerCase();
    return (
      (record.employee_name || "").toLowerCase().includes(keyword) ||
      employeeCode(record.employee_id).toLowerCase().includes(keyword)
    );
  });

  const openCreateModal = () => {
    setSelectedRecord(null);
    setFormError("");
    setIsModalOpen(true);
  };

  const openEditModal = (record) => {
    setSelectedRecord(record);
    setFormError("");
    setIsModalOpen(true);
  };

  const handleSaveAttendance = async (payload) => {
    setSaving(true);
    setFormError("");
    try {
      if (selectedRecord) {
        await attendanceApi.update(selectedRecord.id, payload);
      } else {
        await attendanceApi.create(payload);
      }
      setIsModalOpen(false);
      setReloadKey((key) => key + 1);
    } catch (err) {
      setFormError(err.message || "Could not save attendance.");
    } finally {
      setSaving(false);
    }
  };

  const totalPages = Math.max(pagination.total_pages || 1, 1);

  return (
    <div>
      <header className="attendance-header">
        <h2>Attendance Management</h2>
        <button className="btn btn-add" type="button" onClick={openCreateModal}>
          <Plus size={18} /> Add Attendance
        </button>
      </header>

      <div className="attendance-container">
        <div className="attendance-top table-header">
          <h3>Attendance Information ({pagination.total})</h3>
          <div className="attendance-controls">
            <input
              className="search-input"
              type="month"
              value={monthFilter}
              onChange={(e) => {
                setMonthFilter(e.target.value);
                setCurrentPage(1);
              }}
            />
            <SearchEmployees onSearch={setSearch} />
          </div>
        </div>

        {error && <div className="state-message error">{error}</div>}

        <table className="attendance-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Employee ID</th>
              <th>Month</th>
              <th>Working Days</th>
              <th>Absent Days</th>
              <th>Leave Days</th>
              <th>Late Days</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {loading ? (
              <tr>
                <td colSpan="8" className="table-state">
                  Loading attendance...
                </td>
              </tr>
            ) : filteredRecords.length > 0 ? (
              filteredRecords.map((record) => (
                <tr key={record.id}>
                  <td>{displayText(record.employee_name)}</td>
                  <td>{employeeCode(record.employee_id)}</td>
                  <td>{displayText(record.attendance_month)}</td>
                  <td>
                    <span className="badge-green">{record.work_days}</span>
                  </td>
                  <td>
                    <span className="badge-red">{record.absent_days}</span>
                  </td>
                  <td>{record.leave_days}</td>
                  <td>{record.late_days}</td>
                  <td>
                    <button
                      className="btn-icon btn-edit"
                      type="button"
                      onClick={() => openEditModal(record)}
                      title="Edit attendance"
                    >
                      <Edit2 size={16} />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="8" className="table-state">
                  No attendance records found.
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
        <AttendanceFormModal
          record={selectedRecord}
          onClose={() => setIsModalOpen(false)}
          onSave={handleSaveAttendance}
          saving={saving}
          error={formError}
        />
      )}
    </div>
  );
};

export default Attendance;
