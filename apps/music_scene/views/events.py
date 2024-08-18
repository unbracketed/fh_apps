from fasthtml.common import Div, Titled, fill_form, uri, FT, Card, H2, P
from starlette.requests import Request

from apps.music_scene.components.events import (
    EventDetails,
    EventsTable,
    EventsTableBody,
)
from apps.music_scene.components.forms import EventForm
from apps.music_scene.components.layout import StackedLayout
from apps.music_scene.db_api import (
    upcoming_events,
    list_events,
    create_event,
    get_event,
    update_event,
    delete_event,
    search_events,
)
from apps.music_scene.utils import _ds_full


def home_view(request: Request):
    # TODO use upcoming
    events = list_events(join_venues=True)
    event_list = Div(EventsTable(events))
    if request.headers.get("hx-request"):
        return event_list
    return StackedLayout("Dashboard", event_list)


def list_view(request: Request):
    event_list = Div(EventsTable(list_events(join_venues=True)))
    if request.headers.get("hx-request"):
        return event_list
    return StackedLayout("Events", event_list)


def calendar(request: Request):
    # TODO fix upcoming
    calendar_items = []
    for event in list_events(join_venues=True):
        calendar_items.append(
            Card(cls="mb-4 p-4 border rounded bg-slate-700 text-white")(
                H2(event.name, cls="text-xl font-semibold"),
                P(f"Date: {_ds_full(event.date)}", cls="text-sm"),
                P(f"Venue: {event.venue.name}", cls="text-sm") if event.venue else "",
            )
        )
    events_list = Div(cls="mt-4 bg-slate-50")(*calendar_items)
    if request.headers.get("hx-request"):
        return events_list
    return StackedLayout("Calendar", events_list)


def add_event_form() -> FT:
    return Div(EventForm("add_event_handler", "Add Event"))


def add_event_handler(
    title: str,
    artist: str,
    date: str,
    start_time: str,
    url: str,
    venue_id: str,
    description: str,
) -> FT:
    new_event = dict(
        title=title,
        artist=artist,
        date=date,
        start_time=start_time,
        venue_id=venue_id,
        # url=url,
        # description=description,
    )
    create_event(**new_event)
    return EventsTable(list_events(join_venues=True))


def event_detail(event_id: int) -> FT:
    event = get_event(event_id)
    return Titled(f"Event: {event.title}", Div(EventDetails(event)))


def edit_event_form(event_id: int) -> FT:
    event = get_event(event_id)
    form = EventForm(
        uri("edit_event_handler", event_id=event_id), "Edit Event", event_id=event_id
    )
    return Div(cls="col-span-4")(fill_form(form, event))


def edit_event_handler(
    event_id: int,
    title: str,
    artist: str,
    date: str,
    start_time: str,
    url: str,
    venue_id: str,
    description: str,
) -> FT:
    updated_event = dict(
        title=title,
        artist=artist,
        date=date,
        start_time=start_time,
        venue_id=venue_id,
        # url=url,
        # description=description,
        # is_featured=False
    )
    update_event(event_id, **updated_event)
    return EventsTable(list_events(join_venues=True))


def copy_event_form(event_id: int) -> FT:
    src_event = get_event(event_id)
    form = EventForm(
        uri("add_event_handler"), f"Copy of {src_event.title}", event_id=event_id
    )
    return Div(fill_form(form, src_event))


def delete_event_handler(event_id: int) -> FT:
    delete_event(event_id)
    return EventsTable(list_events(join_venues=True))


async def search_events_handler(request: Request) -> FT:
    if request.method == "GET":
        query = request.query_params["q"]
    elif request.method == "POST":
        form_data = await request.form()
        query = form_data.get("search-events")
    search_results = search_events(query, join_venues=True)
    return EventsTableBody(search_results)
