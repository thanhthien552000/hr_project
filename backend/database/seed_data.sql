-- =============================================
-- HR Management - Seed Data (INSERT only)
-- Bảng đã được tạo bởi Alembic migration
-- =============================================

-- 1. Departments (10 phòng ban)
INSERT INTO departments (id, department_name) VALUES
(1, 'Phòng Nhân sự'),
(2, 'Phòng Kế toán'),
(3, 'Phòng Kỹ thuật'),
(4, 'Phòng Kinh doanh'),
(5, 'Phòng Hành chính'),
(6, 'Phòng Marketing'),
(7, 'Phòng Sản xuất'),
(8, 'Phòng Bảo trì'),
(9, 'Phòng Nghiên cứu & Phát triển'),
(10, 'Phòng Dịch vụ khách hàng');
SELECT setval('departments_id_seq', 10);

-- 2. Positions (10 chức vụ)
INSERT INTO positions (id, position_name) VALUES
(1, 'Nhân viên'),
(2, 'Trưởng nhóm'),
(3, 'Phó phòng'),
(4, 'Trưởng phòng'),
(5, 'Giám đốc'),
(6, 'Thư ký'),
(7, 'Kỹ sư'),
(8, 'Nhân viên thử việc'),
(9, 'Thực tập sinh'),
(10, 'Cố vấn kỹ thuật');
SELECT setval('positions_id_seq', 10);

-- 3. Employees (10 nhân viên)
INSERT INTO employees (id, full_name, date_of_birth, gender, phone_number, email, hire_date, department_id, position_id, status, is_deleted) VALUES
(1, 'Nguyễn Văn An', '1990-02-15', 'Nam', '0901234567', 'an.nguyen@company.vn', '2020-01-10', 1, 1, 'Đang làm việc', false),
(2, 'Lê Thị Bình', '1992-05-22', 'Nữ', '0912345678', 'binh.le@company.vn', '2019-03-12', 2, 3, 'Đang làm việc', false),
(3, 'Trần Quốc Cường', '1988-11-10', 'Nam', '0987654321', 'cuong.tran@company.vn', '2021-05-05', 3, 7, 'Đang làm việc', false),
(4, 'Phạm Hồng Dung', '1995-06-08', 'Nữ', '0934567890', 'dung.pham@company.vn', '2022-02-01', 4, 2, 'Đang làm việc', false),
(5, 'Võ Thành Đạt', '1991-09-19', 'Nam', '0945678901', 'dat.vo@company.vn', '2018-07-20', 5, 4, 'Nghỉ phép', false),
(6, 'Đặng Minh Hạnh', '1996-04-25', 'Nữ', '0976543210', 'hanh.dang@company.vn', '2023-01-01', 6, 1, 'Đang làm việc', false),
(7, 'Lưu Trung Hiếu', '1993-03-30', 'Nam', '0956789012', 'hieu.luu@company.vn', '2017-09-15', 7, 5, 'Đang làm việc', false),
(8, 'Ngô Thu Lan', '1998-12-12', 'Nữ', '0901122334', 'lan.ngo@company.vn', '2024-03-03', 8, 8, 'Thử việc', false),
(9, 'Bùi Văn Minh', '1989-10-05', 'Nam', '0933111222', 'minh.bui@company.vn', '2016-11-11', 9, 9, 'Thực tập', false),
(10, 'Hoàng Thị Oanh', '1994-07-17', 'Nữ', '0909988776', 'oanh.hoang@company.vn', '2020-06-01', 10, 6, 'Đang làm việc', false);
SELECT setval('employees_id_seq', 10);

-- 4. Attendance (tháng 3 & 4/2026)
INSERT INTO attendance (employee_id, work_days, absent_days, leave_days, late_days, attendance_month) VALUES
-- March 2026
(1, 22, 0, 0, 0, '2026-03-01'),
(2, 21, 1, 0, 0, '2026-03-01'),
(3, 23, 0, 0, 0, '2026-03-01'),
(4, 22, 0, 0, 0, '2026-03-01'),
(5, 18, 3, 1, 0, '2026-03-01'),
(6, 22, 0, 0, 0, '2026-03-01'),
(7, 22, 0, 0, 0, '2026-03-01'),
(8, 20, 1, 0, 0, '2026-03-01'),
(9, 17, 0, 2, 0, '2026-03-01'),
(10, 22, 0, 0, 0, '2026-03-01'),
-- April 2026
(1, 20, 1, 1, 0, '2026-04-01'),
(2, 22, 0, 0, 0, '2026-04-01'),
(3, 21, 1, 0, 1, '2026-04-01'),
(4, 19, 2, 1, 0, '2026-04-01'),
(5, 14, 7, 1, 0, '2026-04-01'),
(6, 23, 0, 0, 0, '2026-04-01'),
(7, 22, 0, 0, 0, '2026-04-01'),
(8, 17, 4, 0, 1, '2026-04-01'),
(9, 16, 0, 3, 0, '2026-04-01'),
(10, 21, 1, 0, 0, '2026-04-01');

-- 5. Salaries (tháng 3 & 4/2026)
INSERT INTO salaries (employee_id, salary_month, base_salary, bonus, deductions, net_salary) VALUES
-- March 2026
(1, '2026-03-01', 12000000, 500000, 200000, 12300000),
(2, '2026-03-01', 10000000, 800000, 100000, 10700000),
(3, '2026-03-01', 15000000, 600000, 0, 15600000),
(4, '2026-03-01', 11000000, 400000, 100000, 11300000),
(5, '2026-03-01', 9000000, 0, 300000, 8700000),
(6, '2026-03-01', 9500000, 500000, 0, 10000000),
(7, '2026-03-01', 18000000, 1000000, 0, 19000000),
(8, '2026-03-01', 7000000, 200000, 0, 7200000),
(9, '2026-03-01', 5000000, 0, 0, 5000000),
(10, '2026-03-01', 8500000, 300000, 100000, 8700000),
-- April 2026
(1, '2026-04-01', 12000000, 600000, 200000, 12400000),
(2, '2026-04-01', 10000000, 900000, 100000, 10800000),
(3, '2026-04-01', 15000000, 700000, 0, 15700000),
(4, '2026-04-01', 11000000, 300000, 200000, 11100000),
(5, '2026-04-01', 9000000, 0, 500000, 8500000),
(6, '2026-04-01', 9500000, 600000, 0, 10100000),
(7, '2026-04-01', 18000000, 1200000, 0, 19200000),
(8, '2026-04-01', 7000000, 300000, 0, 7300000),
(9, '2026-04-01', 5000000, 100000, 0, 5100000),
(10, '2026-04-01', 8500000, 400000, 100000, 8800000);

-- 6. Dividends (cuối năm 2024)
INSERT INTO dividends (employee_id, dividend_amount, dividend_date) VALUES
(1, 500000, '2024-12-31'),
(2, 800000, '2024-12-31'),
(3, 300000, '2024-12-31'),
(4, 700000, '2024-12-31'),
(5, 400000, '2024-12-31'),
(6, 600000, '2024-12-31'),
(7, 900000, '2024-12-31'),
(8, 200000, '2024-12-31'),
(9, 150000, '2024-12-31'),
(10, 850000, '2024-12-31');

-- =============================================
-- Verify
-- =============================================
SELECT 'departments' AS tbl, COUNT(*) FROM departments
UNION ALL SELECT 'positions', COUNT(*) FROM positions
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'attendance', COUNT(*) FROM attendance
UNION ALL SELECT 'salaries', COUNT(*) FROM salaries
UNION ALL SELECT 'dividends', COUNT(*) FROM dividends
UNION ALL SELECT 'alerts', COUNT(*) FROM alerts
UNION ALL SELECT 'users', COUNT(*) FROM users
ORDER BY tbl;
