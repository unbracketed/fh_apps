from fasthtml.common import Div, fill_form, uri, FT
from starlette.requests import Request

from apps.music_scene.components.layout import StackedLayout
from apps.music_scene.components.venues import VenueList, VenueForm, ViewActions
from apps.music_scene.models import venues, Venue


def index(request: Request) -> FT:
    venue_list = Div(id="venue-list")(
        VenueList(venues(order_by="name")),
    )
    if request.headers.get("hx-request"):
        return ViewActions(hx_oob_swap="true"), venue_list
    return StackedLayout("Venues", ViewActions(), venue_list)


def venues_list() -> FT:
    all_venues = venues(order_by="name")
    return Div(id="venue-list")(
        VenueList(all_venues),
    )


def add_venue_handler(
    name: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    website: str,
    description: str,
) -> FT:
    new_venue = dict(
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        website=website,
        description=description,
    )
    venues.insert(new_venue)
    return VenueList(venues(order_by="name"))


def add_venue_form() -> FT:
    return Div(id="venue-form")(
        VenueForm("add_venue_form", "Add Venue"),
    )


def edit_venue_form(venue_id: int) -> FT:
    venue = venues[venue_id]
    form = VenueForm(uri("edit_venue_handler", venue_id=venue_id), "Save", venue_id)
    return Div(cls="col-span-4")(fill_form(form, venue))


def edit_venue_handler(
    venue_id: int,
    name: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    website: str,
    description: str,
) -> FT:
    updated_venue = Venue(
        id=venue_id,
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        website=website,
        description=description,
    )
    venues.update(updated_venue)
    # return ViewActions(hx_oob_swap="true"), VenueList(venues(order_by="name"))
    return VenueList(venues(order_by="name"))


def delete_venue_handler(venue_id: int) -> FT:
    venues.delete(venue_id)
    # return ViewActions(hx_oob_swap="true"), VenueList(venues(order_by="name"))
    return VenueList(venues(order_by="name"))
