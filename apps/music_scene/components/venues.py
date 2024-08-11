from fasthtml.common import *
from apps.music_scene.components.layout import Grid
from apps.music_scene.components.elements import SubmitBtn


def VenueList(venues):
    return Div(
        Table(cls="w-full")(
            Thead(
                Tr(
                    Th("Name", cls="text-left"),
                    Th("City", cls="text-left"),
                    Th("State", cls="text-left"),
                    Th("Actions", cls="text-left"),
                )
            ),
            Tbody(*[VenueRow(venue) for venue in venues]),
        ),
    )


def VenueRow(venue):
    return Tr(
        Td(venue.name),
        Td(venue.city),
        Td(venue.state),
        Td(
            A(
                "Edit",
                href=f"/venues/edit/{venue.id}",
                hx_get=f"/venues/edit/{venue.id}",
                hx_target="#venue-list",
                cls="text-blue-500 hover:underline mr-2",
            ),
            A(
                "Delete",
                href=f"/venues/delete/{venue.id}",
                hx_post=f"/venues/delete/{venue.id}",
                hx_target="#venue-list",
                hx_confirm="Are you sure you want to delete this venue?",
                cls="text-red-500 hover:underline",
            ),
        ),
    )


def VenueForm(action, submit_label="Submit", venue_id=None):
    return Form(
        action=action,
        method="post",
        cls="space-y-4",
        hx_post=action,
        hx_target="#venue-list",
        id=f"venue-form-{venue_id}",
    )(
        Grid(cols=2)(
            LabeledInput("Venue Name", "name", required=True),
            LabeledInput("Address", "address"),
            LabeledInput("City", "city"),
            LabeledInput("State", "state"),
            LabeledInput("ZIP Code", "zip_code"),
            LabeledInput("Website", "website"),
            LabeledTextarea("Description", "description"),
        ),
        SubmitBtn(submit_label),
    )


def LabeledInput(label, _id, _type="text", placeholder="", required=False):
    return Label(cls="block")(
        Span(label, cls="text-gray-700"),
        Input(
            id=_id,
            name=_id,
            type=_type,
            placeholder=placeholder,
            required=required,
            cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
        ),
    )


def LabeledTextarea(label, _id, placeholder="", required=False, rows=3):
    return Label(cls="block")(
        Span(label, cls="text-gray-700"),
        Textarea(
            id=_id,
            name=_id,
            rows=rows,
            cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50",
            required=required,
            placeholder=placeholder,
        ),
    )
