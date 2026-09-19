from dataclasses import dataclass
from typing import Literal

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.models import Employee

SortField = Literal["full_name", "job_title", "department", "country", "salary", "hire_date"]
SORTABLE: dict[str, object] = {
    "full_name": Employee.full_name,
    "job_title": Employee.job_title,
    "department": Employee.department,
    "country": Employee.country,
    "salary": Employee.salary,
    "hire_date": Employee.hire_date,
}


@dataclass(frozen=True)
class EmployeeFilters:
    q: str | None = None
    country: str | None = None
    department: str | None = None
    job_title: str | None = None
    min_salary: int | None = None
    max_salary: int | None = None


@dataclass(frozen=True)
class SalaryRow:
    country: str
    currency: str
    department: str
    job_title: str
    salary: int


def _apply_filters(stmt: Select, f: EmployeeFilters) -> Select:
    if f.q:
        like = f"%{f.q.strip().lower()}%"
        stmt = stmt.where(
            or_(func.lower(Employee.full_name).like(like), func.lower(Employee.email).like(like))
        )
    if f.country:
        stmt = stmt.where(Employee.country == f.country)
    if f.department:
        stmt = stmt.where(Employee.department == f.department)
    if f.job_title:
        stmt = stmt.where(Employee.job_title == f.job_title)
    if f.min_salary is not None:
        stmt = stmt.where(Employee.salary >= f.min_salary)
    if f.max_salary is not None:
        stmt = stmt.where(Employee.salary <= f.max_salary)
    return stmt


class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, employee: Employee) -> Employee:
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get(self, employee_id: int) -> Employee | None:
        return self.session.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        return self.session.scalar(select(Employee).where(Employee.email == email))

    def save(self, employee: Employee) -> Employee:
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self.session.delete(employee)
        self.session.commit()

    def search(
        self,
        filters: EmployeeFilters,
        sort_by: SortField = "full_name",
        descending: bool = False,
        offset: int = 0,
        limit: int = 25,
    ) -> tuple[list[Employee], int]:
        total = self.session.scalar(_apply_filters(select(func.count(Employee.id)), filters))
        column = SORTABLE[sort_by]
        order = column.desc() if descending else column.asc()  # type: ignore[attr-defined]
        stmt = (
            _apply_filters(select(Employee), filters)
            .order_by(order, Employee.id)  # id tiebreaker => stable pagination
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(stmt)), total or 0

    def salary_rows(self, filters: EmployeeFilters | None = None) -> list[SalaryRow]:
        """Narrow projection (5 columns) so aggregation over 10k rows stays cheap."""
        stmt = select(
            Employee.country,
            Employee.currency,
            Employee.department,
            Employee.job_title,
            Employee.salary,
        )
        if filters:
            stmt = _apply_filters(stmt, filters)
        return [SalaryRow(*row) for row in self.session.execute(stmt)]

    def facets(self) -> dict[str, list[str]]:
        def distinct(col) -> list[str]:
            return list(self.session.scalars(select(col).distinct().order_by(col)))

        return {
            "countries": distinct(Employee.country),
            "departments": distinct(Employee.department),
            "job_titles": distinct(Employee.job_title),
        }
