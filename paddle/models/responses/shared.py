from typing import Literal, Optional

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
