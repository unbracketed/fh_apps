from fasthtml.common import (
    Div,
    A,
    Table,
    Thead,
    Tr,
    Th,
    Tbody,
    Td,
    Form,
    Label,
    Span,
    Input,
    Textarea,
    Button,
    P,
    H1,
    Dl,
    Dt,
    Dd,
    uri,
)
from apps.music_scene.components.layout import Grid
from apps.music_scene.components.elements import SubmitBtn
from apps.music_scene.models import Venue


def ViewActions(**kwargs):
    # return Div(id="view-actions", **kwargs)(
    #     SlimBtn(
    #         "Add Venue",
    #         uri("add_venue_form"),
    #         cls="bg-lime-300 hover:bg-lime-400",
    #     )
    # )
    return ""


def VenueForm(action, submit_label="Submit", venue_id=None):
    return Form(
        method="post",
        cls="space-y-4",
        post=action,
        hx_target="#view-panel",
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


def VenueRow(venue: Venue, **kwargs):
    return Tr(id=f"venue-row-{venue.id}")(
        Td(
            cls="w-full max-w-0 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:w-auto sm:max-w-none sm:pl-0"
        )(
            venue.name,
            Dl(cls="font-normal lg:hidden")(
                Dt("City", cls="sr-only"),
                Dd(venue.city, cls="mt-1 truncate text-gray-700"),
                Dt("State", cls="sr-only sm:hidden"),
                Dd(venue.state, cls="mt-1 truncate text-gray-500 sm:hidden"),
            ),
        ),
        Td(venue.city, cls="hidden px-3 py-4 text-sm text-gray-500 lg:table-cell"),
        Td(venue.state, cls="hidden px-3 py-4 text-sm text-gray-500 sm:table-cell"),
        Td("numEvents", cls="px-3 py-4 text-sm text-gray-500"),
        Td(cls="py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0")(
            A(
                href="#",
                cls="text-indigo-600 hover:text-indigo-900",
                get=uri("edit_venue_form", venue_id=venue.id),
                hx_target=f"#venue-row-{venue.id}",
            )("Edit", Span(f", {venue.name}", cls="sr-only")),
            A(
                "Delete",
                href="#",
                post=uri("delete_venue_handler", venue_id=venue.id),
                hx_target="#view-panel",
                hx_confirm="Are you sure you want to delete this venue?",
                cls="text-red-500 hover:underline",
            ),
        ),
    )


def VenuesTable(venues, **kwargs):
    rows = [VenueRow(venue) for venue in venues]
    return Div(id="venues-table", cls="px-4 sm:px-6 lg:px-8")(
        Div(cls="sm:flex sm:items-center")(
            Div(cls="sm:flex-auto")(
                H1("Venues", cls="text-base font-semibold leading-6 text-gray-900"),
                P("A list of all the venues.", cls="mt-2 text-sm text-gray-700"),
            ),
            Div(cls="mt-4 sm:ml-16 sm:mt-0 sm:flex-none")(
                Button(
                    "Add venue",
                    get=uri("add_venue_form"),
                    hx_target="#venues-table",
                    type="button",
                    cls="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600",
                )
            ),
        ),
        Div(cls="-mx-4 mt-8 sm:-mx-0")(
            Table(cls="min-w-full divide-y divide-gray-300")(
                Thead(
                    Tr(
                        Th(
                            "Name",
                            scope="col",
                            cls="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0",
                        ),
                        Th(
                            "City",
                            scope="col",
                            cls="hidden px-3 py-3.5 text-left text-sm font-semibold text-gray-900 lg:table-cell",
                        ),
                        Th(
                            "State",
                            scope="col",
                            cls="hidden px-3 py-3.5 text-left text-sm font-semibold text-gray-900 sm:table-cell",
                        ),
                        Th(
                            "Events",
                            scope="col",
                            cls="px-3 py-3.5 text-left text-sm font-semibold text-gray-900",
                        ),
                        Th(scope="col", cls="relative py-3.5 pl-3 pr-4 sm:pr-0")(
                            Span("Edit", cls="sr-only")
                        ),
                    )
                ),
                Tbody(cls="divide-y divide-gray-200 bg-white")(*rows),
            )
        ),
    )
