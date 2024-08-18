from typing import Sequence

from sqlmodel import SQLModel, create_engine, select, Session, col, or_

from apps.music_scene.models import Event

DB_URL = "sqlite:///music_scene_with_sqlmodel.db"
DEBUG = True


def get_db():
    return create_engine(DB_URL, echo=DEBUG)


def init_db():
    engine = get_db()
    SQLModel.metadata.create_all(engine)


def get_event(event_id: int) -> Event | None:
    with Session(get_db()) as session:
        return session.exec(select(Event).where(Event.id == event_id)).one_or_none()


def list_events() -> Sequence[Event]:
    with Session(get_db()) as session:
        return session.exec(select(Event).order_by(Event.date)).fetchall()


def upcoming_events() -> Sequence[Event]:
    raise "TODO"


def create_event(
    title: str,
    date: str,
    artist: str = None,
    start_time: str = None,
    venue_id: int = None,
) -> Event:
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


def update_event(event: Event) -> Event | None:
    with Session(get_db()) as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event


def delete_event(event: Event) -> bool:
    with Session(get_db()) as session:
        session.delete(event)
        return True


def search_events(query: str) -> Sequence[Event]:
    with Session(get_db()) as session:
        query = session.exec(
            select(Event).where(
                or_(
                    col(Event.title).icontains(query),
                    col(Event.artist).icontains(query),
                )
            )
        )
        return query.fetchall()
