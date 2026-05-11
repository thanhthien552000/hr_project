import { useMemo, useState } from "react";
import { X } from "lucide-react";
import { toOptionalNumber } from "../../../utils/formatters";
import {
  EMPLOYEE_STATUSES,
  normalizeEmployeeStatus,
} from "../../../utils/employeeStatus";
import {
  hasErrors,
  normalizePhoneNumber,
  validateEmployeeForm,
  visibleErrors,
} from "../../../utils/validators";

const STATUS_OPTIONS = EMPLOYEE_STATUSES;

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
  const [touchedFields, setTouchedFields] = useState({});
  const [submitAttempted, setSubmitAttempted] = useState(false);
  const validationErrors = useMemo(
    () =>
      validateEmployeeForm(formData, {
        requireDepartmentPosition: true,
      }),
    [formData]
  );
  const fieldErrors = useMemo(
    () => visibleErrors(validationErrors, touchedFields, submitAttempted),
    [submitAttempted, touchedFields, validationErrors]
  );
  const isSubmitDisabled = saving || hasErrors(validationErrors);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((current) => ({ ...current, [name]: value }));
  };

  const handleBlur = (e) => {
    const { name } = e.target;
    setTouchedFields((current) => ({ ...current, [name]: true }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitAttempted(true);
    if (hasErrors(validationErrors)) return;
    onSave({
      ...formData,
      full_name: formData.full_name.trim(),
      phone_number: normalizePhoneNumber(formData.phone_number),
      email: formData.email?.trim() || "",
      department_id: toOptionalNumber(formData.department_id),
      position_id: toOptionalNumber(formData.position_id),
      status: normalizeEmployeeStatus(formData.status),
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

        <form onSubmit={handleSubmit} noValidate>
          <div className="modal-body">
            {error && <div className="form-error">{error}</div>}

            <div className="form-group">
              <label>Họ và tên</label>
              <input
                name="full_name"
                placeholder="Nhập họ và tên"
                value={formData.full_name}
                onChange={handleChange}
                onBlur={handleBlur}
                className={fieldErrors.full_name ? "input-error" : ""}
                required
              />
              {fieldErrors.full_name && <span className="field-error">{fieldErrors.full_name}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Ngày sinh</label>
                <input
                  type="date"
                  name="date_of_birth"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={fieldErrors.date_of_birth ? "input-error" : ""}
                  required
                />
                {fieldErrors.date_of_birth && <span className="field-error">{fieldErrors.date_of_birth}</span>}
              </div>
              <div className="form-group">
                <label>Giới tính</label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  onBlur={handleBlur}
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
                onBlur={handleBlur}
                className={fieldErrors.hire_date ? "input-error" : ""}
                required
              />
              {fieldErrors.hire_date && <span className="field-error">{fieldErrors.hire_date}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Phòng ban</label>
                <select
                  name="department_id"
                  value={formData.department_id}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={fieldErrors.department_id ? "input-error" : ""}
                  required
                >
                  <option value="">Chưa chọn</option>
                  {departments.map((department) => (
                    <option key={department.id} value={department.id}>
                      {department.department_name}
                    </option>
                  ))}
                </select>
                {fieldErrors.department_id && <span className="field-error">{fieldErrors.department_id}</span>}
              </div>
              <div className="form-group">
                <label>Chức vụ</label>
                <select
                  name="position_id"
                  value={formData.position_id}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  className={fieldErrors.position_id ? "input-error" : ""}
                  required
                >
                  <option value="">Chưa chọn</option>
                  {positions.map((position) => (
                    <option key={position.id} value={position.id}>
                      {position.position_name}
                    </option>
                  ))}
                </select>
                {fieldErrors.position_id && <span className="field-error">{fieldErrors.position_id}</span>}
              </div>
            </div>

            <div className="form-group">
              <label>Số điện thoại</label>
              <input
                name="phone_number"
                placeholder="Nhập số điện thoại"
                value={formData.phone_number}
                onChange={handleChange}
                onBlur={handleBlur}
                className={fieldErrors.phone_number ? "input-error" : ""}
              />
              {fieldErrors.phone_number && <span className="field-error">{fieldErrors.phone_number}</span>}
            </div>

            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                placeholder="email@gmail.com"
                value={formData.email}
                onChange={handleChange}
                onBlur={handleBlur}
                className={fieldErrors.email ? "input-error" : ""}
              />
              {fieldErrors.email && <span className="field-error">{fieldErrors.email}</span>}
            </div>

            <div className="form-group">
              <label>Trạng thái</label>
              <select
                name="status"
                value={formData.status}
                onChange={handleChange}
                onBlur={handleBlur}
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
            <button type="submit" className="btn-save" disabled={isSubmitDisabled}>
              {saving ? "Đang lưu..." : "Thêm nhân viên"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AddEmployee;
