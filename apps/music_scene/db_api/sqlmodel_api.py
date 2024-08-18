from typing import Sequence

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import make_transient
from sqlmodel import SQLModel, create_engine, select, Session, col, or_, func

from apps.music_scene.models import Event

DB_URL = "sqlite:///music_scene_with_sqlmodel.db"
DEBUG = True


def get_db():
    return create_engine(DB_URL, echo=DEBUG)


def init_db():
    engine = get_db()
    SQLModel.metadata.create_all(engine)


def get_event(event_id: int) -> Event:
    with Session(get_db()) as session:
        event = session.exec(select(Event).where(Event.id == event_id)).one_or_none()
        if event is None:
            raise ValueError(f"Event with id {event_id} not found")
        return event


def list_events(skip: int = 0, limit: int = 100) -> Sequence[Event]:
    with Session(get_db()) as session:
        return session.exec(
            select(Event).order_by(Event.date).offset(skip).limit(limit)
        ).fetchall()


def upcoming_events(skip: int = 0, limit: int = 100) -> Sequence[Event]:
    with Session(get_db()) as session:
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
        with Session(get_db()) as session:
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
    with Session(get_db()) as session:
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
    with Session(get_db()) as session:
        db_event = session.exec(select(Event).where(Event.id == event.id)).one_or_none()
        if db_event is None:
            raise ValueError(f"Event with id {event.id} not found")
        session.delete(db_event)
        session.commit()
        return True


def search_events(query: str, skip: int = 0, limit: int = 100) -> Sequence[Event]:
    with Session(get_db()) as session:
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
    with Session(get_db()) as session:
        return session.exec(
            select(Event)
            .where(Event.venue_id == venue_id)
            .order_by(Event.date)
            .offset(skip)
            .limit(limit)
        ).fetchall()
