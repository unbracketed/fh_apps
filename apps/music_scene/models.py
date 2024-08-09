from fasthtml.common import patch
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


@patch(as_prop=True)
def name(self: Event) -> str:
    return self.title if not self.artist else f"{self.title}: {self.artist}"


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
    all_venues = set([event.venue for event in events()])
    for venue in all_venues:
        venues.insert({"name": venue})
Venue = venues.dataclass()

__all__ = ["events", "Event", "venues", "Venue"]
