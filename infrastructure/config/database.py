from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

# Database URL from environment or use SQLite as fallback
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite+aiosqlite:///./p12_processor.db")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()


class FileRecordTable(Base):
    __tablename__ = "file_records"

    id = Column(String, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    config_id = Column(String, nullable=False)
    pom_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


async def get_db():
    """Database dependency for FastAPI endpoints"""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)