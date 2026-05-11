"""
Seed script — import initial data into MySQL.
Run: python scripts/seed_data.py
"""
import asyncio
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.core.database import Base
from app.core.security import get_password_hash
from app.models import *  # noqa


# ── Raw data from human.sql & payroll_2026.sql ────────────────────────

DEPARTMENTS = [
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

POSITIONS = [
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

EMPLOYEES = [
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

ATTENDANCE = [
    (1, 22, 1, 0, 0, date(2024, 9, 1)),
    (2, 21, 0, 1, 0, date(2024, 9, 1)),
    (3, 23, 0, 0, 0, date(2024, 9, 1)),
    (4, 22, 2, 0, 0, date(2024, 9, 1)),
    (5, 18, 3, 2, 0, date(2024, 9, 1)),
    (6, 24, 0, 0, 0, date(2024, 9, 1)),
    (7, 20, 1, 1, 0, date(2024, 9, 1)),
    (8, 19, 2, 0, 0, date(2024, 9, 1)),
    (9, 16, 0, 2, 0, date(2024, 9, 1)),
    (10, 22, 1, 0, 0, date(2024, 9, 1)),
    # Extra month for comparison — Oct 2024
    (1, 21, 2, 0, 1, date(2024, 10, 1)),
    (2, 22, 0, 0, 0, date(2024, 10, 1)),
    (3, 22, 1, 0, 0, date(2024, 10, 1)),
    (4, 20, 3, 0, 1, date(2024, 10, 1)),
    (5, 15, 6, 2, 0, date(2024, 10, 1)),
    (6, 23, 0, 0, 0, date(2024, 10, 1)),
    (7, 21, 1, 0, 0, date(2024, 10, 1)),
    (8, 18, 3, 0, 1, date(2024, 10, 1)),
    (9, 17, 0, 3, 0, date(2024, 10, 1)),
    (10, 22, 0, 0, 0, date(2024, 10, 1)),
    # April 2026 (current month)
    (1, 20, 1, 1, 0, date(2026, 4, 1)),
    (2, 22, 0, 0, 0, date(2026, 4, 1)),
    (3, 21, 1, 0, 1, date(2026, 4, 1)),
    (4, 19, 2, 1, 0, date(2026, 4, 1)),
    (5, 14, 7, 1, 0, date(2026, 4, 1)),
    (6, 23, 0, 0, 0, date(2026, 4, 1)),
    (7, 22, 0, 0, 0, date(2026, 4, 1)),
    (8, 17, 4, 0, 1, date(2026, 4, 1)),
    (9, 16, 0, 3, 0, date(2026, 4, 1)),
    (10, 21, 1, 0, 0, date(2026, 4, 1)),
    # March 2026 (for performance comparison)
    (1, 22, 0, 0, 0, date(2026, 3, 1)),
    (2, 21, 1, 0, 0, date(2026, 3, 1)),
    (3, 23, 0, 0, 0, date(2026, 3, 1)),
    (4, 22, 0, 0, 0, date(2026, 3, 1)),
    (5, 18, 3, 1, 0, date(2026, 3, 1)),
    (6, 22, 0, 0, 0, date(2026, 3, 1)),
    (7, 22, 0, 0, 0, date(2026, 3, 1)),
    (8, 20, 1, 0, 0, date(2026, 3, 1)),
    (9, 17, 0, 2, 0, date(2026, 3, 1)),
    (10, 22, 0, 0, 0, date(2026, 3, 1)),
]

SALARIES = [
    # Sep 2024
    (1, date(2024, 9, 1), Decimal("12000000"), Decimal("500000"), Decimal("200000"), Decimal("12300000")),
    (2, date(2024, 9, 1), Decimal("10000000"), Decimal("800000"), Decimal("100000"), Decimal("10700000")),
    (3, date(2024, 9, 1), Decimal("15000000"), Decimal("600000"), Decimal("0"), Decimal("15600000")),
    (4, date(2024, 9, 1), Decimal("11000000"), Decimal("400000"), Decimal("100000"), Decimal("11300000")),
    (5, date(2024, 9, 1), Decimal("9000000"), Decimal("0"), Decimal("300000"), Decimal("8700000")),
    (6, date(2024, 9, 1), Decimal("9500000"), Decimal("500000"), Decimal("0"), Decimal("10000000")),
    (7, date(2024, 9, 1), Decimal("18000000"), Decimal("1000000"), Decimal("0"), Decimal("19000000")),
    (8, date(2024, 9, 1), Decimal("7000000"), Decimal("200000"), Decimal("0"), Decimal("7200000")),
    (9, date(2024, 9, 1), Decimal("5000000"), Decimal("0"), Decimal("0"), Decimal("5000000")),
    (10, date(2024, 9, 1), Decimal("8500000"), Decimal("300000"), Decimal("100000"), Decimal("8700000")),
    # Mar 2026
    (1, date(2026, 3, 1), Decimal("13000000"), Decimal("600000"), Decimal("200000"), Decimal("13400000")),
    (2, date(2026, 3, 1), Decimal("10500000"), Decimal("700000"), Decimal("100000"), Decimal("11100000")),
    (3, date(2026, 3, 1), Decimal("16000000"), Decimal("800000"), Decimal("0"), Decimal("16800000")),
    (4, date(2026, 3, 1), Decimal("12000000"), Decimal("500000"), Decimal("100000"), Decimal("12400000")),
    (5, date(2026, 3, 1), Decimal("9500000"), Decimal("0"), Decimal("300000"), Decimal("9200000")),
    (6, date(2026, 3, 1), Decimal("10000000"), Decimal("400000"), Decimal("0"), Decimal("10400000")),
    (7, date(2026, 3, 1), Decimal("19000000"), Decimal("1200000"), Decimal("0"), Decimal("20200000")),
    (8, date(2026, 3, 1), Decimal("7500000"), Decimal("200000"), Decimal("0"), Decimal("7700000")),
    (9, date(2026, 3, 1), Decimal("5500000"), Decimal("0"), Decimal("0"), Decimal("5500000")),
    (10, date(2026, 3, 1), Decimal("9000000"), Decimal("400000"), Decimal("100000"), Decimal("9300000")),
    # Apr 2026
    (1, date(2026, 4, 1), Decimal("13000000"), Decimal("700000"), Decimal("200000"), Decimal("13500000")),
    (2, date(2026, 4, 1), Decimal("10500000"), Decimal("800000"), Decimal("100000"), Decimal("11200000")),
    (3, date(2026, 4, 1), Decimal("16000000"), Decimal("900000"), Decimal("0"), Decimal("16900000")),
    (4, date(2026, 4, 1), Decimal("12000000"), Decimal("600000"), Decimal("100000"), Decimal("12500000")),
    (5, date(2026, 4, 1), Decimal("9500000"), Decimal("0"), Decimal("500000"), Decimal("9000000")),
    (6, date(2026, 4, 1), Decimal("10000000"), Decimal("500000"), Decimal("0"), Decimal("10500000")),
    (7, date(2026, 4, 1), Decimal("19000000"), Decimal("1500000"), Decimal("0"), Decimal("20500000")),
    (8, date(2026, 4, 1), Decimal("7500000"), Decimal("300000"), Decimal("0"), Decimal("7800000")),
    (9, date(2026, 4, 1), Decimal("5500000"), Decimal("100000"), Decimal("0"), Decimal("5600000")),
    (10, date(2026, 4, 1), Decimal("9000000"), Decimal("500000"), Decimal("100000"), Decimal("9400000")),
]

DIVIDENDS = [
    (1, Decimal("500000"), date(2024, 12, 31)),
    (2, Decimal("800000"), date(2024, 12, 31)),
    (3, Decimal("300000"), date(2024, 12, 31)),
    (4, Decimal("700000"), date(2024, 12, 31)),
    (5, Decimal("400000"), date(2024, 12, 31)),
    (6, Decimal("600000"), date(2024, 12, 31)),
    (7, Decimal("900000"), date(2024, 12, 31)),
    (8, Decimal("200000"), date(2024, 12, 31)),
    (9, Decimal("150000"), date(2024, 12, 31)),
    (10, Decimal("850000"), date(2024, 12, 31)),
]


async def seed():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # ── 0. Admin user ──
        from app.models.user import User
        admin = User(
            email="admin@company.vn",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin",
            role="admin",
            is_active=True,
        )
        session.add(admin)
        print("✓ Created admin user (admin@company.vn / admin123)")

        # ── 1. Departments ──
        from app.models.department import Department
        for dept_id, name in DEPARTMENTS:
            session.add(Department(id=dept_id, department_name=name))
        print(f"✓ Seeded {len(DEPARTMENTS)} departments")

        # ── 2. Positions ──
        from app.models.position import Position
        for pos_id, name in POSITIONS:
            session.add(Position(id=pos_id, position_name=name))
        print(f"✓ Seeded {len(POSITIONS)} positions")

        await session.flush()

        # ── 3. Employees ──
        from app.models.employee import Employee
        for emp_id, name, dob, gender, phone, email, hire, dept, pos, status in EMPLOYEES:
            session.add(Employee(
                id=emp_id, full_name=name, date_of_birth=dob, gender=gender,
                phone_number=phone, email=email, hire_date=hire,
                department_id=dept, position_id=pos, status=status,
            ))
        print(f"✓ Seeded {len(EMPLOYEES)} employees")

        await session.flush()

        # ── 4. Attendance ──
        from app.models.attendance import Attendance
        for emp_id, work, absent, leave, late, month in ATTENDANCE:
            session.add(Attendance(
                employee_id=emp_id, work_days=work, absent_days=absent,
                leave_days=leave, late_days=late, attendance_month=month,
            ))
        print(f"✓ Seeded {len(ATTENDANCE)} attendance records")

        # ── 5. Salaries ──
        from app.models.salary import Salary
        for emp_id, month, base, bonus, ded, net in SALARIES:
            session.add(Salary(
                employee_id=emp_id, salary_month=month,
                base_salary=base, bonus=bonus, deductions=ded, net_salary=net,
            ))
        print(f"✓ Seeded {len(SALARIES)} salary records")

        # ── 6. Dividends ──
        from app.models.dividend import Dividend
        for emp_id, amount, div_date in DIVIDENDS:
            session.add(Dividend(
                employee_id=emp_id, dividend_amount=amount, dividend_date=div_date,
            ))
        print(f"✓ Seeded {len(DIVIDENDS)} dividends")

        await session.commit()
        print("\n✅ Database seeded successfully!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
