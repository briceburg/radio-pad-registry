import logging
from typing import List, TypeVar, Type

from fastapi import HTTPException
from pydantic import ValidationError
from models.pagination import PaginatedResponse

T = TypeVar('T')


def get_logger(name=None):
    """Return a logger using the uvicorn.error logger by default.
    Uvicorn's documentation and community recommend using 'uvicorn.error' for application logs and 'uvicorn.access' for HTTP access logs.
    """
    return logging.getLogger(name or "uvicorn.error")


logger = get_logger()


def build_paginated_response(
    raw_items: List[dict], 
    model_class: Type[T], 
    page: int = 1, 
    per_page: int = 10, 
    max_per_page: int = 100
) -> PaginatedResponse[T]:
    """Build a paginated response using pydantic models."""
    try:
        page = int(page)
        per_page = int(per_page)
    except (ValueError, TypeError):
        page = 1
        per_page = 10

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > max_per_page:
        per_page = max_per_page

    total = len(raw_items)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_raw_items = raw_items[start:end]

    # Convert raw items to pydantic models
    try:
        items = [model_class(**item) for item in paginated_raw_items]
    except ValidationError as e:
        error_message = f"Schema validation error: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail="Internal server error")

    return PaginatedResponse[model_class](
        items=items,
        page=page,
        per_page=per_page,
        total=total,
        total_pages=(total + per_page - 1) // per_page,
    )
