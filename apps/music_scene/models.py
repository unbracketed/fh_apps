from fastlite import database


events_schema = dict(
    id=int,
    title=str,
    artist=str,
    date=str,
    start_time=str,
    venue=str,
    description=str,
    url=str,
    pk="id",
)


db = database("music_scene.db")
events = db.t.events
if events not in db.t:
    events.create(**events_schema)


Event = events.dataclass()

venues_schema = dict(
    id=int,
    name=str,
    address=str,
    city=str,
    state=str,
    zip_code=str,
    website=str,
    description=str,
    pk="id",
)

venues = db.t.venues
if venues not in db.t:
    venues.create(**venues_schema)

Venue = venues.dataclass()

__all__ = ["events", "Event", "venues", "Venue"]
