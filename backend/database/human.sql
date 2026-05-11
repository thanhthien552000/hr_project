-- MySQL version - converted from PostgreSQL (human.sql)
-- Source: HUMAN database

-- ----------------------------
-- Drop tables in correct order (FK dependencies)
-- ----------------------------
DROP TABLE IF EXISTS Dividends;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Positions;
DROP TABLE IF EXISTS Departments;

-- ----------------------------
-- Table structure for Departments
-- ----------------------------
CREATE TABLE Departments (
  DepartmentID INT AUTO_INCREMENT PRIMARY KEY,
  DepartmentName VARCHAR(100) NOT NULL,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of Departments
-- ----------------------------
INSERT INTO Departments (DepartmentID, DepartmentName, CreatedAt, UpdatedAt) VALUES
(1, 'Phòng Nhân sự', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(2, 'Phòng Kế toán', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(3, 'Phòng Kỹ thuật', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(4, 'Phòng Kinh doanh', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(5, 'Phòng Hành chính', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(6, 'Phòng Marketing', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(7, 'Phòng Sản xuất', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(8, 'Phòng Bảo trì', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(9, 'Phòng Nghiên cứu & Phát triển', '2025-10-20 19:10:57', '2025-10-20 19:10:57'),
(10, 'Phòng Dịch vụ khách hàng', '2025-10-20 19:10:57', '2025-10-20 19:10:57');

-- ----------------------------
-- Table structure for Positions
-- ----------------------------
CREATE TABLE Positions (
  PositionID INT AUTO_INCREMENT PRIMARY KEY,
  PositionName VARCHAR(100) NOT NULL,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of Positions
-- ----------------------------
INSERT INTO Positions (PositionID, PositionName, CreatedAt, UpdatedAt) VALUES
(1, 'Nhân viên', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(2, 'Trưởng nhóm', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(3, 'Phó phòng', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(4, 'Trưởng phòng', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(5, 'Giám đốc', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(6, 'Thư ký', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(7, 'Kỹ sư', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(8, 'Nhân viên thử việc', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(9, 'Thực tập sinh', '2025-10-20 19:11:34', '2025-10-20 19:11:34'),
(10, 'Cố vấn kỹ thuật', '2025-10-20 19:11:34', '2025-10-20 19:11:34');

-- ----------------------------
-- Table structure for Employees
-- ----------------------------
CREATE TABLE Employees (
  EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
  FullName VARCHAR(100) NOT NULL,
  DateOfBirth DATE NOT NULL,
  Gender VARCHAR(10),
  PhoneNumber VARCHAR(15),
  Email VARCHAR(100) UNIQUE,
  HireDate DATE NOT NULL,
  DepartmentID INT,
  PositionID INT,
  Status VARCHAR(50),
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
  FOREIGN KEY (PositionID) REFERENCES Positions(PositionID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of Employees
-- ----------------------------
INSERT INTO Employees (EmployeeID, FullName, DateOfBirth, Gender, PhoneNumber, Email, HireDate, DepartmentID, PositionID, Status, CreatedAt, UpdatedAt) VALUES
(1, 'Nguyễn Văn An', '1990-02-15', 'Nam', '0901234567', 'an.nguyen@company.vn', '2020-01-10', 1, 1, 'Đang làm việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(2, 'Lê Thị Bình', '1992-05-22', 'Nữ', '0912345678', 'binh.le@company.vn', '2019-03-12', 2, 3, 'Đang làm việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(3, 'Trần Quốc Cường', '1988-11-10', 'Nam', '0987654321', 'cuong.tran@company.vn', '2021-05-05', 3, 7, 'Đang làm việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(4, 'Phạm Hồng Dung', '1995-06-08', 'Nữ', '0934567890', 'dung.pham@company.vn', '2022-02-01', 4, 2, 'Đang làm việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(5, 'Võ Thành Đạt', '1991-09-19', 'Nam', '0945678901', 'dat.vo@company.vn', '2018-07-20', 5, 4, 'Nghỉ phép', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(6, 'Đặng Minh Hạnh', '1996-04-25', 'Nữ', '0976543210', 'hanh.dang@company.vn', '2023-01-01', 6, 1, 'Đang làm việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(7, 'Lưu Trung Hiếu', '1993-03-30', 'Nam', '0956789012', 'hieu.luu@company.vn', '2017-09-15', 7, 5, 'Đang làm việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(8, 'Ngô Thu Lan', '1998-12-12', 'Nữ', '0901122334', 'lan.ngo@company.vn', '2024-03-03', 8, 8, 'Thử việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(9, 'Bùi Văn Minh', '1989-10-05', 'Nam', '0933111222', 'minh.bui@company.vn', '2016-11-11', 9, 9, 'Thực tập', '2025-10-20 19:11:42', '2025-10-20 19:11:42'),
(10, 'Hoàng Thị Oanh', '1994-07-17', 'Nữ', '0909988776', 'oanh.hoang@company.vn', '2020-06-01', 10, 6, 'Đang làm việc', '2025-10-20 19:11:42', '2025-10-20 19:11:42');

-- ----------------------------
-- Table structure for Dividends
-- ----------------------------
CREATE TABLE Dividends (
  DividendID INT AUTO_INCREMENT PRIMARY KEY,
  EmployeeID INT,
  DividendAmount DECIMAL(12,2) NOT NULL,
  DividendDate DATE NOT NULL,
  CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Records of Dividends
-- ----------------------------
INSERT INTO Dividends (DividendID, EmployeeID, DividendAmount, DividendDate, CreatedAt) VALUES
(1, 1, 500000.00, '2024-12-31', '2025-10-20 19:11:51'),
(2, 2, 800000.00, '2024-12-31', '2025-10-20 19:11:51'),
(3, 3, 300000.00, '2024-12-31', '2025-10-20 19:11:51'),
(4, 4, 700000.00, '2024-12-31', '2025-10-20 19:11:51'),
(5, 5, 400000.00, '2024-12-31', '2025-10-20 19:11:51'),
(6, 6, 600000.00, '2024-12-31', '2025-10-20 19:11:51'),
(7, 7, 900000.00, '2024-12-31', '2025-10-20 19:11:51'),
(8, 8, 200000.00, '2024-12-31', '2025-10-20 19:11:51'),
(9, 9, 150000.00, '2024-12-31', '2025-10-20 19:11:51'),
(10, 10, 850000.00, '2024-12-31', '2025-10-20 19:11:51');
