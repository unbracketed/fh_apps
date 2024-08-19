from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import make_transient
from sqlmodel import SQLModel, create_engine, select, Session, col, or_, func

from apps.music_scene.models import Event, Venue

DB_URL = "sqlite:///music_scene_with_sqlmodel.db"
DEBUG = True

db = None


def get_db():
    return db if db else create_engine(DB_URL, echo=DEBUG)


def get_session():
    return Session(get_db())


def init_db():
    engine = get_db()
    SQLModel.metadata.create_all(engine)


def get_event(event_id: int) -> Event:
    with get_session() as session:
        event = session.exec(select(Event).where(Event.id == event_id)).one_or_none()
        if event is None:
            raise ValueError(f"Event with id {event_id} not found")
        return event


def list_events(skip: int = 0, limit: int = 100) -> Sequence[Event]:
    with get_session() as session:
        return session.exec(
            select(Event).order_by(Event.date).offset(skip).limit(limit)
        ).fetchall()


def upcoming_events(skip: int = 0, limit: int = 100) -> Sequence[Event]:
    with get_session() as session:
        return session.exec(
            select(Event)
            .where(Event.date >= func.date("now"))
            .order_by(Event.date)
            .offset(skip)
            .limit(limit)
        ).fetchall()


def create_event(
    title: str,
    date: str,
    artist: str = None,
    start_time: str = None,
    venue_id: int = None,
) -> Event:
    try:
        with get_session() as session:
            event = Event(
                title=title,
                date=date,
                artist=artist,
                start_time=start_time,
                venue_id=venue_id,
            )
            session.add(event)
            session.commit()
            session.refresh(event)
            return event
    except SQLAlchemyError as e:
        # Log the error here if you have logging set up
        raise ValueError(f"Failed to create event: {str(e)}")


def update_event(event: Event) -> Event:
    with get_session() as session:
        # Detach the event from any previous session
        make_transient(event)
        # Merge the detached event with the current session
        db_event = session.merge(event)
        # Commit the changes
        session.commit()
        # Refresh to ensure we have the latest data
        session.refresh(db_event)
        return db_event


def delete_event(event: Event) -> bool:
    with get_session() as session:
        db_event = session.exec(select(Event).where(Event.id == event.id)).one_or_none()
        if db_event is None:
            raise ValueError(f"Event with id {event.id} not found")
        session.delete(db_event)
        session.commit()
        return True


def search_events(query: str, skip: int = 0, limit: int = 100) -> Sequence[Event]:
    with get_session() as session:
        return session.exec(
            select(Event)
            .where(
                or_(
                    col(Event.title).icontains(query),
                    col(Event.artist).icontains(query),
                )
            )
            .offset(skip)
            .limit(limit)
        ).fetchall()


def get_events_by_venue(
    venue_id: int, skip: int = 0, limit: int = 100
) -> Sequence[Event]:
    with get_session() as session:
        return session.exec(
            select(Event)
            .where(Event.venue_id == venue_id)
            .order_by(Event.date)
            .offset(skip)
            .limit(limit)
        ).fetchall()


def get_venue(venue_id: int) -> Venue:
    with get_session() as session:
        venue = session.exec(select(Venue).where(Venue.id == venue_id)).one_or_none()
        if venue is None:
            raise ValueError(f"Venue with id {venue_id} not found")
        return venue


def list_venues(skip: int = 0, limit: int = 100) -> Sequence[Venue]:
    with get_session() as session:
        return session.exec(
            select(Venue).order_by(Venue.name).offset(skip).limit(limit)
        ).fetchall()


def create_venue(
    name: str,
    address: str = None,
    city: str = None,
    state: str = None,
    zip_code: str = None,
    website: str = None,
    description: str = None,
) -> Venue:
    if not name:
        raise ValueError("Venue name cannot be empty")
    try:
        with get_session() as session:
            venue = Venue(
                name=name,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                website=website,
                description=description,
            )
            session.add(venue)
            session.commit()
            session.refresh(venue)
            return venue
    except SQLAlchemyError as e:
        raise ValueError(f"Failed to create venue: {str(e)}")


def update_venue(venue: Venue) -> Venue:
    with get_session() as session:
        make_transient(venue)
        # db_venue = session.merge(venue)
        db_venue = session.exec(select(Venue).where(Venue.id == venue.id)).one()
        db_venue.name = venue.name
        db_venue.address = venue.address
        db_venue.city = venue.city
        db_venue.state = venue.state
        db_venue.zip_code = venue.zip_code
        db_venue.website = venue.website
        db_venue.description = venue.description
        session.add(db_venue)
        session.commit()
        session.refresh(db_venue)
        return db_venue


def delete_venue(venue: Venue) -> bool:
    with get_session() as session:
        db_venue = session.exec(select(Venue).where(Venue.id == venue.id)).one_or_none()
        if db_venue is None:
            raise ValueError(f"Venue with id {venue.id} not found")
        session.delete(db_venue)
        session.commit()
        return True


def search_venues(query: str, skip: int = 0, limit: int = 100) -> Sequence[Venue]:
    with get_session() as session:
        return session.exec(
            select(Venue)
            .where(
                or_(
                    col(Venue.name).icontains(query),
                    col(Venue.city).icontains(query),
                    col(Venue.state).icontains(query),
                )
            )
            .offset(skip)
            .limit(limit)
        ).fetchall()


def get_venues_by_city(city: str, skip: int = 0, limit: int = 100) -> Sequence[Venue]:
    with get_session() as session:
        return session.exec(
            select(Venue)
            .where(Venue.city == city)
            .order_by(Venue.name)
            .offset(skip)
            .limit(limit)
        ).fetchall()
