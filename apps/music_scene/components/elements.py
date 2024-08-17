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
