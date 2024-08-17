from fasthtml.common import Div, Titled, fill_form, uri, FT
from starlette.requests import Request

from apps.music_scene.components.events import (
    CompactEventList,
    EventDetails,
    ViewActions,
    EventsTable,
)
from apps.music_scene.components.forms import EventForm
from apps.music_scene.components.layout import MultiViewContainer, StackedLayout
from apps.music_scene.models import events, venues, Event


def home_view(request: Request) -> FT:
    upcoming_events = events(order_by="date")
    event_list = Div(EventsTable(upcoming_events))
    if request.headers.get("hx-request"):
        # return ViewActions(hx_oob_swap="true"), event_list
        return event_list
    return StackedLayout("Events", ViewActions(), event_list)


def list_view(request: Request) -> FT:
    event_list = Div(EventsTable(events(order_by="date")))
    if request.headers.get("hx-request"):
        # return ViewActions(hx_oob_swap="true"), event_list
        return event_list
    return StackedLayout("Events", ViewActions(), event_list)


def calendar(request: Request) -> FT:
    events_list = Div(cls="mt-4 bg-slate-50")(*events(order_by="date"))
    calendar_actions = ""
    if request.headers.get("hx-request"):
        return events_list
    return StackedLayout("Calendar", calendar_actions, events_list)


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
    venue = venues[venue_id].name
    new_event = dict(
        title=title,
        artist=artist,
        date=date,
        start_time=start_time,
        venue=venue,
        url=url,
        description=description,
    )
    events.insert(new_event)
    return Div(*CompactEventList(events(order_by="date")))


def event_detail(event_id: int) -> FT:
    event = events[event_id]
    return Titled(f"Event: {event.title}", Div(EventDetails(event)))


def edit_event_form(event_id: int) -> FT:
    event = events[event_id]
    venue_id = venues.lookup({"name": event.venue})
    setattr(event, "venue_id", venue_id)
    # action = req.url_for("edit_event_handler", event_id=event_id)
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
    venue = venues[venue_id].name
    updated_event = Event(
        id=event_id,
        title=title,
        artist=artist,
        date=date,
        start_time=start_time,
        venue=venue,
        url=url,
        description=description,
    )
    events.update(updated_event)
    return Div(*CompactEventList(events(order_by="date")))


def copy_event_form(event_id: int) -> FT:
    src_event = events[event_id]
    form = EventForm(
        uri("add_event_handler"), f"Copy of {src_event.title}", event_id=event_id
    )
    return Div(fill_form(form, src_event))


def delete_event_handler(event_id: int) -> FT:
    events.delete(event_id)
    return Div(*CompactEventList(events(order_by="date")))
