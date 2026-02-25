from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# Async Engine configuration:
# - pool_pre_ping: Ensures a connection is valid before use
# - pool_size: Base number of connections to keep open
# - max_overflow: Extra connections allowed under high load
engine = create_async_engine(
    settings.DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20
)

# async_sessionmaker is used for asynchronous sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
