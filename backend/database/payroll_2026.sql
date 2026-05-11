-- MySQL version (payroll_2026.sql)
-- Source: payroll_2026 database

-- ----------------------------
-- Drop tables in correct order (FK dependencies)
-- ----------------------------
DROP TABLE IF EXISTS salaries;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS employees_payroll;
DROP TABLE IF EXISTS positions_payroll;
DROP TABLE IF EXISTS departments_payroll;

-- ----------------------------
-- Table structure for departments_payroll
-- ----------------------------
CREATE TABLE departments_payroll (
  DepartmentID INT PRIMARY KEY,
  DepartmentName VARCHAR(100) NOT NULL,
  SyncedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of departments_payroll
-- ----------------------------
INSERT INTO departments_payroll (DepartmentID, DepartmentName, SyncedAt) VALUES
(1, 'Phòng Nhân sự', '2025-10-20 19:13:03'),
(2, 'Phòng Kế toán', '2025-10-20 19:13:03'),
(3, 'Phòng Kỹ thuật', '2025-10-20 19:13:03'),
(4, 'Phòng Kinh doanh', '2025-10-20 19:13:03'),
(5, 'Phòng Hành chính', '2025-10-20 19:13:03'),
(6, 'Phòng Marketing', '2025-10-20 19:13:03'),
(7, 'Phòng Sản xuất', '2025-10-20 19:13:03'),
(8, 'Phòng Bảo trì', '2025-10-20 19:13:03'),
(9, 'Phòng Nghiên cứu & Phát triển', '2025-10-20 19:13:03'),
(10, 'Phòng Dịch vụ khách hàng', '2025-10-20 19:13:03');

-- ----------------------------
-- Table structure for positions_payroll
-- ----------------------------
CREATE TABLE positions_payroll (
  PositionID INT PRIMARY KEY,
  PositionName VARCHAR(100) NOT NULL,
  SyncedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of positions_payroll
-- ----------------------------
INSERT INTO positions_payroll (PositionID, PositionName, SyncedAt) VALUES
(1, 'Nhân viên', '2025-10-20 19:13:03'),
(2, 'Trưởng nhóm', '2025-10-20 19:13:03'),
(3, 'Phó phòng', '2025-10-20 19:13:03'),
(4, 'Trưởng phòng', '2025-10-20 19:13:03'),
(5, 'Giám đốc', '2025-10-20 19:13:03'),
(6, 'Thư ký', '2025-10-20 19:13:03'),
(7, 'Kỹ sư', '2025-10-20 19:13:03'),
(8, 'Nhân viên thử việc', '2025-10-20 19:13:03'),
(9, 'Thực tập sinh', '2025-10-20 19:13:03'),
(10, 'Cố vấn kỹ thuật', '2025-10-20 19:13:03');

-- ----------------------------
-- Table structure for employees_payroll
-- ----------------------------
CREATE TABLE employees_payroll (
  EmployeeID INT PRIMARY KEY,
  FullName VARCHAR(100) NOT NULL,
  DepartmentID INT,
  PositionID INT,
  Status VARCHAR(50),
  SyncedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (DepartmentID) REFERENCES departments_payroll(DepartmentID),
  FOREIGN KEY (PositionID) REFERENCES positions_payroll(PositionID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of employees_payroll
-- ----------------------------
INSERT INTO employees_payroll (EmployeeID, FullName, DepartmentID, PositionID, Status, SyncedAt) VALUES
(1, 'Nguyễn Văn An', 1, 1, 'Đang làm việc', '2025-10-20 19:13:03'),
(2, 'Lê Thị Bình', 2, 3, 'Đang làm việc', '2025-10-20 19:13:03'),
(3, 'Trần Quốc Cường', 3, 7, 'Đang làm việc', '2025-10-20 19:13:03'),
(4, 'Phạm Hồng Dung', 4, 2, 'Đang làm việc', '2025-10-20 19:13:03'),
(5, 'Võ Thành Đạt', 5, 4, 'Nghỉ phép', '2025-10-20 19:13:03'),
(6, 'Đặng Minh Hạnh', 6, 1, 'Đang làm việc', '2025-10-20 19:13:03'),
(7, 'Lưu Trung Hiếu', 7, 5, 'Đang làm việc', '2025-10-20 19:13:03'),
(8, 'Ngô Thu Lan', 8, 8, 'Thử việc', '2025-10-20 19:13:03'),
(9, 'Bùi Văn Minh', 9, 9, 'Thực tập', '2025-10-20 19:13:03'),
(10, 'Hoàng Thị Oanh', 10, 6, 'Đang làm việc', '2025-10-20 19:13:03');

-- ----------------------------
-- Table structure for attendance
-- ----------------------------
CREATE TABLE attendance (
  AttendanceID INT AUTO_INCREMENT PRIMARY KEY,
  EmployeeID INT,
  WorkDays INT NOT NULL,
  AbsentDays INT DEFAULT 0,
  LeaveDays INT DEFAULT 0,
  AttendanceMonth DATE NOT NULL,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (EmployeeID) REFERENCES employees_payroll(EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of attendance
-- ----------------------------
INSERT INTO attendance (AttendanceID, EmployeeID, WorkDays, AbsentDays, LeaveDays, AttendanceMonth, CreatedAt) VALUES
(1,  1, 22, 1, 0, '2024-09-01', '2025-10-20 19:13:03'),
(2,  2, 21, 0, 1, '2024-09-01', '2025-10-20 19:13:03'),
(3,  3, 23, 0, 0, '2024-09-01', '2025-10-20 19:13:03'),
(4,  4, 22, 2, 0, '2024-09-01', '2025-10-20 19:13:03'),
(5,  5, 18, 3, 2, '2024-09-01', '2025-10-20 19:13:03'),
(6,  6, 24, 0, 0, '2024-09-01', '2025-10-20 19:13:03'),
(7,  7, 20, 1, 1, '2024-09-01', '2025-10-20 19:13:03'),
(8,  8, 19, 2, 0, '2024-09-01', '2025-10-20 19:13:03'),
(9,  9, 16, 0, 2, '2024-09-01', '2025-10-20 19:13:03'),
(10, 10, 22, 1, 0, '2024-09-01', '2025-10-20 19:13:03'),
(11, 1,  22, 1, 0, '2024-09-01', '2025-10-20 19:14:40'),
(12, 2,  21, 0, 1, '2024-09-01', '2025-10-20 19:14:40'),
(13, 3,  23, 0, 0, '2024-09-01', '2025-10-20 19:14:40'),
(14, 4,  22, 2, 0, '2024-09-01', '2025-10-20 19:14:40'),
(15, 5,  18, 3, 2, '2024-09-01', '2025-10-20 19:14:40'),
(16, 6,  24, 0, 0, '2024-09-01', '2025-10-20 19:14:40'),
(17, 7,  20, 1, 1, '2024-09-01', '2025-10-20 19:14:40'),
(18, 8,  19, 2, 0, '2024-09-01', '2025-10-20 19:14:40'),
(19, 9,  16, 0, 2, '2024-09-01', '2025-10-20 19:14:40'),
(20, 10, 22, 1, 0, '2024-09-01', '2025-10-20 19:14:40');

-- ----------------------------
-- Table structure for salaries
-- ----------------------------
CREATE TABLE salaries (
  SalaryID INT AUTO_INCREMENT PRIMARY KEY,
  EmployeeID INT,
  SalaryMonth DATE NOT NULL,
  BaseSalary DECIMAL(12,2) NOT NULL,
  Bonus DECIMAL(12,2) DEFAULT 0.00,
  Deductions DECIMAL(12,2) DEFAULT 0.00,
  NetSalary DECIMAL(12,2) NOT NULL,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (EmployeeID) REFERENCES employees_payroll(EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of salaries
-- ----------------------------
INSERT INTO salaries (SalaryID, EmployeeID, SalaryMonth, BaseSalary, Bonus, Deductions, NetSalary, CreatedAt) VALUES
(1,  1,  '2024-09-01', 12000000.00, 500000.00, 200000.00, 12300000.00, '2025-10-20 19:13:03'),
(2,  2,  '2024-09-01', 10000000.00, 800000.00, 100000.00, 10700000.00, '2025-10-20 19:13:03'),
(3,  3,  '2024-09-01', 15000000.00, 600000.00,      0.00, 15600000.00, '2025-10-20 19:13:03'),
(4,  4,  '2024-09-01', 11000000.00, 400000.00, 100000.00, 11300000.00, '2025-10-20 19:13:03'),
(5,  5,  '2024-09-01',  9000000.00,      0.00, 300000.00,  8700000.00, '2025-10-20 19:13:03'),
(6,  6,  '2024-09-01',  9500000.00, 500000.00,      0.00, 10000000.00, '2025-10-20 19:13:03'),
(7,  7,  '2024-09-01', 18000000.00, 1000000.00,     0.00, 19000000.00, '2025-10-20 19:13:03'),
(8,  8,  '2024-09-01',  7000000.00, 200000.00,      0.00,  7200000.00, '2025-10-20 19:13:03'),
(9,  9,  '2024-09-01',  5000000.00,      0.00,      0.00,  5000000.00, '2025-10-20 19:13:03'),
(10, 10, '2024-09-01',  8500000.00, 300000.00, 100000.00,  8700000.00, '2025-10-20 19:13:03'),
(11, 1,  '2024-09-01', 12000000.00, 500000.00, 200000.00, 12300000.00, '2025-10-20 19:15:00'),
(12, 2,  '2024-09-01', 10000000.00, 800000.00, 100000.00, 10700000.00, '2025-10-20 19:15:00'),
(13, 3,  '2024-09-01', 15000000.00, 600000.00,      0.00, 15600000.00, '2025-10-20 19:15:00'),
(14, 4,  '2024-09-01', 11000000.00, 400000.00, 100000.00, 11300000.00, '2025-10-20 19:15:00'),
(15, 5,  '2024-09-01',  9000000.00,      0.00, 300000.00,  8700000.00, '2025-10-20 19:15:00'),
(16, 6,  '2024-09-01',  9500000.00, 500000.00,      0.00, 10000000.00, '2025-10-20 19:15:00'),
(17, 7,  '2024-09-01', 18000000.00, 1000000.00,     0.00, 19000000.00, '2025-10-20 19:15:00'),
(18, 8,  '2024-09-01',  7000000.00, 200000.00,      0.00,  7200000.00, '2025-10-20 19:15:00'),
(19, 9,  '2024-09-01',  5000000.00,      0.00,      0.00,  5000000.00, '2025-10-20 19:15:00'),
(20, 10, '2024-09-01',  8500000.00, 300000.00, 100000.00,  8700000.00, '2025-10-20 19:15:00');
