import os
from pathlib import Path

class StorageAdapter:
    UPLOAD_DIR = Path("certificates")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_file(filename: str, content: bytes):
        file_path = StorageAdapter.UPLOAD_DIR / filename
        with open(file_path, "wb") as f:
            f.write(content)
        return str(file_path)
