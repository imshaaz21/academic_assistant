from PyPDF2 import PdfReader
from datetime import datetime
from pathlib import Path
from typing import Dict
import hashlib
from config.settings import PAPERS_DIR


class PaperProcessor:
    def __init__(self):
        self.papers_dir = PAPERS_DIR

    def process_uploaded_file(self, uploaded_file) -> Dict:
        """Process uploaded research paper"""
        try:
            file_path = self.papers_dir / uploaded_file.name
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getvalue())

            content = self._extract_content(file_path)

            paper_id = self._generate_paper_id(uploaded_file.name, content)

            metadata = self._extract_metadata(uploaded_file.name, content)

            return {
                'id': paper_id,
                'title': metadata.get('title', uploaded_file.name),
                'content': content,
                'metadata': metadata,
                'file_path': str(file_path),
                'success': True
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _extract_content(self, file_path: Path) -> str:
        """Extract text content from different file formats"""
        file_extension = file_path.suffix.lower()

        if file_extension == '.pdf':
            return self._extract_pdf_content(file_path)
        elif file_extension == '.txt':
            return self._extract_txt_content(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

    def _extract_pdf_content(self, file_path: Path) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text


    def _extract_txt_content(self, file_path: Path) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _generate_paper_id(self, filename: str, content: str) -> str:
        """Generate unique paper ID"""
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"paper_{content_hash}"

    def _extract_metadata(self, filename: str, content: str) -> Dict:
        """Extract metadata from paper content"""
        lines = content.split('\n')

        title = filename
        for line in lines[:10]:
            if len(line.strip()) > 20 and len(line.strip()) < 200:
                title = line.strip()
                break

        word_count = len(content.split())

        return {
            'title': title,
            'filename': filename,
            'word_count': word_count,
            'processed_at': datetime.now().isoformat()
        }