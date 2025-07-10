import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import json

# Import our custom modules
from core.llm_handler import LLMHandler
from core.vector_store import VectorStore
from core.paper_processor import PaperProcessor
from core.citation_manager import CitationManager
from components.chat_interface import ChatInterface
from components.paper_upload import PaperUpload
from components.deadline_tracker import DeadlineTracker
from components.citation_display import CitationDisplay
from config.settings import APP_TITLE, APP_DESCRIPTION

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load external CSS
with open('static/css/style.css', 'r') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)


class ResearchAssistantApp:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.vector_store = VectorStore()
        self.paper_processor = PaperProcessor()
        self.citation_manager = CitationManager()
        self.chat_interface = ChatInterface(self.llm_handler, self.vector_store)
        self.paper_upload = PaperUpload(self.paper_processor, self.vector_store)
        self.deadline_tracker = DeadlineTracker()
        self.citation_display = CitationDisplay(self.citation_manager)

        self._initialize_session_state()

    def _initialize_session_state(self):
        """Initialize session state variables"""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'uploaded_papers' not in st.session_state:
            st.session_state.uploaded_papers = []
        if 'deadlines' not in st.session_state:
            st.session_state.deadlines = []

    def render_header(self):
        """Render the main header"""
        st.markdown(f"""
        <div class="main-header">
            <h1>🔬 {APP_TITLE}</h1>
            <p>{APP_DESCRIPTION}</p>
        </div>
        """, unsafe_allow_html=True)

    def render_dashboard(self):
        """Render the main dashboard"""
        st.header("📊 Research Dashboard")

        # Metrics row
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            papers_count = len(self.vector_store.get_all_papers())
            st.metric("📄 Papers", papers_count)

        with col2:
            citations_count = len(self.citation_manager.get_all_citations())
            st.metric("📝 Citations", citations_count)

        with col3:
            deadlines_count = len(st.session_state.deadlines)
            st.metric("⏰ Deadlines", deadlines_count)

        with col4:
            chat_count = len(st.session_state.chat_history)
            st.metric("💬 Conversations", chat_count)

        # Recent activity
        st.subheader("📈 Recent Activity")

        # Create sample data for visualization
        activity_data = {
            'Date': [datetime.now() - timedelta(days=i) for i in range(7)],
            'Papers Added': [2, 1, 3, 0, 2, 1, 1],
            'Citations Created': [1, 2, 1, 1, 0, 2, 1],
            'Queries Made': [5, 3, 7, 2, 4, 6, 3]
        }

        df = pd.DataFrame(activity_data)

        fig = px.line(df, x='Date', y=['Papers Added', 'Citations Created', 'Queries Made'],
                      title="Weekly Research Activity")
        st.plotly_chart(fig, use_container_width=True)

    def render_chat(self):
        """Render the chat interface"""
        st.header("💬 Research Chat")
        self.chat_interface.render()

    def render_papers(self):
        """Render the papers management interface"""
        st.header("📄 Paper Management")

        tab1, tab2 = st.tabs(["Upload Papers", "Manage Papers"])

        with tab1:
            self.paper_upload.render()

        with tab2:
            self._render_paper_management()

    def _render_paper_management(self):
        """Render paper management interface"""
        papers = self.vector_store.get_all_papers()

        if not papers:
            st.info("No papers uploaded yet. Use the 'Upload Papers' tab to add papers.")
            return

        st.subheader("📚 Your Research Papers")

        for paper in papers:
            with st.expander(f"📄 {paper['metadata'].get('title', paper['id'])}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**ID:** {paper['id']}")
                    st.write(f"**Word Count:** {paper['metadata'].get('word_count', 'N/A')}")
                    st.write(f"**Processed:** {paper['metadata'].get('processed_at', 'N/A')}")

                    # Show first 200 characters of content
                    content_preview = paper['content'][:200] + "..." if len(paper['content']) > 200 else paper[
                        'content']
                    st.text_area("Preview", content_preview, height=100, disabled=True)

                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{paper['id']}"):
                        if self.vector_store.delete_paper(paper['id']):
                            st.success("Paper deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to delete paper")

                    if st.button(f"📝 Summarize", key=f"summarize_{paper['id']}"):
                        with st.spinner("Generating summary..."):
                            summary = self.llm_handler.summarize_paper(
                                paper['content'],
                                paper['metadata'].get('title', '')
                            )
                            st.write("**Summary:**")
                            st.write(summary['summary'])

    def render_citations(self):
        """Render the citations management interface"""
        st.header("📝 Citation Management")
        self.citation_display.render()

    def render_deadlines(self):
        """Render the deadline tracker interface"""
        st.header("⏰ Deadline Tracker")
        self.deadline_tracker.render()

    def render_settings(self):
        """Render the settings interface"""
        st.header("⚙️ Settings")

        st.subheader("🤖 Model Configuration")

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Model Name", value="deepseek-r1:1.5b", disabled=True)
            st.text_input("Ollama URL", value="http://localhost:11434", disabled=True)

        with col2:
            st.text_input("ChromaDB Host", value="localhost", disabled=True)
            st.text_input("ChromaDB Port", value="8000", disabled=True)

        st.subheader("🔧 Application Settings")

        # Theme settings
        theme = st.selectbox("Theme", ["Light", "Dark"], index=0)

        # Export settings
        st.subheader("📤 Export Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Export Citations"):
                citations_bibtex = self.citation_manager.export_citations("bibtex")
                st.download_button(
                    "Download BibTeX",
                    citations_bibtex,
                    "citations.bib",
                    "text/plain"
                )

        with col2:
            if st.button("Export Chat History"):
                chat_json = json.dumps(st.session_state.chat_history, indent=2)
                st.download_button(
                    "Download Chat History",
                    chat_json,
                    "chat_history.json",
                    "application/json"
                )

        with col3:
            if st.button("Export Papers List"):
                papers = self.vector_store.get_all_papers()
                papers_df = pd.DataFrame([{
                    'id': p['id'],
                    'title': p['metadata'].get('title', ''),
                    'word_count': p['metadata'].get('word_count', 0),
                    'processed_at': p['metadata'].get('processed_at', '')
                } for p in papers])

                st.download_button(
                    "Download CSV",
                    papers_df.to_csv(index=False),
                    "papers.csv",
                    "text/csv"
                )

    def run(self):
        """Main application runner"""
        self.render_header()

        # Sidebar navigation
        with st.sidebar:
            st.image("https://placehold.co/150x50/667eea/white?text=Research+AI", width=150)

            selected = option_menu(
                menu_title="Navigation",
                options=["Dashboard", "Chat", "Papers", "Citations", "Deadlines", "Settings"],
                icons=["speedometer2", "chat-dots", "file-earmark-text", "quote", "calendar-check", "gear"],
                menu_icon="cast",
                default_index=0,
                styles={
                    "container": {"background-color": "#1a1a1a", "padding": "10px"},
                    "icon": {"color": "#667eea", "font-size": "18px"},
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "--hover-color": "#d3d3d3"},
                    "nav-link-selected": {"background-color": "#667eea", "color": "white"},
                }
            )

            # Status indicators
            st.markdown("---")
            st.markdown("**🔧 System Status**")

            # Check Ollama connection
            try:
                self.llm_handler.client.list()
                st.success("🤖 Ollama: Connected")
            except:
                st.error("🤖 Ollama: Disconnected")

            # Check ChromaDB connection
            try:
                self.vector_store.client.heartbeat()
                st.success("🗄️ ChromaDB: Connected")
            except:
                st.error("🗄️ ChromaDB: Disconnected")

        # Main content area
        if selected == "Dashboard":
            self.render_dashboard()
        elif selected == "Chat":
            self.render_chat()
        elif selected == "Papers":
            self.render_papers()
        elif selected == "Citations":
            self.render_citations()
        elif selected == "Deadlines":
            self.render_deadlines()
        elif selected == "Settings":
            self.render_settings()


# Run the application
if __name__ == "__main__":
    app = ResearchAssistantApp()
    app.run()
