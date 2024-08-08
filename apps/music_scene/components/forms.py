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
        FieldGroup(
            LabeledInput("Event Title", "title", required=True),
            #Input(id="title", placeholder="Event Title", required=True),
            Input(id="artist", placeholder="Artist Name"),
            Input(id="date", type="date", required=True),
            Input(id="start_time", type="time"),
            Input(id="venue", placeholder="Venue"),
            Input(id="url", placeholder="URL"),
            Textarea(id="description", placeholder="Event Description", rows=4),
            Button("Add Event", type="submit", cls="btn btn-primary"),
        )
    )


def LabeledInput(label, _id, _type='text', placeholder='', required=False):
    return Label(cls='block')(
        Span(label, cls='text-gray-700'),
        Input(
            id=_id,
            type=_type,
            placeholder=placeholder,
            required=required,
            cls='mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50')
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


def Example():
    return Titled("Form Test", FieldGroup(
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