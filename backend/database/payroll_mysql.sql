-- =====================================================
-- DATABASE: payroll_db (MySQL)
-- Chứa: salaries, attendance, alerts
-- Dùng cho: HR Management System - Payroll data
-- =====================================================

CREATE DATABASE IF NOT EXISTS payroll_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE payroll_db;

-- =====================================================
-- Drop tables (nếu tồn tại)
-- =====================================================
DROP TABLE IF EXISTS alerts;
DROP TABLE IF EXISTS salaries;
DROP TABLE IF EXISTS attendance;

-- =====================================================
-- 1. Bảng attendance (chấm công)
-- employee_id tham chiếu employees trong HumanDB (SQL Server)
-- Không có FK constraint vì cross-database
-- =====================================================
CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    work_days INT NOT NULL,
    absent_days INT DEFAULT 0,
    leave_days INT DEFAULT 0,
    late_days INT DEFAULT 0,
    attendance_month DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee_id (employee_id),
    INDEX idx_attendance_month (attendance_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 2. Bảng salaries (bảng lương)
-- employee_id tham chiếu employees trong HumanDB (SQL Server)
-- =====================================================
CREATE TABLE salaries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    salary_month DATE NOT NULL,
    base_salary DECIMAL(12,2) NOT NULL,
    bonus DECIMAL(12,2) DEFAULT 0.00,
    deductions DECIMAL(12,2) DEFAULT 0.00,
    net_salary DECIMAL(12,2) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee_id (employee_id),
    INDEX idx_salary_month (salary_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 3. Bảng alerts (cảnh báo)
-- employee_id tham chiếu employees trong HumanDB (SQL Server)
-- =====================================================
CREATE TABLE alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    alert_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL DEFAULT 'warning',
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_employee_id (employee_id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_is_read (is_read)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- SEED DATA
-- =====================================================

-- Attendance (tháng 3 & 4/2026)
INSERT INTO attendance (employee_id, work_days, absent_days, leave_days, late_days, attendance_month) VALUES
-- March 2026
(1,  22, 0, 0, 0, '2026-03-01'),
(2,  21, 1, 0, 0, '2026-03-01'),
(3,  23, 0, 0, 0, '2026-03-01'),
(4,  22, 0, 0, 0, '2026-03-01'),
(5,  18, 3, 1, 0, '2026-03-01'),
(6,  22, 0, 0, 0, '2026-03-01'),
(7,  22, 0, 0, 0, '2026-03-01'),
(8,  20, 1, 0, 0, '2026-03-01'),
(9,  17, 0, 2, 0, '2026-03-01'),
(10, 22, 0, 0, 0, '2026-03-01'),
-- April 2026
(1,  20, 1, 1, 0, '2026-04-01'),
(2,  22, 0, 0, 0, '2026-04-01'),
(3,  21, 1, 0, 1, '2026-04-01'),
(4,  19, 2, 1, 0, '2026-04-01'),
(5,  14, 7, 1, 0, '2026-04-01'),
(6,  23, 0, 0, 0, '2026-04-01'),
(7,  22, 0, 0, 0, '2026-04-01'),
(8,  17, 4, 0, 1, '2026-04-01'),
(9,  16, 0, 3, 0, '2026-04-01'),
(10, 21, 1, 0, 0, '2026-04-01');

-- Salaries (tháng 3 & 4/2026)
INSERT INTO salaries (employee_id, salary_month, base_salary, bonus, deductions, net_salary) VALUES
-- March 2026
(1,  '2026-03-01', 12000000, 500000,  200000, 12300000),
(2,  '2026-03-01', 10000000, 800000,  100000, 10700000),
(3,  '2026-03-01', 15000000, 600000,       0, 15600000),
(4,  '2026-03-01', 11000000, 400000,  100000, 11300000),
(5,  '2026-03-01',  9000000,      0,  300000,  8700000),
(6,  '2026-03-01',  9500000, 500000,       0, 10000000),
(7,  '2026-03-01', 18000000, 1000000,      0, 19000000),
(8,  '2026-03-01',  7000000, 200000,       0,  7200000),
(9,  '2026-03-01',  5000000,      0,       0,  5000000),
(10, '2026-03-01',  8500000, 300000,  100000,  8700000),
-- April 2026
(1,  '2026-04-01', 12000000, 600000,  200000, 12400000),
(2,  '2026-04-01', 10000000, 900000,  100000, 10800000),
(3,  '2026-04-01', 15000000, 700000,       0, 15700000),
(4,  '2026-04-01', 11000000, 300000,  200000, 11100000),
(5,  '2026-04-01',  9000000,      0,  500000,  8500000),
(6,  '2026-04-01',  9500000, 600000,       0, 10100000),
(7,  '2026-04-01', 18000000, 1200000,      0, 19200000),
(8,  '2026-04-01',  7000000, 300000,       0,  7300000),
(9,  '2026-04-01',  5000000, 100000,       0,  5100000),
(10, '2026-04-01',  8500000, 400000,  100000,  8800000);

-- =====================================================
-- VERIFY
-- =====================================================
SELECT 'attendance' AS tbl, COUNT(*) AS cnt FROM attendance
UNION ALL SELECT 'salaries', COUNT(*) FROM salaries
UNION ALL SELECT 'alerts', COUNT(*) FROM alerts
ORDER BY tbl;
