from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response model."""
    items: List[T] = Field(..., description="List of items for current page")
    page: int = Field(..., description="Current page number", example=1)
    per_page: int = Field(..., description="Number of items per page", example=10)
    total: int = Field(..., description="Total number of items", example=100)
    total_pages: int = Field(..., description="Total number of pages", example=10)

    model_config = {
        "json_schema_extra": {
            "example": {
                "items": [],
                "page": 1,
                "per_page": 10,
                "total": 100,
                "total_pages": 10
            }
        }
    }