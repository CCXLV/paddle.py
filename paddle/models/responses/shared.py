from typing import Literal, Optional, TypedDict

from pydantic import BaseModel


class ImportMeta(BaseModel):
    imported_from: Literal["paddle_classic"]
    external_id: Optional[str] = None


class Pagination(BaseModel):
    per_page: int
    next: str
    has_more: bool
    estimated_total: int


class Meta(BaseModel):
    request_id: str


class MetaWithPagination(Meta):
    pagination: Pagination


class BillingCycle(BaseModel):
    frequency: int
    interval: Literal["day", "week", "month", "year"]


class BillingCycleType(TypedDict):
    frequency: int
    interval: Literal["day", "week", "month", "year"]


class DateRange(BaseModel):
    starts_at: str
    ends_at: str
