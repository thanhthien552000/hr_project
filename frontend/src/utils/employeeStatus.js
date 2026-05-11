export const EMPLOYEE_STATUSES = [
  "Đang làm việc",
  "Nghỉ việc",
  "Nghỉ phép",
  "Thử việc",
  "Thực tập",
];

const STATUS_ALIASES = {
  "Äang lÃ m viá»‡c": "Đang làm việc",
  "Nghá»‰ viá»‡c": "Nghỉ việc",
  "Ngh? vi?c": "Nghỉ việc",
  "Nghá»‰ phÃ©p": "Nghỉ phép",
  "Thá»­ viá»‡c": "Thử việc",
  "Thá»±c táº­p": "Thực tập",
  "dang lam viec": "Đang làm việc",
  "nghi viec": "Nghỉ việc",
  "nghi phep": "Nghỉ phép",
  "thu viec": "Thử việc",
  "thuc tap": "Thực tập",
};

const foldVietnamese = (value) =>
  value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d")
    .replace(/Đ/g, "D")
    .toLowerCase()
    .trim();

const STATUS_BY_FOLDED_VALUE = EMPLOYEE_STATUSES.reduce((acc, status) => {
  acc[foldVietnamese(status)] = status;
  return acc;
}, {});

export const normalizeEmployeeStatus = (
  value,
  fallback = "Đang làm việc",
) => {
  if (value === null || value === undefined || value === "") return fallback;

  const status = String(value).trim();
  if (EMPLOYEE_STATUSES.includes(status)) return status;

  return (
    STATUS_ALIASES[status] ||
    STATUS_ALIASES[status.toLowerCase()] ||
    STATUS_BY_FOLDED_VALUE[foldVietnamese(status)] ||
    fallback
  );
};
