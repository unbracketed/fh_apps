from dataclasses import dataclass, asdict, make_dataclass
from typing import List

from sqlite_utils import Database
from sqlite_utils.db import NotFoundError

from apps.music_scene.models import Venue, Event  # , venue_schema, event_schema

DB_URL = "/Users/brian/code/fh_apps/apps/music_scene/music_scene_with_api.db"
EVENTS_TABLE = "events"
VENUES_TABLE = "venues"


def tracer(sql, params):
    print("SQL: {} - params: {}".format(sql, params))


# from dataclasses import dataclass, make_dataclass

venue_schema = dict(
    id=int,
    name=str,
    address=str,
    city=str,
    state=str,
    zip_code=str,
    website=str,
    description=str,
)

Venue = make_dataclass("Venue", venue_schema.items())

event_schema = dict(
    id=int,
    title=str,
    artist=str,
    date=str,
    start_time=str,
    venue_id=int,
    description=str,
    url=str,
    is_featured=bool,
)
Event = make_dataclass("Event", event_schema.items())


def init_db(db):
    db[VENUES_TABLE].create(
        venue_schema, pk="id", if_not_exists=True, not_null=["name"]
    )

    db[EVENTS_TABLE].create(
        event_schema,
        pk="id",
        if_not_exists=True,
        not_null={"title", "date"},
        foreign_keys=[("venue_id", "venues")],
        defaults={"is_featured": False},
    )
    return db


def get_db():
    return Database(DB_URL, tracer=tracer)


def get_events_table():
    return get_db()[EVENTS_TABLE]


def get_event(event_id: int) -> Event | None:
    events_table = get_events_table()
    try:
        return Event(**events_table.get(event_id))
    except NotFoundError:
        return None


def list_events(join_venues=False) -> List[Event]:
    Venue = make_dataclass("Venue", [("name", str), ("city", str), ("state", str)])
    FullEvent = make_dataclass(
        "Event",
        [
            ("id", int),
            ("title", int),
            ("artist", str),
            ("date", str),
            ("start_time", str),
            ("venue", Venue),
            ("name", str),
        ],
    )

    if join_venues:
        join_venues_sql = """
            SELECT
                e.id,
                e.title,
                e.artist,
                e.date,
                e.start_time,
                v.name AS venue_name,
                v.city AS venue_city,
                v.state AS venue_state
            FROM
                events e
            LEFT JOIN
                venues v ON e.venue_id = v.id
        """
        prepped_events = []
        rows = get_db().query(join_venues_sql)
        for row in rows:
            venue_name = row.pop("venue_name")
            venue_city = row.pop("venue_city")
            venue_state = row.pop("venue_state")
            if venue_name:
                _venue = Venue(name=venue_name, city=venue_city, state=venue_state)
                row["venue"] = _venue
            else:
                row["venue"] = None
            row["name"] = (
                f"{row['title']} - {row['artist']}" if row["artist"] else row["title"]
            )
            prepped_events.append(FullEvent(**row))
        return prepped_events

    events_table = get_events_table()
    return [Event(**row) for row in events_table.rows]


def upcoming_events() -> List[Event]:
    events_table = get_events_table()
    # TODO need to add date comparison to rows_where
    return [Event(**row) for row in events_table.rows_where(order_by="date")]


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
    update_cols = {}
    if title:
        update_cols["title"] = title
    if artist:
        update_cols["artist"] = artist
    if date:
        update_cols["date"] = date
    if start_time:
        update_cols["start_time"] = start_time
    if venue_id:
        update_cols["venue_id"] = venue_id
    events_table.update(event_id, update_cols)
    return True


def delete_event(event_id: int) -> bool:
    events_table = get_events_table()
    events_table.delete(event_id)
    return True


def search_events(query: str, join_venues=False) -> List[Event]:
    Venue = make_dataclass("Venue", [("name", str), ("city", str), ("state", str)])
    Event = make_dataclass(
        "Event",
        [
            ("id", int),
            ("title", int),
            ("artist", str),
            ("date", str),
            ("start_time", str),
            ("venue", Venue),
            ("name", str),
        ],
    )
    if join_venues:
        join_venues_sql = """
                    SELECT
                        e.id,
                        e.title,
                        e.artist,
                        e.date,
                        e.start_time,
                        v.name AS venue_name,
                        v.city AS venue_city,
                        v.state AS venue_state
                    FROM
                        events e
                    LEFT JOIN
                        venues v ON e.venue_id = v.id
                    WHERE
                        e.title LIKE ? OR e.artist LIKE ?
                """
        prepped_events = []
        rows = get_db().query(join_venues_sql, [f"%{query}%", f"%{query}%"])
        for row in rows:
            venue_name = row.pop("venue_name")
            venue_city = row.pop("venue_city")
            venue_state = row.pop("venue_state")
            if venue_name:
                _venue = Venue(name=venue_name, city=venue_city, state=venue_state)
                row["venue"] = _venue
            else:
                row["venue"] = None
            row["name"] = (
                f"{row['title']} - {row['artist']}" if row["artist"] else row["title"]
            )
            prepped_events.append(Event(**row))
        return prepped_events
    else:
        events_table = get_events_table()
        return [
            Event(**row)
            for row in events_table.rows_where(
                "title LIKE ? OR artist LIKE ?", [f"%{query}%", f"%{query}%"]
            )
        ]


def get_venues_table():
    return get_db()[VENUES_TABLE]


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
    venues_table.insert(new_venue)
    return True


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
