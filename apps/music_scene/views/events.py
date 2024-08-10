from fasthtml import Div, H1

from apps.music_scene.components.events import EventsActions, CompactEventList
from apps.music_scene.components.forms import EventForm
from apps.music_scene.components.layout import Container
from apps.music_scene.models import events, venues


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
        #EventsActions(view_mode="compact", hx_swap_oob="#events-actions"),
        Div(cls="mt-4")(*CompactEventList(events(order_by="date"))),
    )


def calendar():
    return (
        #EventsActions(view_mode="full", hx_swap_oob="#events-actions"),
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