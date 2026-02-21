from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

# Engine configuration with production settings:
# - pool_pre_ping: Ensures a connection is valid before use
# - pool_size: Base number of connections to keep open
# - max_overflow: Extra connections allowed under high load
engine = create_engine(
    settings.DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
