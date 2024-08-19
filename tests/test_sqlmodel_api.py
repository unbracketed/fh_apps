from datetime import date
from unittest.mock import patch

import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import make_transient

from sqlmodel import SQLModel, Session, create_engine

from apps.music_scene.db_api.sqlmodel_api import get_venue, create_venue, update_venue, delete_venue
from apps.music_scene.models import Venue


@pytest.fixture
def db_engine():
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def db_session(db_engine):

    # Register models
    from apps.music_scene.models import Venue, Event

    session = Session(db_engine)

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


def test_create_venue_with_invalid_data(db_session):
    with pytest.raises(
            ValueError):  # Assuming your create_venue function raises ValueError for invalid data
        create_venue(name="")  # Assuming name is a required field


def test_update_nonexistent_venue(db_session):
    non_existent_venue = Venue(id=999, name="Non-existent")
    with pytest.raises(NoResultFound):
        update_venue(non_existent_venue)


def test_delete_nonexistent_venue(db_session):
    non_existent_venue = Venue(id=999, name="Non-existent")
    with pytest.raises(ValueError):
        delete_venue(non_existent_venue)


def test_create_venue_with_events(db_engine, db_session):
    from apps.music_scene.db_api.sqlmodel_api import create_event
    from sqlmodel import select, Session
    from sqlalchemy.orm import selectinload

    venue = create_venue(name="Venue with Events")
    create_event(title="Event 1", date=date.today(), venue_id=venue.id)
    create_event(title="Event 2", date=date.today(), venue_id=venue.id)

    # Use a new session to ensure we're not working with cached data
    with Session(db_engine) as session:
        statement = select(Venue).options(selectinload(Venue.events)).where(Venue.id == venue.id)
        retrieved_venue = session.exec(statement).one()

        assert len(retrieved_venue.events) == 2
        assert retrieved_venue.events[0].title in ["Event 1", "Event 2"]
        assert retrieved_venue.events[1].title in ["Event 1", "Event 2"]
        assert retrieved_venue.events[1].date == date.today()
        assert retrieved_venue.events[1].venue_id == venue.id

def test_list_venues(db_session):
    from apps.music_scene.db_api.sqlmodel_api import list_venues
    create_venue(name="Venue 1")
    create_venue(name="Venue 2")
    create_venue(name="Venue 3")

    venues = list_venues()
    assert len(venues) == 3
    assert {venue.name for venue in venues} == {"Venue 1", "Venue 2", "Venue 3"}


def test_search_venues(db_session):
    from apps.music_scene.db_api.sqlmodel_api import search_venues
    create_venue(name="Rock Venue", city="New York")
    create_venue(name="Jazz Club", city="Chicago")
    create_venue(name="Blues Bar", city="New Orleans")

    results = search_venues("Rock")
    assert len(results) == 1
    assert results[0].name == "Rock Venue"

    results = search_venues("New")
    assert len(results) == 2
    assert {venue.name for venue in results} == {"Rock Venue", "Blues Bar"}
