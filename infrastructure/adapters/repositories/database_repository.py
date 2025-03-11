from app.domain.ports.repositories import FileRepository
from app.domain.models import FileRecord
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.infrastructure.config.database import FileRecordTable


class DatabaseFileRepository(FileRepository):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def save(self, file_record: FileRecord) -> bool:
        try:
            db_record = FileRecordTable(
                id=file_record.id,
                file_name=file_record.file_name,
                config_id=file_record.config_id,
                pom_content=file_record.pom_content,
                created_at=file_record.created_at
            )

            self.db_session.add(db_record)
            await self.db_session.commit()
            return True
        except SQLAlchemyError:
            await self.db_session.rollback()
            return False

    async def get_by_id(self, id: str) -> Optional[FileRecord]:
        try:
            query = select(FileRecordTable).where(FileRecordTable.id == id)
            result = await self.db_session.execute(query)
            record = result.scalars().first()

            if not record:
                return None

            return FileRecord(
                id=record.id,
                file_name=record.file_name,
                config_id=record.config_id,
                pom_content=record.pom_content,
                created_at=record.created_at
            )
        except SQLAlchemyError:
            return None