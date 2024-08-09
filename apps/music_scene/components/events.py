from datetime import datetime
from fastcore.basics import patch
from fasthtml.common import Card, P, Div, H2, A, H1, Script

from apps.music_scene.components.elements import SlimBtn
from apps.music_scene.components.layout import Grid
from apps.music_scene.models import Event


def _ds_full(date_str):
    """Convert a date string like '2024-03-14' to string like 'Thursday, March 14, 2024'"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%A, %B %d, %Y")


def _ds_short(date_str):
    """Convert a date string like '2024-03-14' to string like 'March 14'"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%B %d")


def _ts_full(time_str):
    """Convert a time string like '20:00' or '20:15'
    to a friendly local time like '8PM' or '8:15PM'."""
    time_obj = datetime.strptime(time_str, "%H:%M")

    if time_obj.minute != 0:
        # If minute is non-zero, include it in the format.
        return time_obj.strftime("%I:%M %p").lstrip("0")
    else:
        # If minute is zero, only include hour in the format.
        return time_obj.strftime("%I %p").lstrip("0")


@patch
def __ft__(self: Event):
    return Card(
        H2(self.title, cls="text-xl font-semibold"),
        P(f"Artist: {self.artist}", cls="text-gray-600") if self.artist else "",
        P(f"Date: {_ds_full(self.date)}", cls="text-sm"),
        P(f"Venue: {self.venue}", cls="text-sm") if self.venue else "",
        Div(cls="mt-2")(
            A(
                href=f"/event/{self.id}",
                cls="btn btn-primary text-blue-500 hover:underline mr-4",
            )("View Details"),
            A(
                href=f"/edit-event/{self.id}",
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
        P(f"Date: {_ds_full(event.date)}", cls="mb-2"),
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
                href=f"/edit-event/{event.id}",
                cls="ml-4 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600",
            ),
            cls="mt-6",
        ),
    )


def CompactEventList(events, **kwargs):
    css_classes = " ".join(["border-b-2", "mt-4", "py-1", kwargs.pop("cls", "")])

    return [
        Grid(cols=12, cls=css_classes)(
            Div(cls="col-span-4 font-bold")("Event Name / Artist"),
            Div(cls="col-span-4 font-bold")("Venue"),
            Div(cls="font-bold")("Date"),
            Div(cls="font-bold")("Time"),
            Div(cls="col-span-2 invisible")(""),
        )
    ] + [
        Div(
            Grid(cols=12, cls=css_classes, id=f"event-row-{event.id}")(
                Div(cls="col-span-4")(
                    f"{event.title}: {event.artist}" if event.artist else event.title
                ),
                Div(cls="col-span-4")(f"{event.venue}" if event.venue else ""),
                Div(_ds_short(event.date)),
                Div(f"{_ts_full(event.start_time)}" if event.start_time else "-"),
                Div(cls="col-span-2")(
                    A(
                        id=f"edit-btn-{event.id}",
                        href=f"/edit-event/{event.id}",
                        cls="underline hover:bg-rose-200 px-1",
                        hx_get=f"/edit-event/{event.id}",
                        hx_target=f"#event-edit-form-{event.id}",
                        hx_swap="innerHTML",
                    )("Edit"),
                    A(
                        href=f"/event/{event.id}",
                        cls="underline hover:bg-blue-200 px-1",
                    )("View"),
                    A(
                        id=f"copy-btn-{event.id}",
                        href=f"/event/copy/{event.id}",
                        cls="underline hover:bg-red-300 px-1",
                        hx_get=f"/event/copy/{event.id}",
                        hx_target=f"#event-edit-form-{event.id}",
                        hx_swap="innerHTML",
                    )("Copy"),
                    A(
                        href=f"/event/delete/{event.id}",
                        cls="underline hover:bg-red-500 px-1",
                        hx_post=f"/event/delete/{event.id}",
                        hx_target="#event-list",
                        hx_confirm=f"Delete {event.name}?"
                    )("Del"),
                ),
            ),
            Div(id=f"event-edit-form-{event.id}", cls="hidden"),
            Script(
                f"""
                me('#edit-btn-{event.id}').on('click', ev => {{
                    me('#event-row-{event.id}').classToggle('hidden');
                    me('#event-edit-form-{event.id}').classToggle('hidden');
                }});
                me('#copy-btn-{event.id}').on('click', ev => {{
                    me('#event-edit-form-{event.id}').classToggle('hidden');
                }});
            """
            ),
        )
        for event in events
    ]


def EventsActions(*args, view_mode="full", **kwargs):
    if view_mode == "full":
        btn = SlimBtn(
            "Compact View", "/compact-view", cls="text-black bg-yellow-50 border"
        )
    else:
        btn = SlimBtn("Full View", "/full-view", cls="bg-lime-500 hover:bg-lime-600")
    add_event = SlimBtn(
        "Add Event", "/add-event", cls="bg-orange-500 hover:bg-orange-600"
    )
    venues_btn = SlimBtn("Venues", "/venues", cls="bg-green-500 hover:bg-green-600")
    return Div(btn, add_event, venues_btn, *args, id="events-actions", **kwargs)
