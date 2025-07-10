import os
from pathlib import Path
from config.settings import SUPPORTED_FORMATS, MAX_FILE_SIZE


class FileUtils:
    @staticmethod
    def validate_file(file, max_size: int = MAX_FILE_SIZE) -> bool:
        """Validate uploaded file"""
        if file is None:
            return False

        file_ext = os.path.splitext(file.name)[1].lower()
        if file_ext not in SUPPORTED_FORMATS:
            return False

        if len(file.getvalue()) > max_size:
            return False

        return True

    @staticmethod
    def save_file(file, destination: Path) -> bool:
        """Save uploaded file to destination"""
        try:
            with open(destination, 'wb') as f:
                f.write(file.getvalue())
            return True
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return False

    @staticmethod
    def get_file_size(file) -> int:
        """Get file size in bytes"""
        return len(file.getvalue())

    @staticmethod
    def clean_filename(filename: str) -> str:
        """Clean filename for safe storage"""
        return "".join(c for c in filename if c.isalnum() or c in ('.', '_', '-')).rstrip()
