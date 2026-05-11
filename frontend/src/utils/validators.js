/**
 * Validation utilities for HR project forms.
 * Each validator returns an error message string or "" if valid.
 */

const PHONE_REGEX = /^0\d{9}$/;
const EMAIL_REGEX = /^[A-Za-z0-9._%+-]+@gmail\.com$/i;
const NAME_REGEX = /^[\p{L}\s'-]+$/u;
const MONTH_REGEX = /^\d{4}-(0[1-9]|1[0-2])$/;

const isBlank = (value) =>
  value === null || value === undefined || String(value).trim() === "";

const parseDateInput = (value) => {
  if (isBlank(value)) return null;
  const [year, month, day] = String(value).split("-").map(Number);
  if (!year || !month || !day) return null;

  const date = new Date(year, month - 1, day);
  if (
    date.getFullYear() !== year ||
    date.getMonth() !== month - 1 ||
    date.getDate() !== day
  ) {
    return null;
  }
  return date;
};

const startOfToday = () => {
  const today = new Date();
  return new Date(today.getFullYear(), today.getMonth(), today.getDate());
};

const parseMonthInput = (value) => {
  if (isBlank(value)) return null;
  const monthValue = String(value).trim();
  if (!MONTH_REGEX.test(monthValue)) return null;
  const [year, month] = monthValue.split("-").map(Number);
  return new Date(year, month - 1, 1);
};

const addMonths = (date, count) =>
  new Date(date.getFullYear(), date.getMonth() + count, 1);

const formatMonth = (date) =>
  `${String(date.getMonth() + 1).padStart(2, "0")}/${date.getFullYear()}`;

const daysInMonth = (monthDate) =>
  new Date(monthDate.getFullYear(), monthDate.getMonth() + 1, 0).getDate();

const toFiniteNumber = (value) => {
  if (isBlank(value)) return null;
  const n = Number(String(value).trim());
  return Number.isFinite(n) ? n : null;
};

/** Trim and check required field */
export const required = (value, label = "Trường này") => {
  if (isBlank(value)) {
    return `${label} không được để trống`;
  }
  return "";
};

/** Minimum length */
export const minLength = (value, min, label = "Trường này") => {
  if (value && String(value).trim().length < min) {
    return `${label} phải có ít nhất ${min} ký tự`;
  }
  return "";
};

/** Maximum length */
export const maxLength = (value, max, label = "Trường này") => {
  if (value && String(value).trim().length > max) {
    return `${label} không được quá ${max} ký tự`;
  }
  return "";
};

/** Vietnamese full name: letters, spaces, hyphens, apostrophes only */
export const fullName = (value) => {
  if (!value || !value.trim()) return "";
  if (!NAME_REGEX.test(value.trim().normalize("NFC"))) {
    return "Họ tên chỉ được chứa chữ cái, khoảng trắng, dấu nháy hoặc dấu gạch nối";
  }
  return "";
};

/** Email format */
export const email = (value) => {
  if (!value || !value.trim()) return ""; // optional - check required separately
  if (!EMAIL_REGEX.test(value.trim())) {
    return "Email phải đúng định dạng Gmail (VD: ten@gmail.com)";
  }
  return "";
};

export const normalizePhoneNumber = (value) =>
  String(value || "")
    .trim()
    .replace(/[\s-]/g, "");

/** Vietnamese phone number: 10 digits starting with 0 */
export const phoneVN = (value) => {
  if (!value || !value.trim()) return ""; // optional
  if (!/^[\d\s-]+$/.test(value.trim())) {
    return "Số điện thoại chỉ được chứa chữ số, khoảng trắng hoặc dấu gạch ngang";
  }
  if (!PHONE_REGEX.test(normalizePhoneNumber(value))) {
    return "Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0 (VD: 0912 345 678)";
  }
  return "";
};

/** Date must not be in the future */
export const dateNotFuture = (value, label = "Ngày") => {
  if (!value) return "";
  const d = parseDateInput(value);
  if (!d) return `${label} không hợp lệ`;
  if (d > startOfToday()) return `${label} không được ở tương lai`;
  return "";
};

/** Age must be >= minAge */
export const minAge = (dob, min = 16) => {
  if (!dob) return "";
  const birth = parseDateInput(dob);
  if (!birth) return "Ngày sinh không hợp lệ";
  const today = startOfToday();
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  if (age < min) return `Nhân viên phải đủ ${min} tuổi trở lên`;
  if (age > 100) return "Ngày sinh không hợp lệ";
  return "";
};

export const hireDateAfterDobAndMinAge = (dob, hireDate, min = 16) => {
  if (!dob || !hireDate) return "";
  const birth = parseDateInput(dob);
  const hire = parseDateInput(hireDate);
  if (!birth || !hire) return "";

  if (hire < birth) {
    return "Ngày vào làm không được trước ngày sinh";
  }

  const eligibleDate = new Date(birth);
  eligibleDate.setFullYear(birth.getFullYear() + min);
  if (hire < eligibleDate) {
    return `Ngày vào làm phải từ khi nhân viên đủ ${min} tuổi`;
  }

  return "";
};

export const monthNotTooFarInFuture = (
  value,
  maxMonthOffset = 1,
  label = "Tháng"
) => {
  if (!value) return "";
  const month = parseMonthInput(value);
  if (!month) return `${label} không hợp lệ`;

  const today = startOfToday();
  const maxAllowedMonth = addMonths(
    new Date(today.getFullYear(), today.getMonth(), 1),
    maxMonthOffset
  );

  if (month > maxAllowedMonth) {
    return `${label} không được sau ${formatMonth(maxAllowedMonth)}`;
  }

  return "";
};

/** Number must be >= 0 */
export const nonNegative = (value, label = "Giá trị") => {
  if (isBlank(value)) return "";
  const n = toFiniteNumber(value);
  if (n === null) return `${label} phải là số hợp lệ`;
  if (n < 0) return `${label} không được âm`;
  return "";
};

/** Number must be >= 0 and <= max */
export const numberRange = (value, min, max, label = "Giá trị") => {
  if (isBlank(value)) return "";
  const n = toFiniteNumber(value);
  if (n === null) return `${label} phải là số hợp lệ`;
  if (n < min) return `${label} không được nhỏ hơn ${min}`;
  if (n > max) return `${label} không được lớn hơn ${max}`;
  return "";
};

export const attendanceDaysWithinMonth = (data) => {
  const month = parseMonthInput(data.attendance_month);
  if (!month) return "";

  const workDays = toFiniteNumber(data.work_days);
  const absentDays = toFiniteNumber(data.absent_days) ?? 0;
  const leaveDays = toFiniteNumber(data.leave_days) ?? 0;
  if (workDays === null) return "";

  const monthDays = daysInMonth(month);
  const total = workDays + absentDays + leaveDays;
  if (total > monthDays) {
    return `Tổng ngày công, ngày vắng và ngày phép không được vượt quá ${monthDays} ngày của tháng ${formatMonth(month)}`;
  }

  return "";
};

export const calculateNetSalary = (data) => {
  const baseSalary = toFiniteNumber(data.base_salary) ?? 0;
  const bonus = toFiniteNumber(data.bonus) ?? 0;
  const deductions = toFiniteNumber(data.deductions) ?? 0;
  return baseSalary + bonus - deductions;
};

export const netSalaryWarning = (data) => {
  if (calculateNetSalary(data) < 0) {
    return "Lương thực nhận đang âm; vui lòng kiểm tra lại khấu trừ";
  }
  return "";
};

/**
 * Run multiple validators on a value, return the first error.
 * Usage: firstError(value, [required(value, "Họ tên"), minLength(value, 2, "Họ tên")])
 */
export const firstError = (...errors) => {
  for (const err of errors) {
    if (err) return err;
  }
  return "";
};

/**
 * Validate employee form data, return errors object { field: message }.
 */
export const validateEmployeeForm = (data, options = {}) => {
  const { requireDepartmentPosition = false } = options;
  const errors = {};

  errors.full_name = firstError(
    required(data.full_name, "Họ và tên"),
    minLength(data.full_name, 2, "Họ và tên"),
    maxLength(data.full_name, 100, "Họ và tên"),
    fullName(data.full_name)
  );

  errors.date_of_birth = firstError(
    required(data.date_of_birth, "Ngày sinh"),
    dateNotFuture(data.date_of_birth, "Ngày sinh"),
    minAge(data.date_of_birth, 16)
  );

  errors.hire_date = firstError(
    required(data.hire_date, "Ngày vào làm"),
    dateNotFuture(data.hire_date, "Ngày vào làm"),
    hireDateAfterDobAndMinAge(data.date_of_birth, data.hire_date, 16)
  );

  if (requireDepartmentPosition) {
    errors.department_id = required(data.department_id, "Phòng ban");
    errors.position_id = required(data.position_id, "Chức vụ");
  }

  errors.phone_number = phoneVN(data.phone_number);

  errors.email = email(data.email);

  // Remove empty errors
  Object.keys(errors).forEach((key) => {
    if (!errors[key]) delete errors[key];
  });

  return errors;
};

/**
 * Validate attendance form data.
 */
export const validateAttendanceForm = (data, isEdit) => {
  const errors = {};

  if (!isEdit) {
    errors.employee_id = required(data.employee_id, "Nhân viên");
    errors.attendance_month = firstError(
      required(data.attendance_month, "Tháng chấm công"),
      monthNotTooFarInFuture(data.attendance_month, 1, "Tháng chấm công")
    );
  }

  errors.work_days = firstError(
    required(data.work_days, "Số ngày công"),
    numberRange(data.work_days, 0, 31, "Số ngày công")
  );

  errors.absent_days = numberRange(data.absent_days, 0, 31, "Số ngày vắng");
  errors.leave_days = numberRange(data.leave_days, 0, 31, "Số ngày phép");
  errors.late_days = numberRange(data.late_days, 0, 31, "Số ngày đi muộn");
  errors.attendance_days = attendanceDaysWithinMonth(data);

  Object.keys(errors).forEach((key) => {
    if (!errors[key]) delete errors[key];
  });

  return errors;
};

/**
 * Validate payroll/salary form data.
 */
export const validatePayrollForm = (data, isEdit) => {
  const errors = {};

  if (!isEdit) {
    errors.employee_id = required(data.employee_id, "Nhân viên");
    errors.salary_month = firstError(
      required(data.salary_month, "Tháng lương"),
      monthNotTooFarInFuture(data.salary_month, 1, "Tháng lương")
    );
  }

  errors.base_salary = firstError(
    required(data.base_salary, "Lương cơ bản"),
    nonNegative(data.base_salary, "Lương cơ bản")
  );

  errors.bonus = nonNegative(data.bonus, "Thưởng");
  errors.deductions = nonNegative(data.deductions, "Khấu trừ");

  Object.keys(errors).forEach((key) => {
    if (!errors[key]) delete errors[key];
  });

  return errors;
};

export const validatePayrollWarnings = (data) => {
  const warnings = {
    net_salary: netSalaryWarning(data),
  };

  Object.keys(warnings).forEach((key) => {
    if (!warnings[key]) delete warnings[key];
  });

  return warnings;
};

/** Check if errors object has any errors */
export const hasErrors = (errors) => Object.keys(errors).length > 0;

export const visibleErrors = (
  errors,
  touchedFields = {},
  submitted = false,
  relatedFields = {}
) => {
  const visible = {};

  Object.entries(errors).forEach(([field, message]) => {
    const relatedTouched = relatedFields[field]?.some(
      (relatedField) => touchedFields[relatedField]
    );
    if (submitted || touchedFields[field] || relatedTouched) {
      visible[field] = message;
    }
  });

  return visible;
};
