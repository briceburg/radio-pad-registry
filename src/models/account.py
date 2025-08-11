from pydantic import BaseModel, Field

from lib.constants import SLUG_PATTERN


class AccountBase(BaseModel):
    """Base model for accounts, containing common fields."""

    name: str = Field(..., json_schema_extra={"example": "brice b"})


class AccountCreate(AccountBase):
    """Request body model for creating/updating an account via the PUT endpoint."""

    pass


class Account(AccountBase):
    """The full account model as stored and returned by the API."""

    id: str = Field(
        ...,
        pattern=SLUG_PATTERN,
        json_schema_extra={"example": "briceburg", "pattern": SLUG_PATTERN},
    )
