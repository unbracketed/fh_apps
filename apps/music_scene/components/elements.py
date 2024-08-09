from fasthtml.common import A, Button


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


def HoverBtnPrimary(label: str, **kwargs):
    return A(cls=_class_str(hover_btn_classes), **kwargs)(label)


def SubmitBtn(label: str, **kwargs):
    return Button(label, cls=_class_str(hover_btn_classes), type="submit", **kwargs)


def SlimBtn(label: str, action, **kwargs):
    css = ["text-white", "bg-lime-600", "px-2", "hover:bg-lime-700", "rounded", kwargs.pop("cls", "")]
    return A(
        href=action,
        hx_get=action,
        hx_target="#event-list",
        cls=" ".join(css),
    )(label)
