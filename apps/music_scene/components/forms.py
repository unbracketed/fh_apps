from fasthtml.common import *


def EventForm(event):
    return Form(action=f"/edit_event/{event.id}", method="post", cls="space-y-4")(
        Input(id="title", value=event.title, required=True),
        Input(id="artist", value=event.artist),
        Input(id="date", type="date", value=event.date, required=True),
        Input(id="start_time", type="time", value=event.start_time),
        Input(id="venue", value=event.venue),
        Input(id="url", value=event.url),
        Textarea(id="description", value=event.description, rows=4),
        Hidden(id="id", value=event.id),
        Button("Update Event", type="submit"),
    )

def AddEventForm():
    return Form(action="/add_event", method="post", cls="space-y-4")(
        Input(id="title", placeholder="Event Title", required=True),
        Input(id="artist", placeholder="Artist Name"),
        Input(id="date", type="date", required=True),
        Input(id="start_time", type="time"),
        Input(id="venue", placeholder="Venue"),
        Input(id="url", placeholder="URL"),
        Textarea(id="description", placeholder="Event Description", rows=4),
        Button("Add Event", type="submit")
    )


def LabeledInput(label, _id, _type='text', placeholder=''):
    return Label(cls='block')(
        Span(label, cls='text-gray-700'),
        Input(id=_id, type=_type, placeholder=placeholder, cls='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50')
    )

def LabeledSelect(label, _id, options=[]):
    options = (Option('Corporate event'),
            Option('Wedding'),
            Option('Birthday'),
            Option('Other'))
    return Label(cls='block')(
        Span(label, cls='text-gray-700'),
        Select(
            id=_id,
            cls='block w-full mt-1 rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50')(
            *options
        )
    ),

def FieldGroup(*fields):
    return Div(cls='mt-8 max-w-md')(
        Div(cls='grid grid-cols-1 gap-6')(
            *fields
        )
    )