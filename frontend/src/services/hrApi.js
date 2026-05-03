const DEFAULT_API_BASE_URL = "http://localhost:8000/api/v1";

export const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || DEFAULT_API_BASE_URL
).replace(/\/$/, "");

class ApiError extends Error {
  constructor(message, status, details) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.details = details;
  }
}

const getStoredToken = () => {
  try {
    return window.localStorage.getItem("hr_access_token");
  } catch {
    return null;
  }
};

const appendParams = (url, params = {}) => {
  Object.entries(params).forEach(([key, value]) => {
    if (value === undefined || value === null || value === "") return;
    url.searchParams.set(key, value);
  });
};

const buildUrl = (path, params) => {
  const cleanPath = path.startsWith("/") ? path.slice(1) : path;
  const url = new URL(`${API_BASE_URL}/${cleanPath}`);
  appendParams(url, params);
  return url;
};

const getErrorMessage = (payload, fallback) => {
  if (payload?.error?.message) return payload.error.message;
  if (typeof payload?.detail === "string") return payload.detail;
  if (Array.isArray(payload?.detail)) {
    return payload.detail
      .map((item) => item.msg || item.message)
      .filter(Boolean)
      .join(", ");
  }
  if (payload?.message && payload.success === false) return payload.message;
  return fallback;
};

const request = async (
  path,
  { method = "GET", params, body, responseType, headers: customHeaders } = {},
) => {
  const headers = new Headers(customHeaders);
  const token = getStoredToken();

  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (body !== undefined && !(body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(buildUrl(path, params), {
    method,
    headers,
    body:
      body === undefined || body instanceof FormData
        ? body
        : JSON.stringify(body),
  });

  if (responseType === "blob") {
    if (!response.ok) {
      throw new ApiError(
        `Request failed with status ${response.status}`,
        response.status,
      );
    }
    return response.blob();
  }

  const payload = await response.json().catch(() => null);

  if (!response.ok || payload?.success === false) {
    throw new ApiError(
      getErrorMessage(payload, `Request failed with status ${response.status}`),
      response.status,
      payload,
    );
  }

  return payload && Object.prototype.hasOwnProperty.call(payload, "data")
    ? payload.data
    : payload;
};

export const dashboardApi = {
  getSummary: (params) => request("/dashboard/summary", { params }),
  getPerformance: (params) => request("/dashboard/performance", { params }),
  getPayrollByDepartment: (params) =>
    request("/dashboard/payroll-by-department", { params }),
  getRecentActivities: (params) =>
    request("/dashboard/recent-activities", { params }),
  getTopAbsentEmployees: (params) =>
    request("/dashboard/top-absent-employees", { params }),
};

export const employeesApi = {
  list: (params) => request("/employees", { params }),
  getById: (employeeId) => request(`/employees/${employeeId}`),
  create: (body) => request("/employees", { method: "POST", body }),
  update: (employeeId, body) =>
    request(`/employees/${employeeId}`, { method: "PUT", body }),
  remove: (employeeId) =>
    request(`/employees/${employeeId}`, { method: "DELETE" }),
  exportPdf: (params) =>
    request("/employees/export/pdf", { params, responseType: "blob" }),
};

export const payrollApi = {
  list: (params) => request("/payroll", { params }),
  getById: (salaryId) => request(`/payroll/${salaryId}`),
  create: (body) => request("/payroll", { method: "POST", body }),
  update: (salaryId, body) =>
    request(`/payroll/${salaryId}`, { method: "PUT", body }),
  statistics: (params) => request("/payroll/statistics", { params }),
};

export const attendanceApi = {
  list: (params) => request("/attendance", { params }),
  create: (body) => request("/attendance", { method: "POST", body }),
  update: (attendanceId, body) =>
    request(`/attendance/${attendanceId}`, { method: "PUT", body }),
};

export const statusApi = {
  overview: () => request("/status/overview"),
};

export const alertsApi = {
  list: (params) => request("/alerts", { params }),
  generate: (params) =>
    request("/alerts/generate", { method: "POST", params }),
};

export const departmentsApi = {
  list: (params) => request("/departments", { params }),
};

export const positionsApi = {
  list: (params) => request("/positions", { params }),
};

export { ApiError };
