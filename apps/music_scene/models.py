from typing import List

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


db = database("/Users/brian/code/fh_apps/apps/music_scene/music_scene.db")
# db.register_fts4_bm25()

events = db.t.events
if events not in db.t:
    events.create(**events_schema)
db["events"].enable_fts(
    ["title", "artist", "venue"], create_triggers=True, replace=True
)

Event = events.dataclass()


@patch(as_prop=True)
def name(self: Event) -> str:
    return self.title if not self.artist else f"{self.title}: {self.artist}"


# This is needed because detect_fts() is failing
# detect_fts attempts to find entries in sqlite_master but the like comparisons are failing due to
# multi-line schema statements
fts_search_sql = """
with original as (
    select
        rowid,
        [title],
        [artist],
        [venue]
    from [events]
)
select
    [original].[title],
    [original].[artist],
    [original].[venue]
from
    [original]
    join [events_fts] on [original].rowid = [events_fts].rowid
where
    [events_fts] match :query
order by
    rank_bm25(matchinfo([events_fts], 'pcnalx'))
"""


def do_search(query: str) -> List[Event]:
    return [
        Event(**row)
        for row in events.rows_where(
            "title LIKE ? OR artist LIKE ?", [f"%{query}%", f"%{query}%"]
        )
    ]


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
db["venues"].enable_fts(["name"], create_triggers=True, replace=True)
Venue = venues.dataclass()

__all__ = ["events", "Event", "venues", "Venue"]
