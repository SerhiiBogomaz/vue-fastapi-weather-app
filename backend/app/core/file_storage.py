from pathlib import Path
from fastapi import UploadFile
from fastapi import HTTPException, status

class FileStorageConfig:
    def __init__(self) -> None:
        self.AVATAR_DIR = Path('static/avatars')
        self.AVATAR_DIR.mkdir(exist_ok=True, parents=True)
        self.ALLOWED_TYPES = ['image/jpeg', 'image/png']
        self.MAX_SIZE = 2 * 1024 * 1024

    def validate_file(self, file: UploadFile) -> None:
        if file.content_type not in self.ALLOWED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed: {', '.join(self.ALLOWED_TYPES)}"
            )

        if file.size is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not determine file size"
                )

        if file.size > self.MAX_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail={
                    "error": "File too large",
                    "max_size_mb": self.MAX_SIZE // (1024 * 1024),
                    "actual_size_mb": file.size // (1024 * 1024)
                }
            )


file_storage = FileStorageConfig()
