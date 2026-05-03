export const currentMonthValue = () => new Date().toISOString().slice(0, 7);

export const formatCurrency = (value) =>
  new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0,
  }).format(Number(value || 0));

export const formatNumber = (value) =>
  new Intl.NumberFormat("vi-VN").format(Number(value || 0));

export const formatPercent = (value) => `${Number(value || 0).toFixed(1)}%`;

export const employeeCode = (id) => `EMP${String(id).padStart(3, "0")}`;

export const toOptionalNumber = (value) =>
  value === "" || value === null || value === undefined ? null : Number(value);

export const displayText = (value, fallback = "-") =>
  value === null || value === undefined || value === "" ? fallback : value;
