import math
from dataclasses import dataclass

from app.domain.countries import currency_for
from app.errors import ConflictError, NotFoundError
from app.models import Employee
from app.repositories.employee_repository import EmployeeFilters, EmployeeRepository, SortField
from app.schemas import EmployeeCreate, EmployeeUpdate


@dataclass(frozen=True)
class Page:
    items: list[Employee]
    total: int
    page: int
    page_size: int

    @property
    def pages(self) -> int:
        return math.ceil(self.total / self.page_size) if self.total else 0


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def create(self, data: EmployeeCreate) -> Employee:
        self._ensure_email_free(data.email)
        return self.repo.add(Employee(**data.model_dump(), currency=currency_for(data.country)))

    def get(self, employee_id: int) -> Employee:
        employee = self.repo.get(employee_id)
        if employee is None:
            raise NotFoundError(f"Employee {employee_id} not found")
        return employee

    def update(self, employee_id: int, data: EmployeeUpdate) -> Employee:
        employee = self.get(employee_id)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        if "email" in changes and changes["email"] != employee.email:
            self._ensure_email_free(changes["email"])
        for field, value in changes.items():
            setattr(employee, field, value)
        if "country" in changes:
            employee.currency = currency_for(employee.country)
        return self.repo.save(employee)

    def delete(self, employee_id: int) -> None:
        self.repo.delete(self.get(employee_id))

    def list(
        self,
        filters: EmployeeFilters,
        sort_by: SortField,
        descending: bool,
        page: int,
        page_size: int,
    ) -> Page:
        items, total = self.repo.search(
            filters, sort_by, descending, offset=(page - 1) * page_size, limit=page_size
        )
        return Page(items, total, page, page_size)

    def _ensure_email_free(self, email: str) -> None:
        if self.repo.get_by_email(email) is not None:
            raise ConflictError(f"Email already in use: {email}")
