-- =====================================================
-- DATABASE: HumanDB (SQL Server)
-- Chứa: departments, positions, employees, dividends
-- Dùng cho: HR Management System - Human resource data
-- =====================================================

-- Tạo database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'HumanDB')
BEGIN
    CREATE DATABASE HumanDB;
END
GO

USE HumanDB;
GO

-- =====================================================
-- Drop tables (nếu tồn tại) theo thứ tự FK
-- =====================================================
IF OBJECT_ID('dividends', 'U') IS NOT NULL DROP TABLE dividends;
IF OBJECT_ID('employees', 'U') IS NOT NULL DROP TABLE employees;
IF OBJECT_ID('positions', 'U') IS NOT NULL DROP TABLE positions;
IF OBJECT_ID('departments', 'U') IS NOT NULL DROP TABLE departments;
GO

-- =====================================================
-- 1. Bảng departments
-- =====================================================
CREATE TABLE departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    department_name NVARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

-- =====================================================
-- 2. Bảng positions
-- =====================================================
CREATE TABLE positions (
    id INT IDENTITY(1,1) PRIMARY KEY,
    position_name NVARCHAR(100) NOT NULL UNIQUE,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);
GO

-- =====================================================
-- 3. Bảng employees
-- =====================================================
CREATE TABLE employees (
    id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender NVARCHAR(10) NOT NULL,
    phone_number NVARCHAR(20) NULL,
    email NVARCHAR(100) UNIQUE NOT NULL,
    hire_date DATE NOT NULL,
    department_id INT NOT NULL,
    position_id INT NOT NULL,
    status NVARCHAR(50) DEFAULT N'Đang làm việc',
    is_deleted BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (position_id) REFERENCES positions(id)
);
GO

-- Index cho các cột thường query
CREATE INDEX IX_employees_department_id ON employees(department_id);
CREATE INDEX IX_employees_position_id ON employees(position_id);
CREATE INDEX IX_employees_status ON employees(status);
GO

-- =====================================================
-- 4. Bảng dividends
-- =====================================================
CREATE TABLE dividends (
    id INT IDENTITY(1,1) PRIMARY KEY,
    employee_id INT NOT NULL,
    dividend_amount DECIMAL(12,2) NOT NULL,
    dividend_date DATE NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
GO

CREATE INDEX IX_dividends_employee_id ON dividends(employee_id);
GO

-- =====================================================
-- SEED DATA
-- =====================================================

-- Departments (10 phòng ban)
SET IDENTITY_INSERT departments ON;
INSERT INTO departments (id, department_name) VALUES
(1, N'Phòng Nhân sự'),
(2, N'Phòng Kế toán'),
(3, N'Phòng Kỹ thuật'),
(4, N'Phòng Kinh doanh'),
(5, N'Phòng Hành chính'),
(6, N'Phòng Marketing'),
(7, N'Phòng Sản xuất'),
(8, N'Phòng Bảo trì'),
(9, N'Phòng Nghiên cứu & Phát triển'),
(10, N'Phòng Dịch vụ khách hàng');
SET IDENTITY_INSERT departments OFF;
GO

-- Positions (10 chức vụ)
SET IDENTITY_INSERT positions ON;
INSERT INTO positions (id, position_name) VALUES
(1, N'Nhân viên'),
(2, N'Trưởng nhóm'),
(3, N'Phó phòng'),
(4, N'Trưởng phòng'),
(5, N'Giám đốc'),
(6, N'Thư ký'),
(7, N'Kỹ sư'),
(8, N'Nhân viên thử việc'),
(9, N'Thực tập sinh'),
(10, N'Cố vấn kỹ thuật');
SET IDENTITY_INSERT positions OFF;
GO

-- Employees (10 nhân viên)
SET IDENTITY_INSERT employees ON;
INSERT INTO employees (id, full_name, date_of_birth, gender, phone_number, email, hire_date, department_id, position_id, status, is_deleted) VALUES
(1,  N'Nguyễn Văn An',     '1990-02-15', N'Nam', '0901234567', 'an.nguyen@company.vn',  '2020-01-10', 1,  1, N'Đang làm việc', 0),
(2,  N'Lê Thị Bình',       '1992-05-22', N'Nữ',  '0912345678', 'binh.le@company.vn',    '2019-03-12', 2,  3, N'Đang làm việc', 0),
(3,  N'Trần Quốc Cường',   '1988-11-10', N'Nam', '0987654321', 'cuong.tran@company.vn', '2021-05-05', 3,  7, N'Đang làm việc', 0),
(4,  N'Phạm Hồng Dung',    '1995-06-08', N'Nữ',  '0934567890', 'dung.pham@company.vn',  '2022-02-01', 4,  2, N'Đang làm việc', 0),
(5,  N'Võ Thành Đạt',      '1991-09-19', N'Nam', '0945678901', 'dat.vo@company.vn',     '2018-07-20', 5,  4, N'Nghỉ phép',     0),
(6,  N'Đặng Minh Hạnh',    '1996-04-25', N'Nữ',  '0976543210', 'hanh.dang@company.vn',  '2023-01-01', 6,  1, N'Đang làm việc', 0),
(7,  N'Lưu Trung Hiếu',    '1993-03-30', N'Nam', '0956789012', 'hieu.luu@company.vn',   '2017-09-15', 7,  5, N'Đang làm việc', 0),
(8,  N'Ngô Thu Lan',        '1998-12-12', N'Nữ',  '0901122334', 'lan.ngo@company.vn',    '2024-03-03', 8,  8, N'Thử việc',      0),
(9,  N'Bùi Văn Minh',       '1989-10-05', N'Nam', '0933111222', 'minh.bui@company.vn',   '2016-11-11', 9,  9, N'Thực tập',      0),
(10, N'Hoàng Thị Oanh',     '1994-07-17', N'Nữ',  '0909988776', 'oanh.hoang@company.vn', '2020-06-01', 10, 6, N'Đang làm việc', 0);
SET IDENTITY_INSERT employees OFF;
GO

-- Dividends (cuối năm 2024)
INSERT INTO dividends (employee_id, dividend_amount, dividend_date) VALUES
(1,  500000.00, '2024-12-31'),
(2,  800000.00, '2024-12-31'),
(3,  300000.00, '2024-12-31'),
(4,  700000.00, '2024-12-31'),
(5,  400000.00, '2024-12-31'),
(6,  600000.00, '2024-12-31'),
(7,  900000.00, '2024-12-31'),
(8,  200000.00, '2024-12-31'),
(9,  150000.00, '2024-12-31'),
(10, 850000.00, '2024-12-31');
GO

-- =====================================================
-- VERIFY
-- =====================================================
SELECT 'departments' AS tbl, COUNT(*) AS cnt FROM departments
UNION ALL SELECT 'positions', COUNT(*) FROM positions
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'dividends', COUNT(*) FROM dividends
ORDER BY tbl;
GO

PRINT '=== HumanDB created and seeded successfully ===';
GO
