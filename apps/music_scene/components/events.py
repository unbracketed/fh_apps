from datetime import datetime
from fastcore.basics import patch
from fasthtml.common import Card, P, Div, H2, A, H1, Script

from apps.music_scene.components.layout import Grid
from apps.music_scene.models import Event


def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A, %B %d, %Y")


@patch
def __ft__(self: Event):
    return Card(
        H2(self.title, cls="text-xl font-semibold"),
        P(f"Artist: {self.artist}", cls="text-gray-600") if self.artist else "",
        P(f"Date: {format_date(self.date)}", cls="text-sm"),
        P(f"Venue: {self.venue}", cls="text-sm") if self.venue else "",
        Div(cls="mt-2")(
            A(
                href=f"/event/{self.id}",
                cls="btn btn-primary text-blue-500 hover:underline mr-4",
            )("View Details"),
            A(
                href=f"/edit_event/{self.id}",
                cls="btn btn-secondary text-green-500 hover:underline",
            )(
                "Edit",
            ),
        ),
        cls="mb-4 p-4 border rounded",
    )


def EventDetails(event: Event):
    return Div(
        H1(event.title, cls="text-3xl font-bold mb-6"),
        P(f"Artist: {event.artist}", cls="text-xl mb-2") if event.artist else "",
        P(f"Date: {format_date(event.date)}", cls="mb-2"),
        P(f"Start Time: {event.start_time}", cls="text-xl font-semibold")
        if event.start_time
        else "",
        P(f"Venue: {event.venue}", cls="mb-2") if event.venue else "",
        P(event.description, cls="mt-4") if event.description else "",
        A("Event URL", href=event.url, cls="text-blue-500 hover:underline")
        if event.url
        else "",
        Div(
            A(
                "Back to Events",
                href="/",
                cls="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600",
            ),
            A(
                "Edit Event",
                href=f"/edit_event/{event.id}",
                cls="ml-4 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600",
            ),
            cls="mt-6",
        ),
    )


# In events.py


def CompactEventList(events, **kwargs):
    css_classes = " ".join(["border-b-2", "py-1", kwargs.pop("cls", "")])

    return [
        Div(
            Grid(cols=4, cls=css_classes, id=f"event-row-{event.id}")(
                Div(f"{event.title}: {event.artist}" if event.artist else event.title),
                Div(event.date),
                Div(f"{event.start_time}" if event.start_time else "-"),
                Div(
                A( id=f"edit-btn-{event.id}",
                        href=f"/edit_event/{event.id}",
                        cls="underline hover:bg-rose-200 inline-block px-1",
                        hx_get=f"/edit_event/{event.id}",
                        hx_target=f"#event-edit-form-{event.id}",
                        hx_swap="innerHTML"
                    )("Edit"),
                    A(href=f"/event/{event.id}", cls="underline hover:bg-blue-200 inline-block px-1")("View"),
                ),
            ),
            Div(id=f"event-edit-form-{event.id}", cls="hidden"),
            Script(f"""
                me('#edit-btn-{event.id}').on('click', ev => {{
                    me('#event-row-{event.id}').classToggle('hidden');
                    me('#event-edit-form-{event.id}').classToggle('hidden');
                }})
            """)
        )
        for event in events
    ]
