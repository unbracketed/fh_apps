from fasthtml.common import (
    Div,
    A,
    uri,
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Dl,
    Dt,
    Dd,
    Td,
    Span,
    H1,
    P,
    Button,
)

from apps.music_scene.components.layout import Grid, JustifiedSearchInput
from apps.music_scene.models import Event
from apps.music_scene.utils import _ds_full, _ds_short, _ts_full


def ViewActions(**kwargs):
    # return Div(id="view-actions", **kwargs)(
    #     SlimBtn(
    #         "Add Event",
    #         uri("add_event_form"),
    #         cls="text-white bg-orange-500 hover:bg-orange-600",
    #     )
    # )
    return ""


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
    css_classes = " ".join(
        [
            "border-b-2",
            "border-slate-700",
            "mt-4",
            "py-1",
            "px-2",
            kwargs.pop("cls", ""),
        ]
    )

    return [
        Grid(cols=12, cls=f"{css_classes} border-b-4")(
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
                        href="#",
                        cls="underline hover:bg-rose-200 px-1",
                        get=uri("edit_event_form", event_id=event.id),
                        hx_target=f"#event-row-{event.id}",
                    )("Edit"),
                    A(
                        href="#",
                        cls="underline hover:bg-blue-200 px-1",
                        get=uri("event_detail", event_id=event.id),
                        hx_target=f"#event-row-{event.id}",
                    )("View"),
                    A(
                        href="#",
                        cls="underline hover:bg-red-300 px-1",
                        get=uri("copy_event_form", event_id=event.id),
                        hx_target=f"#event-row-{event.id}",
                    )("Copy"),
                    A(
                        href="#",
                        cls="underline hover:bg-red-500 px-1",
                        post=uri("delete_event_handler", event_id=event.id),
                        hx_target="#view-panel",
                        hx_confirm=f"Delete {event.name}?",
                    )("Del"),
                ),
            ),
            Div(id=f"event-edit-form-{event.id}", cls="hidden"),
        )
        for event in events
    ]


def EventRow(event: Event, **kwargs):
    stacked_details_items = [
        Dt("Title", cls="sr-only"),
        Dd(event.artist, cls="mt-1 truncate text-gray-700"),
    ]
    if event.venue:
        stacked_details_items.extend(
            [
                Dt("Venue", cls="sr-only sm:hidden"),
                Dd(event.venue.name, cls="mt-1 truncate text-gray-500 sm:hidden"),
            ]
        )
    stacked_details = Dl(cls="font-normal lg:hidden")(*stacked_details_items)
    return Tr(id=f"event-row-{event.id}")(
        Td(
            cls="w-full max-w-0 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:w-auto sm:max-w-none sm:pl-0"
        )(
            event.title,
            stacked_details,
        ),
        Td(event.artist, cls="hidden px-3 py-4 text-sm text-gray-500 lg:table-cell"),
        Td(
            event.venue.name if event.venue else "",
            cls="hidden px-3 py-4 text-sm text-gray-500 sm:table-cell",
        ),
        Td(_ds_short(event.date), cls="px-3 py-4 text-sm text-gray-500"),
        Td(
            _ts_full(event.start_time) if event.start_time else "",
            cls="px-3 py-4 text-sm text-gray-500",
        ),
        Td(cls="py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0")(
            A(
                href="#",
                cls="text-indigo-600 hover:text-indigo-900",
                get=uri("edit_event_form", event_id=event.id),
                hx_target=f"#event-row-{event.id}",
            )("Edit", Span(f", {event.title}", cls="sr-only")),
            A(
                href="#",
                cls="text-indigo-600 hover:text-indigo-900",
                get=uri("copy_event_form", event_id=event.id),
                hx_target="#events-table",
            )("Copy", Span(f", {event.title}", cls="sr-only")),
            A(
                href="#",
                cls="underline hover:bg-red-500 px-1",
                post=uri("delete_event_handler", event_id=event.id),
                hx_target="#events-table",
                hx_confirm=f"Delete {event.name}?",
            )("Delete"),
        ),
    )


def EventsTableBody(events):
    rows = [EventRow(event) for event in events]
    return (
        Tbody(id="events-table-body", cls="divide-y divide-gray-200 bg-white")(*rows),
    )


def EventsTable(events, **kwargs):
    return Div(id="events-table", cls="px-4 sm:px-6 lg:px-8")(
        Div(cls="sm:flex sm:items-center")(
            Div(cls="sm:flex-auto")(
                H1("Events", cls="text-base font-semibold leading-6 text-gray-900"),
                P("A list of all the events.", cls="mt-2 text-sm text-gray-700"),
            ),
            JustifiedSearchInput("events"),
            Div(cls="mt-4 sm:ml-16 sm:mt-0 sm:flex-none")(
                Button(
                    "Add event",
                    get=uri("add_event_form"),
                    hx_target="#events-table",
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
                            "Title",
                            scope="col",
                            cls="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0",
                        ),
                        Th(
                            "Artist",
                            scope="col",
                            cls="hidden px-3 py-3.5 text-left text-sm font-semibold text-gray-900 lg:table-cell",
                        ),
                        Th(
                            "Venue",
                            scope="col",
                            cls="hidden px-3 py-3.5 text-left text-sm font-semibold text-gray-900 sm:table-cell",
                        ),
                        Th(
                            "Date",
                            scope="col",
                            cls="px-3 py-3.5 text-left text-sm font-semibold text-gray-900",
                        ),
                        Th(
                            "Start Time",
                            scope="col",
                            cls="px-3 py-3.5 text-left text-sm font-semibold text-gray-900",
                        ),
                        Th(scope="col", cls="relative py-3.5 pl-3 pr-4 sm:pr-0")(
                            Span("Edit", cls="sr-only")
                        ),
                    )
                ),
                EventsTableBody(events),
            )
        ),
    )
