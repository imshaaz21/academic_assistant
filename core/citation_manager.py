import json
import os
import uuid
import pandas as pd
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from config.settings import CITATIONS_DIR


class CitationManager:
    def __init__(self):
        self.citations_dir = CITATIONS_DIR
        # Ensure directory exists
        os.makedirs(self.citations_dir, exist_ok=True)
        self.citations_file = self.citations_dir / "citations.json"
        self.citations = self._load_citations()

    def _load_citations(self) -> List[Dict[str, Any]]:
        """Load citations from storage"""
        if self.citations_file.exists():
            try:
                with open(self.citations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading citations: {e}")
                return []
        return []

    def _save_citations(self) -> None:
        """Save citations to storage"""
        try:
            # Ensure directory exists
            os.makedirs(self.citations_dir, exist_ok=True)

            with open(self.citations_file, 'w', encoding='utf-8') as f:
                json.dump(self.citations, f, indent=2)
        except (IOError, OSError) as e:
            print(f"Error saving citations: {e}")

    def add_citation(self, paper_data: Dict[str, Any]) -> str:
        """Add a new citation"""
        if not paper_data:
            paper_data = {}

        citation = {
            'id': paper_data.get('id', self._generate_citation_id()),
            'title': paper_data.get('title', ''),
            'authors': paper_data.get('authors', []),
            'year': paper_data.get('year', datetime.now().year),
            'journal': paper_data.get('journal', ''),
            'volume': paper_data.get('volume', ''),
            'pages': paper_data.get('pages', ''),
            'doi': paper_data.get('doi', ''),
            'url': paper_data.get('url', ''),
            'abstract': paper_data.get('abstract', ''),
            'keywords': paper_data.get('keywords', []),
            'added_at': datetime.now().isoformat(),
            'notes': paper_data.get('notes', '')
        }

        self.citations.append(citation)
        self._save_citations()
        return citation['id']

    def get_citation(self, citation_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific citation"""
        for citation in self.citations:
            if citation['id'] == citation_id:
                return citation
        return None

    def get_all_citations(self) -> List[Dict[str, Any]]:
        """Get all citations"""
        return self.citations

    def search_citations(self, query: str) -> List[Dict[str, Any]]:
        """Search citations by title, authors, or keywords"""
        if not query:
            return self.get_all_citations()

        results = []
        query_lower = query.lower()

        for citation in self.citations:
            if query_lower in citation['title'].lower():
                results.append(citation)
                continue

            for author in citation['authors']:
                if query_lower in author.lower():
                    results.append(citation)
                    break

            for keyword in citation['keywords']:
                if query_lower in keyword.lower():
                    results.append(citation)
                    break

        return results

    def delete_citation(self, citation_id: str) -> bool:
        """Delete a citation"""
        for i, citation in enumerate(self.citations):
            if citation['id'] == citation_id:
                del self.citations[i]
                self._save_citations()
                return True
        return False

    def format_citation(self, citation_id: str, style: str = "apa") -> str:
        """Format citation in specified style"""
        citation = self.get_citation(citation_id)
        if not citation:
            return ""

        # Default to APA if style is None
        if not style:
            style = "apa"

        if style.lower() == "apa":
            return self._format_apa(citation)
        elif style.lower() == "mla":
            return self._format_mla(citation)
        elif style.lower() == "chicago":
            return self._format_chicago(citation)
        else:
            return self._format_apa(citation)

    def _format_apa(self, citation: Dict[str, Any]) -> str:
        """Format citation in APA style"""
        authors = ", ".join(citation['authors']) if citation['authors'] else "Unknown"
        year = citation['year']
        title = citation['title']
        journal = citation['journal']
        volume = citation['volume']
        pages = citation['pages']

        formatted = f"{authors} ({year}). {title}."
        if journal:
            formatted += f" {journal}"
        if volume:
            formatted += f", {volume}"
        if pages:
            formatted += f", {pages}"

        return formatted

    def _format_mla(self, citation: Dict[str, Any]) -> str:
        """Format citation in MLA style"""
        authors = ", ".join(citation['authors']) if citation['authors'] else "Unknown"
        title = citation['title']
        journal = citation['journal']
        year = citation['year']

        return f"{authors}. \"{title}.\" {journal}, {year}."

    def _format_chicago(self, citation: Dict[str, Any]) -> str:
        """Format citation in Chicago style"""
        authors = ", ".join(citation['authors']) if citation['authors'] else "Unknown"
        title = citation['title']
        journal = citation['journal']
        year = citation['year']

        return f"{authors}. \"{title}.\" {journal} ({year})."

    def export_citations(self, format_type: str = "bibtex") -> str:
        """Export citations in specified format"""
        # Default to bibtex if format_type is None
        if not format_type:
            format_type = "bibtex"

        if format_type.lower() == "bibtex":
            return self._export_bibtex()
        elif format_type.lower() == "csv":
            return self._export_csv()
        else:
            return self._export_bibtex()

    def _export_bibtex(self) -> str:
        """Export citations as BibTeX"""
        if not self.citations:
            return ""

        bibtex_entries = []
        for citation in self.citations:
            authors = ", ".join(citation['authors']) if citation['authors'] else "Unknown"
            entry = f"""@article{{{citation['id']},
    title = {{{citation['title']}}},
    author = {{{authors}}},
    year = {{{citation['year']}}},
    journal = {{{citation['journal']}}},
    volume = {{{citation['volume']}}},
    pages = {{{citation['pages']}}},
    doi = {{{citation['doi']}}}
}}"""
            bibtex_entries.append(entry)

        return "\n\n".join(bibtex_entries)

    def _export_csv(self) -> str:
        """Export citations as CSV"""
        if not self.citations:
            return ""

        df = pd.DataFrame(self.citations)
        return df.to_csv(index=False)

    def _generate_citation_id(self) -> str:
        """Generate unique citation ID"""
        return f"cite_{uuid.uuid4().hex[:8]}"
