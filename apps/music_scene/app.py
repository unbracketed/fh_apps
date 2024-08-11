from fasthtml import fill_form
from fasthtml.common import Div, Titled, Link, fast_app, serve
from starlette.responses import FileResponse

from apps.music_scene.components.events import CompactEventList
import apps.music_scene.views.events as events_views
from components.forms import EventForm
from apps.music_scene.models import Event, events, Venue, venues
from apps.music_scene.components.venues import VenueList, VenueForm


head_section = (
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True),
    Link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@200..900&family=Karla:ital,wght@0,200..800;1,200..800&display=swap",
    ),
    Link(rel="stylesheet", href="/static/base.css"),
)


exception_handlers = {
    404: lambda req, exc: Titled("404: I don't exist!"),
    418: lambda req, exc: Titled("418: I'm a teapot!"),
    500: lambda req, exc: Titled("500: Hey who turned off the music?"),
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


app.add_route("/", events_views.homeview)
app.add_route("/calendar", events_views.calendar)
app.add_route("/events", events_views.compact_list)
app.add_route("/events/add-event", events_views.add_event_form)
app.add_route("/events/add-event", events_views.add_event_handler, methods=["POST"])
app.add_route("/event/{event_id}", events_views.event_detail)
app.add_route("/edit-event/{event_id}", events_views.edit_event_form)
app.add_route(
    "/edit-event/{event_id}", events_views.edit_event_handler, methods=["POST"]
)
app.add_route("/event/copy/{event_id}", events_views.copy_event_form)
app.add_route("/event/delete/{event_id}", events_views.delete_event, methods=["POST"])


# --------
# Venues
# -------
@rt("/venues")
def get():
    all_venues = venues(order_by="name")
    return (
        Div(id="venue-list")(
            VenueList(all_venues),
        ),
        # Div(id="venue-form")(
        #     VenueForm("/venues/add", "Add Venue"),
        # ),
    )


@rt("/venues/add")
def post(
    name: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    website: str,
    description: str,
):
    new_venue = dict(
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        website=website,
        description=description,
    )
    venues.insert(new_venue)
    return VenueList(venues(order_by="name"))


@rt("/venues/edit/{venue_id}")
def get(venue_id: int):
    venue = venues[venue_id]
    form = VenueForm(f"/venues/edit/{venue_id}", "Save", venue_id)
    return Div(cls="col-span-4")(fill_form(form, venue))


@rt("/venues/edit/{venue_id}")
def post(
    venue_id: int,
    name: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    website: str,
    description: str,
):
    updated_venue = Venue(
        id=venue_id,
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        website=website,
        description=description,
    )
    venues.update(updated_venue)
    return VenueList(venues(order_by="name"))


@rt("/venues/delete/{venue_id}")
def post(venue_id: int):
    venues.delete(venue_id)
    return VenueList(venues(order_by="name"))


serve(port=5045)
