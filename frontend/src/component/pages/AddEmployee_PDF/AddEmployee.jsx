import { useState } from "react";
import { X } from "lucide-react";
import { toOptionalNumber } from "../../../utils/formatters";

const STATUS_OPTIONS = [
  "Đang làm việc",
  "Nghỉ việc",
  "Nghỉ phép",
  "Thử việc",
  "Thực tập",
];

const AddEmployee = ({
  onClose,
  onSave,
  saving,
  error,
  departments = [],
  positions = [],
}) => {
  const [formData, setFormData] = useState({
    full_name: "",
    date_of_birth: "",
    gender: "Nam",
    phone_number: "",
    email: "",
    hire_date: "",
    department_id: "",
    position_id: "",
    status: "Đang làm việc",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      ...formData,
      department_id: toOptionalNumber(formData.department_id),
      position_id: toOptionalNumber(formData.position_id),
    });
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content scale-in">
        <div className="modal-header">
          <h3>Thêm nhân viên mới</h3>
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
                placeholder="Nhập họ và tên"
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
                placeholder="Nhập số điện thoại"
                value={formData.phone_number}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="email@company.vn"
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
              Hủy bỏ
            </button>
            <button type="submit" className="btn-save" disabled={saving}>
              {saving ? "Đang lưu..." : "Thêm nhân viên"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddEmployee;
