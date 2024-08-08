import functools

from fasthtml.common import Div, H1, Title

from apps.music_scene.components.elements import HoverBtnPrimary


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

    # if isinstance(cols, dict):
    #     col_classes = " ".join([f"{bp}:grid-cols-{n}" for bp, n in cols.items()])
    # else:
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


def Layout(*args, **kwargs):
    """Layout for the blog, but can be adapted to anything"""
    # return Title(title), blog_header(), Main(*args, **kwargs), blog_footer()
    title = kwargs.get("title", "Music Scene Calendar")
    return Title(title), Container(H1(cls="text-3xl py-4")(title), *args, **kwargs)


def layout(*dec_args, **dec_kwargs):
    """Decorator factory to wrap a view function with a layout"""

    def decorator(view_function):
        @functools.wraps(view_function)
        def _wrapper(*args, **kwargs):
            result = view_function(*args, **kwargs)
            # Custom processing if needed
            # ...
            return Layout(*result, *dec_args, **dec_kwargs)

        return _wrapper

    return decorator


def ControlPanel(*args, **kwargs):
    return Div(_id="control-panel", cols=2)(
        HoverBtnPrimary(
            "Add Event",
            href="/add_event",
            hx_target="#control-panel",
            hx_get="/add_event",
        )
    )
