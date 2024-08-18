from fasthtml.common import Div, fill_form, uri, FT
from starlette.requests import Request

from apps.music_scene.components.layout import StackedLayout
from apps.music_scene.components.venues import VenueForm, VenuesTable
from apps.music_scene.db_api import (
    list_venues,
    create_venue,
    get_venue,
    update_venue,
    delete_venue,
)
from apps.music_scene.models import Venue


def index(request: Request):
    venue_list = Div(id="venue-list")(
        VenuesTable(list_venues()),
    )
    if request.headers.get("hx-request"):
        return venue_list
    return StackedLayout("Venues", venue_list)


def venues_list() -> FT:
    all_venues = list_venues()
    return Div(id="venue-list")(
        VenuesTable(all_venues),
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
    create_venue(**new_venue)
    return VenuesTable(list_venues())


def add_venue_form() -> FT:
    return Div(id="venue-form")(
        VenueForm("add_venue_form", "Add Venue"),
    )


def edit_venue_form(venue_id: int) -> FT:
    venue = get_venue(venue_id)
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
    updated_venue = dict(
        name=name,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        website=website,
        description=description,
    )
    update_venue(venue_id, **updated_venue)
    return VenuesTable(list_venues())


def delete_venue_handler(venue_id: int) -> FT:
    delete_venue(venue_id)
    return VenuesTable(list_venues())
