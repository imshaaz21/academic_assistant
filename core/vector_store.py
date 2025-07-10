import chromadb
from chromadb.config import Settings
from chromadb.errors import NotFoundError
from typing import List, Dict
from config.settings import CHROMA_HOST, CHROMA_PORT
from utils.logger import get_logger


class VectorStore:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info(f"Initializing VectorStore with Chroma at {CHROMA_HOST}:{CHROMA_PORT}")
        self.client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
            settings=Settings(allow_reset=True)
        )
        self.collection_name = "research_papers"
        self.collection = self._get_or_create_collection()

    def _get_or_create_collection(self):
        """Get or create the research papers collection"""
        self.logger.info(f"Getting or creating collection: {self.collection_name}")
        try:
            return self.client.get_collection(self.collection_name)
        except Exception as e:
            if isinstance(e, NotFoundError) or "not found" in str(e).lower() or "does not exist" in str(e).lower() or "does not exists" in str(e).lower():
                self.logger.info(f"Collection {self.collection_name} not found, creating new collection")
                return self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Academic research papers collection"}
                )
            else:
                self.logger.error(f"Unexpected error getting collection: {str(e)}", exc_info=True)
                raise

    def add_paper(self, paper_id: str, content: str, metadata: Dict) -> bool:
        """Add a paper to the vector store"""
        self.logger.info(f"Adding paper with ID: {paper_id}")
        try:
            self.collection.add(
                documents=[content],
                ids=[paper_id],
                metadatas=[metadata]
            )
            self.logger.info(f"Successfully added paper: {paper_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding paper: {str(e)}", exc_info=True)
            return False

    def search_papers(self, query: str, n_results: int = 5) -> List[Dict]:
        """Search for relevant papers based on query"""
        self.logger.info(f"Searching papers with query: {query[:50]}... (n_results={n_results})")
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            papers = []
            for i, doc in enumerate(results['documents'][0]):
                papers.append({
                    'id': results['ids'][0][i],
                    'content': doc,
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })

            self.logger.info(f"Found {len(papers)} relevant papers")
            return papers
        except Exception as e:
            self.logger.error(f"Error searching papers: {str(e)}", exc_info=True)
            return []

    def get_all_papers(self) -> List[Dict]:
        """Get all papers in the collection"""
        self.logger.info("Getting all papers from collection")
        try:
            results = self.collection.get()
            papers = []
            for i, doc in enumerate(results['documents']):
                papers.append({
                    'id': results['ids'][i],
                    'content': doc,
                    'metadata': results['metadatas'][i]
                })
            self.logger.info(f"Retrieved {len(papers)} papers from collection")
            return papers
        except Exception as e:
            self.logger.error(f"Error getting papers: {str(e)}", exc_info=True)
            return []

    def delete_paper(self, paper_id: str) -> bool:
        """Delete a paper from the collection"""
        self.logger.info(f"Deleting paper with ID: {paper_id}")
        try:
            self.collection.delete(ids=[paper_id])
            self.logger.info(f"Successfully deleted paper: {paper_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting paper: {str(e)}", exc_info=True)
            return False
