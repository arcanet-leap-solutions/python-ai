from app.domain.models import FileRecord
from app.domain.ports.repositories import FileRepository
from app.domain.ports.services import FileConverterService
from typing import Tuple, Optional
import os


class P12ProcessorService:
    def __init__(self, file_repository: FileRepository, file_converter: FileConverterService):
        self.file_repository = file_repository
        self.file_converter = file_converter

    async def process_p12_file(self,
                               file_content: bytes,
                               file_name: str,
                               config_id: str) -> Tuple[bool, Optional[str]]:
        """
        Process P12 file and store results in database
        Returns: (success, error_message)
        """
        try:
            # Extract ID from filename (removing extension)
            file_id = os.path.splitext(file_name)[0]

            # Convert p12 to pom
            success, pom_content, error = await self.file_converter.convert_p12_to_pom(file_content, file_name)

            if not success:
                return False, f"Error converting file: {error}"

            # Create file record
            file_record = FileRecord(
                id=file_id,
                file_name=file_name,
                config_id=config_id,
                pom_content=pom_content
            )

            # Save to database
            saved = await self.file_repository.save(file_record)

            if not saved:
                return False, "Error saving to database"

            return True, None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"