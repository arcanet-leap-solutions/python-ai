import os
from pathlib import Path

class StorageAdapter:
    STORAGE_PATH = "storage/"  # Se puede cambiar a una URL remota

    @staticmethod
    def upload_file(filename: str, file_content: bytes):
        # Crear la carpeta de almacenamiento si no existe
        os.makedirs(StorageAdapter.STORAGE_PATH, exist_ok=True)
        
        file_path = os.path.join(StorageAdapter.STORAGE_PATH, filename)
        
        with open(file_path, "wb") as f:
            f.write(file_content)

        return f"/{StorageAdapter.STORAGE_PATH}{filename}"  # Retornar la URL relativa o remota
    
