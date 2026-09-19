from collections.abc import Iterator

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.services.insights_service import InsightsService


def get_session(request: Request) -> Iterator[Session]:
    with request.app.state.session_factory() as session:
        yield session


def get_repo(session: Session = Depends(get_session)) -> EmployeeRepository:
    return EmployeeRepository(session)


def get_employee_service(repo: EmployeeRepository = Depends(get_repo)) -> EmployeeService:
    return EmployeeService(repo)


def get_insights_service(repo: EmployeeRepository = Depends(get_repo)) -> InsightsService:
    return InsightsService(repo)
