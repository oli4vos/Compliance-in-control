from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


def to_camel(value: str) -> str:
    first, *rest = value.split("_")
    return first + "".join(word.capitalize() for word in rest)


class ApiModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        from_attributes=True,
        populate_by_name=True,
    )


class ProjectCreate(ApiModel):
    name: str = Field(min_length=1, max_length=200)
    client: str = Field(min_length=1, max_length=200)
    reference: str = Field(default="", max_length=100)
    due_date: date | None = None
    product: str = Field(default="", max_length=200)
    product_version: str = Field(default="", max_length=100)
    owner: str = Field(default="", max_length=200)
    notes: str = Field(default="", max_length=5000)


class ProjectResponse(ApiModel):
    id: str
    name: str
    client: str
    reference: str
    due_date: date | None
    product: str
    product_version: str
    owner: str
    notes: str
    created_at: datetime
    requirement_count: int = 0
    reviewed_count: int = 0
    sufficient_count: int = 0
    missing_count: int = 0
    next_deadline: date | None = None
    progress: int = 0
