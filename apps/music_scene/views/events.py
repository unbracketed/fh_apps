from fasthtml import Div, H1, Titled, fill_form

from apps.music_scene.components.events import (
    EventsActions,
    CompactEventList,
    EventDetails,
)
from apps.music_scene.components.forms import EventForm
from apps.music_scene.components.layout import Container
from apps.music_scene.models import events, venues, Event


def homeview():
    upcoming_events = events(order_by="date")
    return Container(
        H1(cls="text-3xl py-4")("Music Scene Manager"),
        EventsActions(view_mode="compact"),
        Div(id="event-list", cls="bg-orange-100 border-2 border-slate-500")(
            *CompactEventList(upcoming_events),
        ),
    )


def compact_list():
    return (
        # EventsActions(view_mode="compact", hx_swap_oob="#events-actions"),
        Div(cls="mt-4")(*CompactEventList(events(order_by="date"))),
    )


def calendar():
    return (
        # EventsActions(view_mode="full", hx_swap_oob="#events-actions"),
        Div(cls="mt-4 bg-slate-50")(*events(order_by="date")),
    )


def add_event_form():
    return (Div(EventForm("/events/add-event", "Add Event")),)


def add_event_handler(
    title: str,
    artist: str,
    date: str,
    start_time: str,
    url: str,
    venue_id: str,
    description: str,
):
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


def event_detail(event_id: int):
    event = events[event_id]
    return Titled(f"Event: {event.title}", Div(EventDetails(event)))


def edit_event_form(event_id: int):
    event = events[event_id]
    venue_id = venues.lookup({"name": event.venue})
    setattr(event, "venue_id", venue_id)
    form = EventForm(f"/edit-event/{event_id}", "Edit Event", event_id=event_id)
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
):
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


def copy_event_form(event_id: int):
    src_event = events[event_id]
    form = EventForm(
        "/events/add-event", f"Copy of {src_event.title}", event_id=event_id
    )
    return Div(fill_form(form, src_event))


def delete_event(event_id: int):
    events.delete(event_id)
    return Div(*CompactEventList(events(order_by="date")))
