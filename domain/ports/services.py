from abc import ABC, abstractmethod
from typing import Tuple, Optional

class FileConverterService(ABC):
    @abstractmethod
    async def convert_p12_to_pom(self, p12_content: bytes, file_name: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Convert p12 file to pom format
        Returns: (success, pom_content, error_message)
        """
        pass