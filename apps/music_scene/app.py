from fasthtml.common import Titled, Link, fast_app, serve
from starlette.responses import FileResponse

import apps.music_scene.views.events as events_views
import apps.music_scene.views.venues as venues_views


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

app.add_route("/venues", venues_views.index)
app.add_route("/venues-list", venues_views.venues_list)
app.add_route("/venues/add-venue", venues_views.add_venue_handler, methods=["POST"])
app.add_route("/venues/edit/{venue_id}", venues_views.edit_venue_form)
app.add_route(
    "/venues/edit/{venue_id}", venues_views.edit_venue_handler, methods=["POST"]
)
app.add_route(
    "/venues/delete/{venue_id}", venues_views.delete_venue_handler, methods=["POST"]
)


serve(port=5045)
