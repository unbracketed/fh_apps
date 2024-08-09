from fasthtml.common import *
from apps.music_scene.components.layout import Grid
from apps.music_scene.components.elements import SubmitBtn
from apps.music_scene.models import venues


def EventForm(action, submit_label="Submit", event_id=None):
    all_venues = venues(order_by="name")
    return Div(
        id=f"event-form-{event_id}",
        cls="py-4 px-2 bg-orange-200 border-solid border-2 border-orange-600",
    )(
        H2("Edit Event", cls="text-2xl mb-4"),
        Form(
            action=action,
            method="post",
            cls="space-y-4",
            hx_post=action,
            hx_target=f"#event-list",
        )(
            Grid(cols=2)(
                LabeledInput("Event Title", "title", required=True),
                LabeledInput(
                    "Artist",
                    "artist",
                    placeholder="Artist, band name, or name of performing act",
                ),
                LabeledInput("Date", "date", _type="date", required=True),
                LabeledInput("Start Time", "start_time", _type="time"),
                LabeledSelect(
                    "Venue",
                    "venue_id",
                    options=[
                        Option(venue.name, value=str(venue.id)) for venue in all_venues
                    ],
                ),
                LabeledInput("URL", "url"),
                LabeledTextarea("Event Description", "description"),
            ),
            SubmitBtn(submit_label),
            Button(
                "Cancel",
                cls="btn btn-secondary cancel-btn",
            ),
            Script(
                f"""me(".cancel-btn").on("click", ev => me("#event-form-{event_id}").fadeOut() )"""
            ),
        ),
    )


def LabeledInput(label, _id, _type="text", placeholder="", required=False):
    return Label(cls="block")(
        Span(label, cls="text-gray-700"),
        Input(
            id=_id,
            type=_type,
            placeholder=placeholder,
            required=required,
            cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
        ),
    )


def LabeledSelect(label, _id, options=[]):
    return Label(cls="block")(
        Span(label, cls="text-gray-700"),
        Select(
            id=_id,
            name=_id,
            cls="block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
        )(*options),
    )


def _class_str(c: list) -> str:
    return " ".join(c)


def LabeledTextarea(label, _id, placeholder="", required=False, rows=3):
    textarea_classes = [
        "mt-1",
        "block",
        "w-full",
        "rounded-md",
        "border-gray-300",
        "shadow-sm",
        "focus:border-indigo-300",
        "focus:ring",
        "focus:ring-indigo-200",
        "focus:ring-opacity-50",
    ]
    return Label(cls="block")(
        Span(label, cls="text-gray-700"),
        Textarea(
            id=_id,
            rows=rows,
            cls=_class_str(textarea_classes),
            required=required,
            placeholder=placeholder,
        ),
    )


def FieldGroup(*fields):
    return Div(cls="mt-8 max-w-md")(Div(cls="grid grid-cols-1 gap-6")(*fields))


def Example():
    return Titled(
        "Form Test",
        FieldGroup(
            LabeledInput("Full Name", "full_name"),
            LabeledInput("Email address", "email", placeholder="john@example.com"),
            LabeledInput("When is your event", "date", _type="date"),
            LabeledSelect("What type of event is it?", "event_type"),
            Label(cls="block")(
                Span("Additional details", cls="text-gray-700"),
                Textarea(
                    rows="3",
                    cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
                ),
            ),
            Div(cls="block")(
                Div(cls="mt-2")(
                    Div(
                        Label(cls="inline-flex items-center")(
                            Input(
                                type="checkbox",
                                checked="",
                                cls="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-offset-0 focus:ring-indigo-200 focus:ring-opacity-50",
                            ),
                            Span("Email me news and special offers", cls="ml-2"),
                        )
                    )
                )
            ),
        ),
    )
