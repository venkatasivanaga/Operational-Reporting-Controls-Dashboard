from backend.app.db.base import Base
from backend.app.db.session import engine

# Import models so Base.metadata knows about them
from backend.app.models.control import Control  # noqa: F401
from backend.app.models.incident import Incident  # noqa: F401
from backend.app.models.test_result import TestResult  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
