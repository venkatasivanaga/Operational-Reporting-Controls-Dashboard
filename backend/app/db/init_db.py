from backend.app.db.base import Base
from backend.app.db.session import engine


def init_db() -> None:
    # For now, create tables directly. We'll switch to Alembic migrations soon.
    Base.metadata.create_all(bind=engine)
