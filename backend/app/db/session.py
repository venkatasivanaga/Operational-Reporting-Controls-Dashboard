from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.config import settings

# Default to a local SQLite DB file in the backend folder
DEFAULT_SQLITE_URL = "sqlite:///./backend/app.db"

DATABASE_URL = getattr(settings, "database_url", None) or DEFAULT_SQLITE_URL

# SQLite needs check_same_thread=False for typical FastAPI usage
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
