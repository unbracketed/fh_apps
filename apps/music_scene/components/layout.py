from fasthtml.common import A, Div, H1, Title, uri
from starlette.requests import Request

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
