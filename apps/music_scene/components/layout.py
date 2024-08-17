from functools import lru_cache

import fasthtml.svg as svg
from fasthtml.common import (
    A,
    Div,
    H1,
    Title,
    uri,
    Nav,
    Img,
    Button,
    Span,
    Svg,
    Main,
    H2,
    FT,
    Label,
    Input,
)

from apps.music_scene.components.elements import SlimBtn


def Container(*args, fluid=False, center=True, padding=True, **kwargs):
    """
    A Container component using Tailwind CSS classes.

    :param args: Child elements to be placed in the container
    :param fluid: If True, the container will be full-width on all screen sizes
    :param center: If True, the container will be centered (default)
    :param padding: If True, adds horizontal padding (default)
    :param kwargs: Additional HTML attributes
    """
    classes = [
        "container" if not fluid else "w-full",
        "mx-auto" if center else "",
        "px-4 sm:px-6 lg:px-8" if padding else "",
        kwargs.pop("cls", ""),  # Use 'cls' for additional classes
    ]

    return Div(*args, cls=" ".join(filter(None, classes)), **kwargs)


# This is here to workaround dynamically generated tailwind classes not being found by the tool
_cols_options = [
    "grid-cols-1",
    "grid-cols-2",
    "grid-cols-3",
    "grid-cols-4",
    "grid-cols-5",
    "grid-cols-6",
    "grid-cols-7",
    "grid-cols-8",
    "grid-cols-9",
    "grid-cols-10",
    "grid-cols-11",
    "grid-cols-12",
    "sm:grid-cols-1",
    "sm:grid-cols-2",
    "sm:grid-cols-3",
    "sm:grid-cols-4",
    "sm:grid-cols-5",
    "sm:grid-cols-6",
    "sm:grid-cols-7",
    "sm:grid-cols-8",
    "sm:grid-cols-9",
    "sm:grid-cols-10",
    "sm:grid-cols-11",
    "sm:grid-cols-12",
    "md:grid-cols-1",
    "md:grid-cols-2",
    "md:grid-cols-3",
    "md:grid-cols-4",
    "md:grid-cols-5",
    "md:grid-cols-6",
    "md:grid-cols-7",
    "md:grid-cols-8",
    "md:grid-cols-9",
    "md:grid-cols-10",
    "md:grid-cols-11",
    "md:grid-cols-12",
]


def Grid(*args, cols=1, gap=6, responsive=True, **kwargs):
    """
    A flexible Grid component using Tailwind CSS classes.

    :param args: Child elements to be placed in the grid
    :param cols: Number of columns (1-12) or a dict for responsive breakpoints
    :param gap: Gap size between grid items (0-8)
    :param responsive: Whether to make the grid responsive
    :param kwargs: Additional HTML attributes - use "cls" for additional classes
    """

    col_classes = f"grid-cols-{cols}"

    if responsive and isinstance(cols, int):
        col_classes = f"grid-cols-1 sm:{col_classes}"

    classes = [
        "grid",
        col_classes,
        f"gap-{gap}",
        kwargs.pop("cls", ""),  # Use 'cls' for additional classes
    ]

    return Div(*args, cls=" ".join(filter(None, classes)), **kwargs)


def NavMenu(*args, **kwargs):
    btn = SlimBtn(
        "Events",
        uri("list_view"),
        cls="bg-lime-500 hover:bg-lime-600",
        hx_push_url="true",
    )
    venues_btn = SlimBtn(
        "Venues",
        "index",
        cls="text-white bg-emerald-600 hover:bg-emerald-700",
        hx_push_url="true",
    )
    calendar_btn = SlimBtn(
        "Calendar", "calendar", cls="bg-slate-700 text-white", hx_push_url="true"
    )
    return Div(
        btn,
        venues_btn,
        calendar_btn,
        *args,
        id="nav-menu",
        cls="mb-4",
        **kwargs,
    )


def MultiViewContainer(title, view_actions, *children, **attrs):
    # if the first arg isn't a string, raise an exception
    if not isinstance(title, str):
        raise ValueError("First argument must be a string")
    return (
        Title(f"{title} | Music Scene Manager"),
        Container(
            A(href="/")(
                H1(id="view-title", cls="text-3xl py-4")(f"Music Scene Manager")
            ),
            NavMenu(),
            Div(id="view-panel")(Div(id="view-actions")(view_actions), *children),
            **attrs,
        ),
    )


def COMMENT(*args):
    return ""


def SL_Nav_Profile_Menu():
    return COMMENT(
        Div(cls="hidden sm:ml-6 sm:flex sm:items-center")(
            Button(
                type="button",
                cls="relative rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2",
            )(
                Span(cls="absolute -inset-1.5"),
                Span("View notifications", cls="sr-only"),
                Svg(
                    fill="none",
                    viewbox="0 0 24 24",
                    stroke_width="1.5",
                    stroke="currentColor",
                    aria_hidden="true",
                    cls="h-6 w-6",
                )(
                    svg.Path(
                        stroke_linecap="round",
                        stroke_linejoin="round",
                        d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0",
                    )
                ),
            ),
            Div(cls="relative ml-3")(
                Div(
                    Button(
                        type="button",
                        id="user-menu-button",
                        aria_expanded="false",
                        aria_haspopup="true",
                        cls="relative flex max-w-xs items-center rounded-full bg-white text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2",
                    )(
                        Span(cls="absolute -inset-1.5"),
                        Span("Open user menu", cls="sr-only"),
                        Img(
                            src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
                            alt="",
                            cls="h-8 w-8 rounded-full",
                        ),
                    )
                ),
                Div(
                    role="menu",
                    aria_orientation="vertical",
                    aria_labelledby="user-menu-button",
                    tabindex="-1",
                    cls="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none",
                )(
                    A(
                        "Your Profile",
                        href="#",
                        role="menuitem",
                        tabindex="-1",
                        id="user-menu-item-0",
                        cls="block px-4 py-2 text-sm text-gray-700",
                    ),
                    A(
                        "Settings",
                        href="#",
                        role="menuitem",
                        tabindex="-1",
                        id="user-menu-item-1",
                        cls="block px-4 py-2 text-sm text-gray-700",
                    ),
                    A(
                        "Sign out",
                        href="#",
                        role="menuitem",
                        tabindex="-1",
                        id="user-menu-item-2",
                        cls="block px-4 py-2 text-sm text-gray-700",
                    ),
                ),
            ),
        )
    )


def SL_Nav_Profile_Menu_Mobile():
    return COMMENT(
        Div(cls="border-t border-gray-200 pb-3 pt-4")(
            Div(cls="flex items-center px-4")(
                Div(cls="flex-shrink-0")(
                    Img(
                        src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
                        alt="",
                        cls="h-10 w-10 rounded-full",
                    )
                ),
                Div(cls="ml-3")(
                    Div("Tom Cook", cls="text-base font-medium text-gray-800"),
                    Div("tom@example.com", cls="text-sm font-medium text-gray-500"),
                ),
                Button(
                    type="button",
                    cls="relative ml-auto flex-shrink-0 rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2",
                )(
                    Span(cls="absolute -inset-1.5"),
                    Span("View notifications", cls="sr-only"),
                    Svg(
                        fill="none",
                        viewbox="0 0 24 24",
                        stroke_width="1.5",
                        stroke="currentColor",
                        aria_hidden="true",
                        cls="h-6 w-6",
                    )(
                        svg.Path(
                            stroke_linecap="round",
                            stroke_linejoin="round",
                            d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0",
                        )
                    ),
                ),
            ),
            Div(cls="mt-3 space-y-1")(
                A(
                    "Your Profile",
                    href="#",
                    cls="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800",
                ),
                A(
                    "Settings",
                    href="#",
                    cls="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800",
                ),
                A(
                    "Sign out",
                    href="#",
                    cls="block px-4 py-2 text-base font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-800",
                ),
            ),
        )
    )


@lru_cache(maxsize=4)
def SL_Nav(active_view):
    active = "inline-flex items-center border-b-2 border-indigo-500 px-1 pt-1 text-sm font-medium text-gray-900"
    inactive = "inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700"
    return (
        Nav(cls="border-b border-gray-200 bg-white")(
            Div(cls="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8")(
                Div(cls="flex h-16 justify-between")(
                    Div(cls="flex")(
                        COMMENT(
                            Div(cls="flex flex-shrink-0 items-center")(
                                Img(
                                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600",
                                    alt="Your Company",
                                    cls="block h-8 w-auto lg:hidden",
                                ),
                                Img(
                                    src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600",
                                    alt="Your Company",
                                    cls="hidden h-8 w-auto lg:block",
                                ),
                            )
                        ),
                        Div(cls="hidden sm:-my-px sm:ml-6 sm:flex sm:space-x-8")(
                            A(
                                "Dashboard",
                                href="/",
                                aria_current="page",
                                cls=active if active_view == "Dashboard" else inactive,
                            ),
                            A(
                                "Events",
                                href="/events/",
                                cls=active if active_view == "Events" else inactive,
                            ),
                            A(
                                "Venues",
                                href="/venues/",
                                cls=active if active_view == "Venues" else inactive,
                            ),
                            A(
                                "Calendar",
                                href="/calendar/",
                                cls=active if active_view == "Calendar" else inactive,
                            ),
                        ),
                    ),
                    Div(
                        cls="flex flex-1 items-center justify-center px-2 lg:ml-6 lg:justify-end"
                    )(
                        Div(cls="w-full max-w-lg lg:max-w-xs")(
                            Label("Search", fr="search", cls="sr-only"),
                            Div(cls="relative")(
                                Div(
                                    cls="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3"
                                )(
                                    Svg(
                                        viewbox="0 0 20 20",
                                        fill="currentColor",
                                        aria_hidden="true",
                                        cls="h-5 w-5 text-gray-400",
                                    )(
                                        svg.Path(
                                            fill_rule="evenodd",
                                            d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z",
                                            clip_rule="evenodd",
                                        )
                                    )
                                ),
                                Input(
                                    id="search",
                                    placeholder="Search",
                                    type="search",
                                    post=uri("search_events_handler"),
                                    hx_trigger="input changed delay:500ms, search",
                                    hx_target="#events-table",
                                    cls="block w-full rounded-md border-0 bg-white py-1.5 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                                ),
                            ),
                        )
                    ),
                    SL_Nav_Profile_Menu(),
                    Div(cls="-mr-2 flex items-center sm:hidden")(
                        Button(
                            type="button",
                            aria_controls="mobile-menu",
                            aria_expanded="false",
                            cls="relative inline-flex items-center justify-center rounded-md bg-white p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2",
                        )(
                            Span(cls="absolute -inset-0.5"),
                            Span("Open main menu", cls="sr-only"),
                            Svg(
                                fill="none",
                                viewbox="0 0 24 24",
                                stroke_width="1.5",
                                stroke="currentColor",
                                aria_hidden="true",
                                cls="block h-6 w-6",
                            )(
                                svg.Path(
                                    stroke_linecap="round",
                                    stroke_linejoin="round",
                                    d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5",
                                )
                            ),
                            Svg(
                                fill="none",
                                viewbox="0 0 24 24",
                                stroke_width="1.5",
                                stroke="currentColor",
                                aria_hidden="true",
                                cls="hidden h-6 w-6",
                            )(
                                svg.Path(
                                    stroke_linecap="round",
                                    stroke_linejoin="round",
                                    d="M6 18L18 6M6 6l12 12",
                                )
                            ),
                        )
                    ),
                )
            ),
            Div(id="mobile-menu", cls="sm:hidden")(
                Div(cls="space-y-1 pb-3 pt-2")(
                    A(
                        "Dashboard",
                        href="#",
                        aria_current="page",
                        cls="block border-l-4 border-indigo-500 bg-indigo-50 py-2 pl-3 pr-4 text-base font-medium text-indigo-700",
                    ),
                    A(
                        "Events",
                        href="/events/",
                        cls="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800",
                    ),
                    A(
                        "Venues",
                        href="/venues/",
                        cls="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800",
                    ),
                    A(
                        "Calendar",
                        href="/calendar/",
                        cls="block border-l-4 border-transparent py-2 pl-3 pr-4 text-base font-medium text-gray-600 hover:border-gray-300 hover:bg-gray-50 hover:text-gray-800",
                    ),
                ),
                SL_Nav_Profile_Menu_Mobile(),
            ),
        ),
    )


def SL_Header(title):
    return Div(cls="md:flex md:items-center md:justify-between")(
        Div(cls="min-w-0 flex-1")(
            H2(
                title,
                cls="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight",
            )
        ),
        Div(cls="mt-4 flex md:ml-4 md:mt-0")(
            Button(
                "Edit",
                type="button",
                cls="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50",
            ),
            Button(
                "Publish",
                type="button",
                cls="ml-3 inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600",
            ),
        ),
    )


def StackedLayout(active_view: str, *children, **attrs) -> FT:
    return Div(cls="min-h-full")(
        Title("Music Scene Manager"),
        SL_Nav(active_view),
        Container(
            Div(cls="py-10")(
                # Header(SL_Header(title)),
                Main(
                    Div(cls="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8")(
                        Div(id="view-panel")(*children)
                    ),
                    **attrs,
                ),
            )
        ),
    )
