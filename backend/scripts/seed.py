"""Seed script to populate database with initial data from the original SQL files."""
import asyncio
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.core.database import Base
from app.core.security import get_password_hash
from app.models import *


async def seed():
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # 1. Seed admin user
        admin = User(
            email="admin@company.vn",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin",
            role="admin",
            is_active=True,
        )
        db.add(admin)

        # 2. Seed Departments
        departments_data = [
            (1, "Phòng Nhân sự"),
            (2, "Phòng Kế toán"),
            (3, "Phòng Kỹ thuật"),
            (4, "Phòng Kinh doanh"),
            (5, "Phòng Hành chính"),
            (6, "Phòng Marketing"),
            (7, "Phòng Sản xuất"),
            (8, "Phòng Bảo trì"),
            (9, "Phòng Nghiên cứu & Phát triển"),
            (10, "Phòng Dịch vụ khách hàng"),
        ]
        for did, name in departments_data:
            db.add(Department(id=did, department_name=name))

        # 3. Seed Positions
        positions_data = [
            (1, "Nhân viên"),
            (2, "Trưởng nhóm"),
            (3, "Phó phòng"),
            (4, "Trưởng phòng"),
            (5, "Giám đốc"),
            (6, "Thư ký"),
            (7, "Kỹ sư"),
            (8, "Nhân viên thử việc"),
            (9, "Thực tập sinh"),
            (10, "Cố vấn kỹ thuật"),
        ]
        for pid, name in positions_data:
            db.add(Position(id=pid, position_name=name))

        await db.flush()

        # 4. Seed Employees
        employees_data = [
            (1, "Nguyễn Văn An", date(1990, 2, 15), "Nam", "0901234567", "an.nguyen@company.vn", date(2020, 1, 10), 1, 1, "Đang làm việc"),
            (2, "Lê Thị Bình", date(1992, 5, 22), "Nữ", "0912345678", "binh.le@company.vn", date(2019, 3, 12), 2, 3, "Đang làm việc"),
            (3, "Trần Quốc Cường", date(1988, 11, 10), "Nam", "0987654321", "cuong.tran@company.vn", date(2021, 5, 5), 3, 7, "Đang làm việc"),
            (4, "Phạm Hồng Dung", date(1995, 6, 8), "Nữ", "0934567890", "dung.pham@company.vn", date(2022, 2, 1), 4, 2, "Đang làm việc"),
            (5, "Võ Thành Đạt", date(1991, 9, 19), "Nam", "0945678901", "dat.vo@company.vn", date(2018, 7, 20), 5, 4, "Nghỉ phép"),
            (6, "Đặng Minh Hạnh", date(1996, 4, 25), "Nữ", "0976543210", "hanh.dang@company.vn", date(2023, 1, 1), 6, 1, "Đang làm việc"),
            (7, "Lưu Trung Hiếu", date(1993, 3, 30), "Nam", "0956789012", "hieu.luu@company.vn", date(2017, 9, 15), 7, 5, "Đang làm việc"),
            (8, "Ngô Thu Lan", date(1998, 12, 12), "Nữ", "0901122334", "lan.ngo@company.vn", date(2024, 3, 3), 8, 8, "Thử việc"),
            (9, "Bùi Văn Minh", date(1989, 10, 5), "Nam", "0933111222", "minh.bui@company.vn", date(2016, 11, 11), 9, 9, "Thực tập"),
            (10, "Hoàng Thị Oanh", date(1994, 7, 17), "Nữ", "0909988776", "oanh.hoang@company.vn", date(2020, 6, 1), 10, 6, "Đang làm việc"),
        ]
        for eid, name, dob, gender, phone, email, hire, dept, pos, status in employees_data:
            db.add(Employee(
                id=eid, full_name=name, date_of_birth=dob, gender=gender,
                phone_number=phone, email=email, hire_date=hire,
                department_id=dept, position_id=pos, status=status,
            ))

        await db.flush()

        # 5. Seed Attendance (tháng 3 & 4 / 2026)
        attendance_data = [
            # March 2026
            (1, 22, 1, 0, 0, date(2026, 3, 1)),
            (2, 21, 0, 1, 0, date(2026, 3, 1)),
            (3, 23, 0, 0, 0, date(2026, 3, 1)),
            (4, 22, 2, 0, 1, date(2026, 3, 1)),
            (5, 18, 3, 2, 0, date(2026, 3, 1)),
            (6, 24, 0, 0, 0, date(2026, 3, 1)),
            (7, 20, 1, 1, 0, date(2026, 3, 1)),
            (8, 19, 2, 0, 1, date(2026, 3, 1)),
            (9, 16, 0, 2, 0, date(2026, 3, 1)),
            (10, 22, 1, 0, 0, date(2026, 3, 1)),
            # April 2026
            (1, 21, 1, 0, 0, date(2026, 4, 1)),
            (2, 22, 0, 0, 0, date(2026, 4, 1)),
            (3, 22, 1, 0, 0, date(2026, 4, 1)),
            (4, 20, 3, 0, 1, date(2026, 4, 1)),
            (5, 15, 6, 2, 0, date(2026, 4, 1)),  # excessive absence
            (6, 23, 0, 0, 0, date(2026, 4, 1)),
            (7, 21, 1, 0, 0, date(2026, 4, 1)),
            (8, 18, 3, 0, 2, date(2026, 4, 1)),
            (9, 17, 1, 1, 0, date(2026, 4, 1)),
            (10, 22, 0, 0, 0, date(2026, 4, 1)),
        ]
        for emp_id, work, absent, leave, late, month in attendance_data:
            db.add(Attendance(
                employee_id=emp_id, work_days=work, absent_days=absent,
                leave_days=leave, late_days=late, attendance_month=month,
            ))

        # 6. Seed Salaries (tháng 3 & 4 / 2026)
        salaries_data = [
            # March 2026
            (1, date(2026, 3, 1), Decimal("12000000"), Decimal("500000"), Decimal("200000"), Decimal("12300000")),
            (2, date(2026, 3, 1), Decimal("10000000"), Decimal("800000"), Decimal("100000"), Decimal("10700000")),
            (3, date(2026, 3, 1), Decimal("15000000"), Decimal("600000"), Decimal("0"), Decimal("15600000")),
            (4, date(2026, 3, 1), Decimal("11000000"), Decimal("400000"), Decimal("100000"), Decimal("11300000")),
            (5, date(2026, 3, 1), Decimal("9000000"), Decimal("0"), Decimal("300000"), Decimal("8700000")),
            (6, date(2026, 3, 1), Decimal("9500000"), Decimal("500000"), Decimal("0"), Decimal("10000000")),
            (7, date(2026, 3, 1), Decimal("18000000"), Decimal("1000000"), Decimal("0"), Decimal("19000000")),
            (8, date(2026, 3, 1), Decimal("7000000"), Decimal("200000"), Decimal("0"), Decimal("7200000")),
            (9, date(2026, 3, 1), Decimal("5000000"), Decimal("0"), Decimal("0"), Decimal("5000000")),
            (10, date(2026, 3, 1), Decimal("8500000"), Decimal("300000"), Decimal("100000"), Decimal("8700000")),
            # April 2026
            (1, date(2026, 4, 1), Decimal("12000000"), Decimal("600000"), Decimal("200000"), Decimal("12400000")),
            (2, date(2026, 4, 1), Decimal("10000000"), Decimal("900000"), Decimal("100000"), Decimal("10800000")),
            (3, date(2026, 4, 1), Decimal("15000000"), Decimal("700000"), Decimal("0"), Decimal("15700000")),
            (4, date(2026, 4, 1), Decimal("11000000"), Decimal("300000"), Decimal("200000"), Decimal("11100000")),
            (5, date(2026, 4, 1), Decimal("9000000"), Decimal("0"), Decimal("500000"), Decimal("8500000")),
            (6, date(2026, 4, 1), Decimal("9500000"), Decimal("600000"), Decimal("0"), Decimal("10100000")),
            (7, date(2026, 4, 1), Decimal("18000000"), Decimal("1200000"), Decimal("0"), Decimal("19200000")),
            (8, date(2026, 4, 1), Decimal("7000000"), Decimal("300000"), Decimal("0"), Decimal("7300000")),
            (9, date(2026, 4, 1), Decimal("5000000"), Decimal("100000"), Decimal("0"), Decimal("5100000")),
            (10, date(2026, 4, 1), Decimal("8500000"), Decimal("400000"), Decimal("100000"), Decimal("8800000")),
        ]
        for emp_id, month, base, bonus, deduct, net in salaries_data:
            db.add(Salary(
                employee_id=emp_id, salary_month=month, base_salary=base,
                bonus=bonus, deductions=deduct, net_salary=net,
            ))

        # 7. Seed Dividends
        dividends_data = [
            (1, Decimal("500000"), date(2024, 12, 31)),
            (2, Decimal("800000"), date(2024, 12, 31)),
            (3, Decimal("300000"), date(2024, 12, 31)),
            (4, Decimal("700000"), date(2024, 12, 31)),
            (5, Decimal("400000"), date(2024, 12, 31)),
        ]
        for emp_id, amount, div_date in dividends_data:
            db.add(Dividend(
                employee_id=emp_id, dividend_amount=amount, dividend_date=div_date,
            ))

        await db.commit()
        print("✅ Seed data completed successfully!")
        print("   - 1 admin user (admin@company.vn / admin123)")
        print("   - 10 departments")
        print("   - 10 positions")
        print("   - 10 employees")
        print("   - 20 attendance records (March & April 2026)")
        print("   - 20 salary records (March & April 2026)")
        print("   - 5 dividends")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
