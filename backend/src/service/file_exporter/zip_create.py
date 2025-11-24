import base64
from io import BytesIO
from typing import List
from zipfile import ZipFile

from src.model.file import FileModel


class ZipService:
    def create(self, files: List[FileModel]) -> BytesIO:
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zipf:
            for file in files:
                zipf.writestr(file.filename, file.content)
        zip_buffer.seek(0)
        return zip_buffer

    def create_base64(self, files: List[FileModel]) -> str:
        zip_bytes = self.create(files).getvalue()
        return base64.b64encode(zip_bytes).decode("utf-8")
