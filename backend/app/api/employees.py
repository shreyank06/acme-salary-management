from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.deps import get_employee_service, get_repo
from app.repositories.employee_repository import EmployeeFilters, EmployeeRepository, SortField
from app.schemas import (
    EmployeeCreate,
    EmployeeOut,
    EmployeePage,
    EmployeeUpdate,
    FacetsOut,
)
from app.services.employee_service import EmployeeService

router = APIRouter(prefix="/api/employees", tags=["employees"])
Service = Annotated[EmployeeService, Depends(get_employee_service)]


@router.get("", response_model=EmployeePage)
def list_employees(
    service: Service,
    q: str | None = Query(None, max_length=100),
    country: str | None = None,
    department: str | None = None,
    job_title: str | None = None,
    min_salary: int | None = Query(None, ge=0),
    max_salary: int | None = Query(None, ge=0),
    sort_by: SortField = "full_name",
    order: Literal["asc", "desc"] = "asc",
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
):
    filters = EmployeeFilters(q, country, department, job_title, min_salary, max_salary)
    result = service.list(filters, sort_by, order == "desc", page, page_size)
    return EmployeePage(
        items=[EmployeeOut.model_validate(e) for e in result.items],
        total=result.total,
        page=result.page,
        page_size=result.page_size,
        pages=result.pages,
    )


@router.get("/facets", response_model=FacetsOut)
def facets(repo: EmployeeRepository = Depends(get_repo)):
    return repo.facets()


@router.post("", response_model=EmployeeOut, status_code=status.HTTP_201_CREATED)
def create_employee(data: EmployeeCreate, service: Service):
    return service.create(data)


@router.get("/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, service: Service):
    return service.get(employee_id)


@router.patch("/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, data: EmployeeUpdate, service: Service):
    return service.update(employee_id, data)


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(employee_id: int, service: Service):
    service.delete(employee_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
