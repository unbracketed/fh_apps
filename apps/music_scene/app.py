from fasthtml import fill_form
from fasthtml.common import Div, Titled, Link, A, H2, fast_app, serve
from starlette.responses import RedirectResponse, FileResponse

from apps.music_scene.components.events import EventDetails, CompactEventList
from apps.music_scene.components.layout import Container, layout, Grid, ControlPanel
from apps.music_scene.models import Event, events
from components.forms import EventForm

head_section = (
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True),
    Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@200..900&family=Karla:ital,wght@0,200..800;1,200..800&display=swap",
    ),
    Link(
        rel="stylesheet",
        href="/static/base.css",
    ),
)


exception_handlers = {
    404: lambda req, exc: Titled("404: I don't exist!"),
    418: lambda req, exc: Titled("418: I'm a teapot!"),
}

app, rt = fast_app(
    hdrs=head_section,
    pico=False,
    exception_handlers=exception_handlers,
    bodykw={"cls": "bg-orange-50"},
)


@rt("/static/{fname:path}.{ext:static}")
async def get(fname: str, ext: str):
    return FileResponse(f"/static/{fname}.{ext}")


@rt("/")
@layout()
def get():
    upcoming_events = events(order_by="date")

    return (
        Grid(cols=4)(
            Div(id="event-list", cls="col-span-3")(
                A(href="/full-view", hx_get="/full-view", hx_target="#event-list", cls="underline")(
                    "Full View"
                ),
                *CompactEventList(upcoming_events, cls="mt-4"),
            ),
            ControlPanel(),
        ),
    )


@rt("/control-panel")
def get():
    return ControlPanel()


@rt("/full-view")
def get():
    return A(href="/compact-view", hx_get="/compact-view", hx_target="#event-list", cls="underline")(
        "Compact View"
    ), Div(cls="mt-4")(*events(order_by="date"))


@rt("/compact-view")
def get():
    return Div(
        A(href="/full-view", hx_get="/full-view", hx_target="#event-list", cls=)("Full View"),
        *CompactEventList(events(order_by="date"), cls="mt-4"),
    )


@rt("/add_event")
def get():
    return H2(cls="text-xl")("Add New Event"), Div(EventForm("/add_event", "Add Event"))


@rt("/add_event")
def post(
    title: str,
    artist: str,
    date: str,
    start_time: str,
    url: str,
    venue: str,
    description: str,
):
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
    return RedirectResponse(url="/", status_code=303)


@rt("/event/{event_id}")
@layout()
def get(event_id: int):
    event = events[event_id]
    return Titled(f"Event: {event.title}", Div(EventDetails(event)))


@rt("/edit_event/{event_id}")
def get(event_id: int):
    event = events[event_id]
    return Titled(
        f"Edit Event: {event.title}",
        Container(
            fill_form(EventForm(f"/edit_event/{event_id}", "Save Event"), event),
            event,
        ),
    )


@rt("/edit_event/{event_id}")
def post(
    event_id: int,
    title: str,
    artist: str,
    date: str,
    start_time: str,
    url: str,
    venue: str,
    description: str,
):
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
    return RedirectResponse(url=f"/event/{event_id}", status_code=303)


serve(port=5045)
