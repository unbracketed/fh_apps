from typing import List

from fasthtml.common import (
    A,
    Button,
    Div,
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
)


def _class_str(c):
    return " ".join(c)


hover_btn_classes = [
    "btn",
    "btn-primary",
    "inline-block",
    "bg-orange-500",
    "text-white",
    "py-2",
    "px-4",
    "rounded",
    "hover:bg-orange-600",
]


def SubmitBtn(label: str, **kwargs):
    return Button(label, cls=_class_str(hover_btn_classes), type="submit", **kwargs)


def SlimBtn(label: str, action, **kwargs):
    css = ["px-2", "rounded", kwargs.pop("cls", "")]
    return A(
        href="#", get=action, hx_target="#view-panel", cls=" ".join(css), **kwargs
    )(label)


def ResponsiveRow(items, summary: dict, **kwargs):
    first, *rest = items
    if summary:
        compact_row = Dl(cls="font-normal lg:hidden")(
            *[
                (Dt(k, cls="sr-only"), Dd(v, cls="mt-1 truncate text-gray-700"))
                for k, v in summary.items()
            ]
        )
        #     Dt('Title', cls='sr-only'),
        #     Dd('Front-end Developer', cls='mt-1 truncate text-gray-700'),
        #     Dt('Email', cls='sr-only sm:hidden'),
        #     Dd('lindsay.walton@example.com', cls='mt-1 truncate text-gray-500 sm:hidden')
        # )
    return Tr(
        Td(
            cls="w-full max-w-0 py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:w-auto sm:max-w-none sm:pl-0"
        )(first, compact_row),
        Td(
            "Front-end Developer",
            cls="hidden px-3 py-4 text-sm text-gray-500 lg:table-cell",
        ),
        Td(
            "lindsay.walton@example.com",
            cls="hidden px-3 py-4 text-sm text-gray-500 sm:table-cell",
        ),
        Td("Member", cls="px-3 py-4 text-sm text-gray-500"),
        Td(cls="py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0")(
            A(href="#", cls="text-indigo-600 hover:text-indigo-900")(
                "Edit", Span(", Lindsay Walton", cls="sr-only")
            )
        ),
    )


def ResponsiveTable(headings: List[str], *rows, **kwargs):
    thead = Thead(
        Tr(
            *[
                Th(
                    heading,
                    scope="col",
                    cls="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0",
                )
                for heading in headings
            ],
            Th(scope="col", cls="relative py-3.5 pl-3 pr-4 sm:pr-0")(
                Span("Edit", cls="sr-only")
            )
        )
    )

    return Div(cls="px-4 sm:px-6 lg:px-8")(
        Div(cls="sm:flex sm:items-center")(
            Div(cls="sm:flex-auto")(
                H1("Users", cls="text-base font-semibold leading-6 text-gray-900"),
                P(
                    "A list of all the users in your account including their name, title, email and role.",
                    cls="mt-2 text-sm text-gray-700",
                ),
            ),
            Div(cls="mt-4 sm:ml-16 sm:mt-0 sm:flex-none")(
                Button(
                    "Add user",
                    type="button",
                    cls="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600",
                )
            ),
        ),
        Div(cls="-mx-4 mt-8 sm:-mx-0")(
            Table(cls="min-w-full divide-y divide-gray-300")(
                thead, Tbody(cls="divide-y divide-gray-200 bg-white")(*rows)
            )
        ),
    )
