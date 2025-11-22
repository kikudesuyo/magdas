import glob
import os
from io import BytesIO
from typing import List, Tuple
from zipfile import ZipFile

from src.model.file import FileModel


class FileService:
    def create(self, file_bytes: bytes) -> BytesIO:
        buffer = BytesIO(file_bytes)
        buffer.seek(0)
        return buffer


class ZipService:
    def create(self, files: List[FileModel]) -> BytesIO:
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zipf:
            for file in files:
                zipf.writestr(file.filename, file.content)
        zip_buffer.seek(0)
        return zip_buffer
