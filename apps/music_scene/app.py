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
    404: lambda req, exc: Titled("404: I'm not exist!"),
    418: lambda req, exc: Titled("418: I'm a teapot!"),
    500: lambda req, exc: Titled("500: Hey who turned off the music?"),
}


app, rt = fast_app(
    hdrs=head_section,
    pico=False,
    exception_handlers=exception_handlers,
    htmlkw={"cls": "h-full"},
    bodykw={"cls": "h-full"},
    live=True,
)


@rt("/static/{fname:path}.{ext:static}")
async def get(fname: str, ext: str):
    return FileResponse(f"/static/{fname}.{ext}")


app.get("/")(events_views.home_view)
app.get("/calendar/")(events_views.calendar)
app.get("/events")(events_views.list_view)
app.get("/events/search")(events_views.search_events_handler)
app.post("/events/search")(events_views.search_events_handler)
app.get("/events/detail/{event_id}")(events_views.event_detail)
app.get("/events/add-event-form")(events_views.add_event_form)
app.post("/events/add-event")(events_views.add_event_handler)
app.get("/events/edit-event/{event_id}/")(events_views.edit_event_form)
app.post("/events/edit-event/{event_id}/")(events_views.edit_event_handler)
app.get("/events/copy/{event_id}/")(events_views.copy_event_form)
app.post("/events/delete/{event_id}/")(events_views.delete_event_handler)

app.get("/venues/")(venues_views.index)
app.get("/venues-list/")(venues_views.venues_list)
app.get("/venues/add-venue/")(venues_views.add_venue_form)
app.post("/venues/add-venue/")(venues_views.add_venue_handler)
app.get("/venues/edit/{venue_id}/")(venues_views.edit_venue_form)
app.post("/venues/edit/{venue_id}/")(venues_views.edit_venue_handler)
app.post("/venues/delete/{venue_id}/")(venues_views.delete_venue_handler)


serve(port=5045)
