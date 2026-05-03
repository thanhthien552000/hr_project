
### SERVICE
Service = Service = tầng xử lý logic nghiệp vụ. Nó là cầu nối giữa API và Repository:

API (route) → Service (logic) → Repository (DB) → Database
              ↑
              ├─ Validate dữ liệu
              ├─ Kiểm tra business rule (vd: email trùng?)
              ├─ Convert schema → model
              ├─ Convert model → dict response
              ├─ Tính toán (vd: % thay đổi lương)
              └─ Throw exception khi lỗi

Tại sao tách Service ra khỏi API?
- Tach Service giúp tách biệt rõ ràng giữa phần xử lý logic nghiệp vụ và phần định nghĩa API. Điều này giúp code dễ bảo trì, dễ test và tái sử dụng hơn.
- Nếu để logic nghiệp vụ trong API, khi có thay đổi về logic sẽ ảnh hưởng trực tiếp
- API chịu trách nhiệm nhận request và trả về response, trong khi Service chịu trách nhiệm xử lý logic nghiệp vụ. Điều này giúp code trở nên modular và dễ dàng mở rộng trong tương lai.



# Tổng quan kiến trúc:
Client (Browser/Postman)
    │
    │  HTTP Request: GET /api/v1/employees?page=1&page_size=10
    ▼
┌─────────────────────────────────────────────┐
│  1. FASTAPI APP (main.py)                   │  ← Nhận request, routing
│     └─ Router (api/v1/...)                  │
├─────────────────────────────────────────────┤
│  2. SERVICE (services/employee.py)          │  ← Xử lý logic nghiệp vụ
├─────────────────────────────────────────────┤
│  3. REPOSITORY (repositories/employee.py)   │  ← Truy vấn database
├─────────────────────────────────────────────┤
│  4. MODEL (models/employee.py)              │  ← Định nghĩa bảng trong DB
├─────────────────────────────────────────────┤
│  5. DATABASE (PostgreSQL)                   │  ← Nơi lưu dữ liệu thật
└─────────────────────────────────────────────┘
    │
    ▼
Client nhận JSON Response