# Academic Research Assistant

AI-powered research companion for paper analysis and citation management.

## Overview

Academic Research Assistant is a Streamlit-based application designed to help researchers manage their academic papers, citations, and research deadlines. It leverages AI capabilities through local language models to provide intelligent paper summarization, research chat, and citation management.

## Features

- **Research Dashboard**: View metrics and visualizations of your research activity
- **AI-Powered Chat**: Interact with your research papers using natural language
- **Paper Management**: 
  - Upload and store research papers
  - Automatically extract and index content
  - Generate AI summaries of papers
- **Citation Management**: Create, organize, and export citations in academic formats
- **Deadline Tracker**: Keep track of important research deadlines
- **Settings Management**: Configure application settings and export data

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) for local LLM support
- [ChromaDB](https://www.trychroma.com/) for vector storage

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/academic_assistant.git
   cd academic_assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install streamlit streamlit-option-menu plotly pandas chromadb ollama
   ```

4. Install Ollama and download the required model:
   ```bash
   # Follow instructions at https://ollama.ai/ to install Ollama
   ollama pull deepseek-r1:1.5b
   ```

5. Start ChromaDB server:
   ```bash
   # Install ChromaDB server following instructions at https://docs.trychroma.com/
   chroma run --path data/chroma_db
   ```

## Configuration

The application is configured through the `config.toml` file:

```toml
[paths]
data_dir = "data"
papers_dir = "data/papers"
citations_dir = "data/citations"
deadlines_dir = "data/deadlines"

[llm]
ollama_base_url = "http://localhost:11434"
model_name = "deepseek-r1:1.5b"

[chroma]
host = "localhost"
port = 8000
db_path = "data/chroma_db"

[app]
title = "Academic Research Assistant"
description = "AI-powered research companion for paper analysis and citation management"
max_file_size = 10485760
supported_formats = [".pdf", ".txt"]
```

## Usage

1. Start the Ollama service:
   ```bash
   ollama serve
   ```

2. Start the ChromaDB server:
   ```bash
   chroma run --path data/chroma_db
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

4. Open your browser and navigate to `http://localhost:8501`

## Project Structure

- `app.py`: Main application file
- `components/`: UI components
  - `chat_interface.py`: Research chat interface
  - `paper_upload.py`: Paper upload component
  - `deadline_tracker.py`: Deadline tracking component
  - `citation_display.py`: Citation management component
- `core/`: Core functionality
  - `llm_handler.py`: Language model integration
  - `vector_store.py`: Vector database integration
  - `paper_processor.py`: Paper processing logic
  - `citation_manager.py`: Citation management logic
- `config/`: Configuration files
  - `settings.py`: Application settings
- `static/`: Static assets
  - `css/`: CSS stylesheets
- `utils/`: Utility functions
- `data/`: Data storage (created at runtime)

## Dependencies

- `streamlit`: Web application framework
- `streamlit-option-menu`: Navigation menu component
- `plotly`: Interactive visualizations
- `pandas`: Data manipulation
- `chromadb`: Vector database for semantic search
- `ollama`: Local LLM integration

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.