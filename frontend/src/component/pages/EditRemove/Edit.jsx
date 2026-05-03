import { useEffect, useState } from "react";
import { X } from "lucide-react";
import { toOptionalNumber } from "../../../utils/formatters";
import "./Edit.css";

const STATUS_OPTIONS = [
  "Đang làm việc",
  "Nghỉ việc",
  "Nghỉ phép",
  "Thử việc",
  "Thực tập",
];

const buildFormState = (employee) => ({
  full_name: employee?.full_name || "",
  date_of_birth: employee?.date_of_birth || "",
  gender: employee?.gender || "Nam",
  phone_number: employee?.phone_number || "",
  email: employee?.email || "",
  hire_date: employee?.hire_date || "",
  department_id: employee?.department_id || "",
  position_id: employee?.position_id || "",
  status: employee?.status || "Đang làm việc",
});

const EditEmployeeModal = ({
  isOpen,
  onClose,
  employee,
  onSave,
  saving,
  error,
  departments = [],
  positions = [],
}) => {
  const [formData, setFormData] = useState(() => buildFormState(employee));

  useEffect(() => {
    setFormData(buildFormState(employee));
  }, [employee]);

  if (!isOpen || !employee) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(employee.id, {
      ...formData,
      department_id: toOptionalNumber(formData.department_id),
      position_id: toOptionalNumber(formData.position_id),
    });
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content scale-in">
        <div className="modal-header">
          <h3>Chỉnh sửa nhân viên</h3>
          <button className="close-btn" onClick={onClose} type="button">
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="modal-body">
            {error && <div className="form-error">{error}</div>}

            <div className="form-group">
              <label>Họ và tên</label>
              <input
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Ngày sinh</label>
                <input
                  type="date"
                  name="date_of_birth"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Giới tính</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                >
                  <option value="Nam">Nam</option>
                  <option value="Nữ">Nữ</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Ngày vào làm</label>
              <input
                type="date"
                name="hire_date"
                value={formData.hire_date}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Phòng ban</label>
                <select
                  name="department_id"
                  value={formData.department_id}
                  onChange={handleChange}
                >
                  <option value="">Chưa chọn</option>
                  {departments.map((department) => (
                    <option key={department.id} value={department.id}>
                      {department.department_name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Chức vụ</label>
                <select
                  name="position_id"
                  value={formData.position_id}
                  onChange={handleChange}
                >
                  <option value="">Chưa chọn</option>
                  {positions.map((position) => (
                    <option key={position.id} value={position.id}>
                      {position.position_name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Số điện thoại</label>
              <input
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Trạng thái</label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
              >
                {STATUS_OPTIONS.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="modal-footer">
            <button
              type="button"
              className="btn-cancel"
              onClick={onClose}
              disabled={saving}
            >
              Thoát
            </button>
            <button type="submit" className="btn-save" disabled={saving}>
              {saving ? "Đang lưu..." : "Lưu thay đổi"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditEmployeeModal;
