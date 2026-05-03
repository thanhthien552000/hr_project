"""Quick demo: call 5 API endpoints."""
import httpx
import json
from app.core.security import create_access_token
from datetime import timedelta

token = create_access_token({"sub": 1, "email": "admin@company.vn", "role": "admin"}, expires_delta=timedelta(hours=24))
h = {"Authorization": f"Bearer {token}"}
BASE = "http://localhost:8000"

print("=" * 60)
print("  DEMO: HR Management System API")
print("=" * 60)

# 1
print("\n[1] GET /health")
r = httpx.get(f"{BASE}/health")
print(f"    Status: {r.json()['status']}")

# 2
print("\n[2] GET /api/v1/employees — Danh sách nhân viên")
r = httpx.get(f"{BASE}/api/v1/employees?page_size=10", headers=h)
data = r.json()["data"]
print(f"    Tổng: {data['total']} nhân viên | Trang: {data['page']}/{data['total_pages']}")
for emp in data["items"]:
    print(f"    • [{emp['id']}] {emp['full_name']:20s} | {emp['department_name']:32s} | {emp['status']}")

# 3
print("\n[3] GET /api/v1/dashboard/summary — Tổng quan tháng 4/2026")
r = httpx.get(f"{BASE}/api/v1/dashboard/summary?month=2026-04", headers=h)
d = r.json()["data"]
arrow = "↑" if d["change_direction"] == "up" else "↓"
print(f"    Tổng NV: {d['total_employees']} | Đang làm: {d['active_employees']} | Nghỉ việc: {d['resigned_employees']} | Thay đổi: {arrow} {d['change_percentage']}%")

# 4
print("\n[4] GET /api/v1/status/overview — Biểu đồ trạng thái")
r = httpx.get(f"{BASE}/api/v1/status/overview", headers=h)
sd = r.json()["data"]
print(f"    Tổng: {sd['total_employees']} nhân viên")
for s in sd["statuses"]:
    bar = "█" * int(s["percentage"] / 5)
    print(f"    {s['status']:20s} {s['count']:3d} ({s['percentage']:5.1f}%) {bar}")

# 5
print("\n[5] GET /api/v1/payroll — Lương tháng 4 vs tháng 3")
r = httpx.get(f"{BASE}/api/v1/payroll?month=2026-04&page_size=5", headers=h)
for item in r.json()["data"]["items"]:
    net = f"{int(item['net_salary']):>12,}".replace(",", ".")
    change = ""
    if item.get("previous_month"):
        arrow = "↑" if item["change_direction"] == "up" else "↓"
        change = f" {arrow} {item['change_percentage']}%"
    print(f"    • {item['full_name']:20s} | {net} VND{change}")

print("\n" + "=" * 60)
print("  Swagger UI: http://localhost:8000/docs")
print("=" * 60)
