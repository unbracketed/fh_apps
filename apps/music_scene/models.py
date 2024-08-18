from datetime import date, time
from typing import List
from pydantic import validator
from sqlmodel import Field, SQLModel, Relationship


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    artist: str | None
    date: date
    start_time: time | None
    venue_id: int | None = Field(default=None, foreign_key="venue.id")
    description: str | None
    url: str | None
    is_featured: bool = Field(default=False)
    venue: "Venue" = Relationship(back_populates="events")

    # @validator('date')
    # def ensure_date_not_past(cls, v):
    #     if v < date.today():
    #         raise ValueError('Date cannot be in the past')
    #     return v


class Venue(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    address: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    website: str | None
    description: str | None
    events: List["Event"] = Relationship(back_populates="venue")

    # @validator('zip_code')
    # def validate_zip_code(cls, v):
    #     if v and not v.isdigit():
    #         raise ValueError('Zip code must contain only digits')
    #     return v
