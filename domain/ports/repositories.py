from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models import FileRecord

class FileRepository(ABC):
    @abstractmethod
    async def save(self, file_record: FileRecord) -> bool:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[FileRecord]:
        pass