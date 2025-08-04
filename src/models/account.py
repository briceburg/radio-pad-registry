from typing import Optional
from pydantic import BaseModel


class Account(BaseModel):
    """Account model."""
    id: str
    name: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "briceburg",
                "name": "Brice B"
            }
        }
    }


class AccountList(BaseModel):
    """Account list item for pagination."""
    id: str
    name: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "briceburg", 
                "name": "Briceburg"
            }
        }
    }