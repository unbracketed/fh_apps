from fasthtml import Div, fill_form

from apps.music_scene.components.venues import VenueList, VenueForm
from apps.music_scene.models import venues, Venue


def venues_list():
    all_venues = venues(order_by="name")
    return (
        Div(id="venue-list")(
            VenueList(all_venues),
        ),
        # Div(id="venue-form")(
        #     VenueForm("/venues/add", "Add Venue"),
        # ),
    )


def add_venue_handler(
    name: str,
    address: str,
    city: str,
    state: str,
    zip_code: str,
    website: str,
    description: str,
):
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


def edit_venue_form(venue_id: int):
    venue = venues[venue_id]
    form = VenueForm(f"/venues/edit/{venue_id}", "Save", venue_id)
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
):
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
    return VenueList(venues(order_by="name"))


def delete_venue_handler(venue_id: int):
    venues.delete(venue_id)
    return VenueList(venues(order_by="name"))