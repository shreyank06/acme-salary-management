from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import get_insights_service
from app.domain.countries import COUNTRIES
from app.repositories.employee_repository import EmployeeFilters
from app.schemas import BreakdownRow, BucketOut, DistributionOut, StatsOut, SummaryOut
from app.services.insights_service import GroupBy, InsightsService

router = APIRouter(prefix="/api", tags=["insights"])
Service = Annotated[InsightsService, Depends(get_insights_service)]


@router.get("/insights/summary", response_model=SummaryOut)
def summary(service: Service, country: str | None = None, department: str | None = None):
    s = service.summary(EmployeeFilters(country=country, department=department))
    return SummaryOut(**vars(s))


@router.get("/insights/breakdown", response_model=list[BreakdownRow])
def breakdown(service: Service, group_by: GroupBy = "country", country: str | None = None):
    return [
        BreakdownRow(key=r.key, currency=r.currency, stats=StatsOut(**vars(r.stats)))
        for r in service.breakdown(group_by, country)
    ]


@router.get("/insights/distribution", response_model=DistributionOut)
def distribution(
    service: Service,
    country: str | None = None,
    department: str | None = None,
    buckets: int = Query(10, ge=2, le=50),
):
    d = service.distribution(EmployeeFilters(country=country, department=department), buckets)
    return DistributionOut(currency=d.currency, buckets=[BucketOut(**vars(b)) for b in d.buckets])


@router.get("/countries")
def countries():
    return [vars(c) for c in COUNTRIES.values()]
