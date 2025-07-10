import os
from pathlib import Path
import toml

# Load config
config = toml.load(Path(__file__).parent.parent / "config.toml")

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / config["paths"]["data_dir"]
PAPERS_DIR = BASE_DIR / config["paths"]["papers_dir"]
CITATIONS_DIR = BASE_DIR / config["paths"]["citations_dir"]
DEADLINES_DIR = BASE_DIR / config["paths"]["deadlines_dir"]

for dir_path in [DATA_DIR, PAPERS_DIR, CITATIONS_DIR, DEADLINES_DIR]:
    dir_path.mkdir(exist_ok=True)

# LLM Configuration
OLLAMA_BASE_URL = config["llm"]["ollama_base_url"]
MODEL_NAME = config["llm"]["model_name"]

# ChromaDB Configuration
CHROMA_HOST = config["chroma"]["host"]
CHROMA_PORT = config["chroma"]["port"]
CHROMA_DB_PATH = str(BASE_DIR / config["chroma"]["db_path"])

# Application Settings
APP_TITLE = config["app"]["title"]
APP_DESCRIPTION = config["app"]["description"]
MAX_FILE_SIZE = config["app"]["max_file_size"]
SUPPORTED_FORMATS = config["app"]["supported_formats"]

# API Keys (set as environment variables)
ARXIV_API_KEY = os.getenv("ARXIV_API_KEY", "")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "")
