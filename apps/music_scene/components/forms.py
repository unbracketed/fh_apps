from fasthtml.common import *

from apps.music_scene.components.elements import SubmitBtn, HoverBtnPrimary


def EventForm(action, submit_label="Submit"):
    return Form(action=action, method="post", cls="space-y-4")(
        FieldGroup(
            LabeledInput("Event Title", "title", required=True),
            LabeledInput(
                "Artist",
                "artist",
                placeholder="Artist, band name, or  name of performing act",
            ),
            LabeledInput("Date", "date", _type="date", required=True),
            LabeledInput("Start Time", "start_time", _type="time"),
            LabeledInput(
                "Venue", "venue", placeholder="Venue name or location of event"
            ),
            LabeledInput("URL", "url"),
            LabeledTextarea("Event Description", "description"),
            SubmitBtn(submit_label),
            HoverBtnPrimary(
                "Cancel", hx_get="/control-panel", hx_target="#control-panel"
            ),
        )
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
    options = (
        Option("Corporate event"),
        Option("Wedding"),
        Option("Birthday"),
        Option("Other"),
    )
    return Label(cls="block")(
        Span(label, cls="text-gray-700"),
        Select(
            id=_id,
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
