from fasthtml.common import Div, Titled, Title, Link, A, fast_app, serve, Label, Span, Textarea, Input
from starlette.responses import RedirectResponse, FileResponse

from apps.music_scene.components.events import EventDetails
from apps.music_scene.components.layout import Container, layout
from apps.music_scene.models import Event, events
from components.forms import EventForm, AddEventForm, FieldGroup, LabeledInput, LabeledSelect

head_section = (
        Title("Music Scene Cities Labs"),
        Link(
            rel="stylesheet",
            href="/static/base.css",
        ),
)
app, rt = fast_app(hdrs=head_section, pico=False)


@rt("/static/{fname:path}.{ext:static}")
async def get(fname:str, ext:str): return FileResponse(f'/static/{fname}.{ext}')


@rt("/")
@layout()
def get():
    upcoming_events = events(order_by='date')
    return (
        *upcoming_events,
        A("Add New Event", cls="btn btn-primary mt-6 inline-block bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600", href="/add_event"),
        Titled("Form Test", FieldGroup(
            LabeledInput('Full Name', 'full_name'),
            LabeledInput('Email address', 'email', placeholder='john@example.com'),
            LabeledInput('When is your event', 'date', _type='date'),
            LabeledSelect('What type of event is it?', 'event_type'),

            Label(cls='block')(
                Span('Additional details', cls='text-gray-700'),
                Textarea(rows='3',
                         cls='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50')
            ),
            Div(cls='block')(
                Div(cls='mt-2')(
                    Div(
                        Label(cls='inline-flex items-center')(
                            Input(type='checkbox', checked='',
                                  cls='rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-offset-0 focus:ring-indigo-200 focus:ring-opacity-50'),
                            Span('Email me news and special offers', cls='ml-2')
                        )
                    )
                )
            )
        ))
    )

@rt("/add_event")
@layout()
def get():
    return Titled(
        "Add New Event",
        Div(
            AddEventForm()
        )
    )

@rt("/add_event")
def post(title: str, artist: str, date: str, start_time: str, url: str, venue: str, description: str):
    new_event = dict(title=title, artist=artist, date=date, start_time=start_time, venue=venue, url=url, description=description)
    events.insert(new_event)
    return RedirectResponse(url="/", status_code=303)


@rt("/event/{event_id}")
@layout()
def get(event_id: int):
    event = events[event_id]
    return Titled(
        f"Event: {event.title}",
        Div(
            EventDetails(event)
        )
    )


@rt("/edit_event/{event_id}")
def get(event_id: int):
    event = events[event_id]
    return Titled(
        f"Edit Event: {event.title}",
        Container(
            EventForm(event),
            event,
        )
    )

@rt("/edit_event/{event_id}")
def post(event_id: int, title: str, artist: str, date: str, start_time: str, url: str, venue: str, description: str):
    updated_event = Event(id=event_id, title=title, artist=artist, date=date, start_time=start_time, venue=venue, url=url, description=description)
    events.update(updated_event)
    return RedirectResponse(url=f"/event/{event_id}", status_code=303)

serve(port=5045)