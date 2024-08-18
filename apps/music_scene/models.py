from sqlmodel import Field, SQLModel, create_engine


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    artist: str | None
    date: str
    start_time: str | None
    venue_id: int | None = Field(default=None, foreign_key="venue.id")
    description: str | None
    url: str | None
    is_featured: bool = Field(default=False)


class Venue(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    address: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    website: str
    description: str | None
