"""Pydantic request/response models (the API contract)."""

from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.countries import COUNTRIES

Name = Annotated[str, Field(min_length=1, max_length=120)]
Label = Annotated[str, Field(min_length=1, max_length=80)]
Salary = Annotated[int, Field(gt=0, le=2_000_000_000)]


def _check_country(v: str | None) -> str | None:
    if v is not None and v not in COUNTRIES:
        raise ValueError(f"Unsupported country: {v}")
    return v


class EmployeeBase(BaseModel):
    full_name: Name
    email: EmailStr
    job_title: Label
    department: Label
    country: str
    salary: Salary
    hire_date: date

    _country = field_validator("country")(_check_country)

    @field_validator("email")
    @classmethod
    def _lower_email(cls, v: str) -> str:
        return v.lower()


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    """All fields optional (PATCH semantics)."""

    full_name: Name | None = None
    email: EmailStr | None = None
    job_title: Label | None = None
    department: Label | None = None
    country: str | None = None
    salary: Salary | None = None
    hire_date: date | None = None

    _country = field_validator("country")(_check_country)

    @field_validator("email")
    @classmethod
    def _lower_email(cls, v: str | None) -> str | None:
        return v.lower() if v else v


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    job_title: str
    department: str
    country: str
    currency: str
    salary: int
    hire_date: date


class EmployeePage(BaseModel):
    items: list[EmployeeOut]
    total: int
    page: int
    page_size: int
    pages: int


class StatsOut(BaseModel):
    count: int
    total: int
    min: int
    max: int
    avg: float
    median: float


class SummaryOut(BaseModel):
    currency: str
    headcount: int
    countries: int
    total_payroll: int
    avg_salary: float
    median_salary: float


class BreakdownRow(BaseModel):
    key: str
    currency: str
    stats: StatsOut


class BucketOut(BaseModel):
    start: int
    end: int
    count: int


class DistributionOut(BaseModel):
    currency: str
    buckets: list[BucketOut]


class FacetsOut(BaseModel):
    countries: list[str]
    departments: list[str]
    job_titles: list[str]
