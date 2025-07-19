# Academic Research Assistant - RAG-Based Paper Analysis Tool

**Open Source AI Research Assistant | Local LLM Processing | Zero API Costs**

Transform your research workflow with intelligent paper analysis, automated summarization, and conversational AI - all running locally on your machine.

## Screenshot

<img width="1920" height="1043" alt="Screenshot From 2025-07-10 10-48-15" src="https://github.com/user-attachments/assets/36b48ebb-9961-4435-9663-8437f6ef6c45" />


---

## What is Academic Research Assistant?

Academic Research Assistant is a **Retrieval-Augmented Generation (RAG) model** that revolutionizes how researchers interact with academic papers. Upload your research papers and instantly get AI-powered summaries, engage in natural conversations about the content, and extract insights - all without sending data to external APIs or paying for tokens.

## 🚀 Key Features

### RAG-Powered Paper Analysis
- **Upload & Analyze**: Drop PDF papers and get instant AI summaries
- **Conversational AI**: Chat naturally with your research papers using advanced RAG technology
- **Context-Aware Responses**: Get accurate answers grounded in your uploaded documents
- **Multi-Paper Queries**: Ask questions across multiple papers simultaneously

### Local AI Processing
- **No API Keys Required**: Run powerful open-source LLMs locally
- **Zero Token Costs**: Process unlimited papers without subscription fees  
- **Privacy First**: Your research stays on your machine - no data sent to external servers
- **Scalable Performance**: Use lightweight models on modest hardware or high-parameter models on powerful machines

### Intelligent Research Management
- **Smart Summarization**: Get concise, accurate summaries of complex research papers
- **Citation Generation**: Automatically generate properly formatted citations
- **Research Dashboard**: Visualize your paper analysis activity and insights
- **Deadline Tracking**: Never miss important research milestones

## 🏗️ How It Works (RAG Architecture)

1. **Document Ingestion**: Upload research papers (PDF/TXT)
2. **Text Extraction**: Automatically extract and chunk paper content
3. **Vector Embedding**: Convert text chunks into searchable vector embeddings
4. **Vector Storage**: Store embeddings in local ChromaDB for fast retrieval
5. **Query Processing**: When you ask questions, relevant chunks are retrieved
6. **Response Generation**: Local LLM generates answers using retrieved context

## 🛠️ Installation & Setup


### Quick Installation

```bash
# Clone repository
git clone https://github.com/imshaaz21/academic_assistant.git
cd academic_assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Ollama (Local LLM Runtime)
curl -fsSL https://ollama.ai/install.sh | sh

# Download AI model (choose based on your hardware)
ollama pull deepseek-r1:1.5b      # Lightweight (2GB RAM)
ollama pull llama3.1:8b           # Balanced (8GB RAM) 
ollama pull llama3.1:70b          # High-accuracy (64GB+ RAM)
```

### Docker Deployment
```bash
docker build -t academic_assistant .
docker run -p 8501:8501 -v $(pwd)/data:/app/data academic_assistant
```

## ⚙️ Configuration

Customize your RAG model in `config.toml`:

```toml
[llm]
model_name = "llama3.1:8b"        # Choose your model
temperature = 0.1                  # Lower = more factual
max_tokens = 4096                 # Response length limit

[rag]
chunk_size = 1000                 # Text chunk size for processing
chunk_overlap = 200               # Overlap between chunks
top_k = 5                         # Number of relevant chunks to retrieve

[vector_store]
embedding_model = "all-MiniLM-L6-v2"  # Sentence embedding model
similarity_threshold = 0.7             # Minimum similarity for retrieval
```

## 🚦 Getting Started

1. **Launch Services**
   ```bash
   ollama serve &                    # Start Ollama LLM server
   chroma run --path ./chroma_db &   # Start vector database
   streamlit run app.py              # Launch web interface
   ```

2. **Access Application**
   Open `http://localhost:8501` in your browser

3. **Upload Papers**
   - Drag & drop PDF research papers
   - Wait for automatic processing and indexing
   - Get instant AI-generated summaries

4. **Start Chatting**
   - Ask questions about your papers
   - Get contextual answers with source citations
   - Explore insights across multiple documents

## 💡 Example Use Cases

**Literature Review**: "Summarize the main findings about neural networks in computer vision across all uploaded papers"

**Methodology Comparison**: "Compare the experimental methods used in Smith et al. vs Johnson et al."

**Concept Exploration**: "Explain how transformer architecture is discussed in these papers"

**Citation Help**: "Generate APA citations for all papers mentioning 'deep learning'"

## 🏛️ Technical Architecture

```
RAG Pipeline Architecture:
📄 Papers → 🔄 Chunking → 🧮 Embeddings → 💾 ChromaDB → 🔍 Retrieval → 🤖 LLM → 💬 Response
```

### Core Components
- **Frontend**: Streamlit web interface
- **RAG Engine**: Custom retrieval-augmented generation pipeline  
- **Vector Store**: ChromaDB for semantic search
- **LLM Backend**: Ollama with swappable open-source models
- **Processing**: PyPDF2, LangChain for document handling

## 📊 Performance & Model Options

| Model | Size | RAM Needed | Speed | Accuracy | Best For |
|-------|------|------------|-------|----------|----------|
| DeepSeek-R1 1.5B | 2GB | 4GB | Fast | Good | Quick summaries |
| Llama 3.1 8B | 8GB | 16GB | Medium | Very Good | Balanced usage |
| Llama 3.1 70B | 70GB | 128GB | Slow | Excellent | Research-grade analysis |

## 🔒 Privacy & Security

- **Local Processing**: All data stays on your machine
- **No Cloud Dependencies**: Works completely offline
- **No API Keys**: Zero external service dependencies
- **Open Source**: Full transparency in code and models
- **GDPR Compliant**: No data collection or transmission

## 🌟 Why Choose Academic Research Assistant?

- ✅ **Cost Effective**: No subscription fees or API costs
- ✅ **Privacy First**: Your research data never leaves your computer  
- ✅ **Unlimited Usage**: Process as many papers as your hardware allows
- ✅ **Customizable**: Swap models and tune parameters for your needs
- ✅ **Open Source**: Transparent, modifiable, and community-driven
- ✅ **Academic Focus**: Built specifically for research workflows

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

## 🏷️ Keywords

`academic research` `RAG model` `local AI` `paper analysis` `research assistant` `LLM` `open source` `privacy-first` `offline AI` `literature review` `paper summarization` `conversational AI` `vector database` `semantic search`
