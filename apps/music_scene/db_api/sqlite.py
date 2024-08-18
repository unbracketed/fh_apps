from dataclasses import dataclass, asdict
from typing import List

from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

DB_URL = "/Users/brian/code/fh_apps/apps/music_scene/music_scene_with_api.db"
EVENTS_TABLE = "events"
VENUES_TABLE = "venues"


def tracer(sql, params):
    print("SQL: {} - params: {}".format(sql, params))


db = Database(DB_URL, tracer=tracer)


@dataclass
class Venue:
    id = int
    name = str
    address = str
    city = str
    state = str
    zip_code = str
    website = str
    description = str


@dataclass
class Event:
    id: int
    title: str
    artist: str
    date: str
    start_time: str
    venue_id: str
    description: str
    url: str
    is_featured: bool


def init_db():
    db[VENUES_TABLE].create(asdict(Venue), if_not_exists=True, not_null=["name"])

    db[EVENTS_TABLE].create(
        asdict(Event),
        pk="id",
        if_not_exists=True,
        not_null={"title", "date"},
        defaults={"is_featured": False},
    )
    return db


def get_db():
    return Database(DB_URL, tracer=tracer)


def get_events_table():
    return db[EVENTS_TABLE]


def get_event(event_id: int) -> Event | None:
    events_table = get_events_table()
    try:
        return Event(**events_table.get(event_id))
    except NotFoundError:
        return None


def list_events() -> List[Event]:
    events_table = get_events_table()
    return [Event(**row) for row in events_table.rows]


def create_event(
    title: str,
    date: str,
    artist: str = None,
    start_time: str = None,
    venue_id: int = None,
):
    events_table = get_events_table()
    new_event = dict(
        title=title, date=date, artist=artist, venue_id=venue_id, start_time=start_time
    )
    return events_table.insert(new_event)


def update_event(
    event_id: int,
    title: str = None,
    artist: str = None,
    date: str = None,
    start_time: str = None,
    venue_id: int = None,
) -> True:
    events_table = get_events_table()
    events_table.update(
        event_id,
        dict(
            title=title,
            artist=artist,
            date=date,
            start_time=start_time,
            venue_id=venue_id,
        ),
    )
    return True


def delete_event(event_id: int) -> bool:
    events_table = get_events_table()
    events_table.delete(event_id)
    return True


def search_events(query: str) -> List[Event]:
    events_table = get_events_table()
    return [
        Event(**row)
        for row in events_table.rows_where(
            "title LIKE ? OR artist LIKE ?", [f"%{query}%", f"%{query}%"]
        )
    ]


def get_venues_table():
    return db[VENUES_TABLE]


def get_venue(venue_id: int) -> Venue | None:
    venues_table = get_venues_table()
    try:
        return Venue(**venues_table.get(venue_id))
    except NotFoundError:
        return None


def list_venues() -> List[Venue]:
    venues_table = get_venues_table()
    return [Venue(**row) for row in venues_table.rows]


def create_venue(
    name: str,
    address: str = None,
    city: str = None,
    state: str = None,
    zip_code: str = None,
    website: str = None,
    description: str = None,
) -> Venue:
    venues_table = get_venues_table()
    new_venue = dict(
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        website=website,
        description=description,
    )
    venue_id = venues_table.insert(new_venue)
    return get_venue(venue_id)


def update_venue(venue_id: int, **kwargs) -> Venue:
    venues_table = get_venues_table()
    venues_table.update(venue_id, kwargs)
    return get_venue(venue_id)


def delete_venue(venue_id: int) -> bool:
    venues_table = get_venues_table()
    venues_table.delete(venue_id)
    return True


def search_venues(search_term: str) -> List[Venue]:
    venues_table = get_venues_table()
    results = venues_table.rows_where(
        "name LIKE ? OR city LIKE ? OR description LIKE ?",
        [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"],
    )
    return [Venue(**row) for row in results]
