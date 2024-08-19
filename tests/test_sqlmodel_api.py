from unittest.mock import patch

import pytest

from sqlmodel import SQLModel, Session, create_engine

from apps.music_scene.db_api.sqlmodel_api import get_venue, create_venue, update_venue, delete_venue


@pytest.fixture(scope="function")
def db_session():

    # Register models
    from apps.music_scene.models import Venue, Event

    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    session = Session(engine)

    # Mock get_session function to return mock session object
    with patch('apps.music_scene.db_api.sqlmodel_api.get_session', return_value=session) as mock_get_session:
        yield mock_get_session


    session.close()

def test_create_venue(db_session):
    venue = create_venue(name="Test Venue", city="Test City")
    assert venue.id is not None
    assert venue.name == "Test Venue"
    assert venue.city == "Test City"

def test_get_venue(db_session):
    venue = create_venue(name="Test Venue")
    retrieved_venue = get_venue(venue.id)
    assert retrieved_venue.id == venue.id
    assert retrieved_venue.name == venue.name

def test_update_venue(db_session):
    venue = create_venue(name="Old Name")
    venue.name = "New Name"
    updated_venue = update_venue(venue)
    assert updated_venue.name == "New Name"

def test_delete_venue(db_session):
    venue = create_venue(name="To Be Deleted")
    delete_venue(venue)
    with pytest.raises(ValueError):
        get_venue(venue.id)

@pytest.mark.parametrize("venue_data", [
    {"name": "Venue 1", "city": "City 1"},
    {"name": "Venue 2", "city": "City 2", "state": "State 2"},
])
def test_create_venue_with_different_data(db_session, venue_data):
    venue = create_venue(**venue_data)
    for key, value in venue_data.items():
        assert getattr(venue, key) == value

def test_get_non_existent_venue(db_session):
    with pytest.raises(ValueError):
        get_venue(999)  # Assuming 999 is not a valid venue id

