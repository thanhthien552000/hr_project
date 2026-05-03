### 3. Use Cases theo từng Module

#### Module 1: Dashboard (~5 API)
- UC-D1: Xem tổng số người dùng/nhân viên
- UC-D2: Xem hiệu suất theo tháng (% tăng/giảm so với tháng trước)
- UC-D3: Xem biểu đồ tròn payroll theo phòng ban
- UC-D4: Xem danh sách nhân viên hoạt động gần đây (tên + lương)
- UC-D5: Xem biểu đồ cột nhân viên nghỉ nhiều buổi nhất

#### Module 2: Quản lý Nhân viên (~6 API)
- UC-E1: Xem danh sách nhân viên (filter, search, pagination)
- UC-E2: Xem chi tiết nhân viên
- UC-E3: Thêm nhân viên mới
- UC-E4: Cập nhật thông tin nhân viên
- UC-E5: Xóa nhân viên (soft delete)
- UC-E6: Xuất PDF danh sách nhân viên

#### Module 3: Payroll (~5 API)
- UC-P1: Xem danh sách lương (tên NV + lương tháng trước + lương tháng này)
- UC-P2: Xem chi tiết lương nhân viên
- UC-P3: Tạo bảng lương tháng
- UC-P4: Cập nhật lương nhân viên
- UC-P5: Thống kê lương theo phòng ban

#### Module 4: Attendance (~3 API)
- UC-A1: Xem danh sách chấm công theo tháng
- UC-A2: Tạo/cập nhật chấm công nhân viên
- UC-A3: Thống kê chấm công (tổng ngày đi làm, nghỉ, phép)

#### Module 5: Trạng thái (~1 API)
- UC-S1: Biểu đồ tròn trạng thái NV (đang làm, nghỉ việc, đi làm trễ)

#### Module 6: Cảnh báo (~2 API)
- UC-AL1: Xem danh sách cảnh báo (lương, nghỉ quá nhiều, biến động lương)
- UC-AL2: Tạo/tính toán cảnh báo tự động

### 4. Mối quan hệ giữa Entities