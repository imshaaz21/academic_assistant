import streamlit as st
from typing import List
import os
from config.settings import MAX_FILE_SIZE, SUPPORTED_FORMATS


def _generate_summary(paper_result: dict) -> dict | None:
    """Generate summary for processed paper"""
    try:
        from core.llm_handler import LLMHandler
        llm = LLMHandler()
        return llm.summarize_paper(paper_result['content'], paper_result['title'])
    except Exception as e:
        st.error(f"Failed to generate summary: {str(e)}")
        return None


def _extract_citations(paper_result: dict) -> List[dict]:
    """Extract citations from processed paper"""
    try:
        # Simple citation extraction (can be enhanced with NLP)
        content = paper_result['content']
        citations = []

        # Look for common citation patterns
        import re

        # Pattern for year citations like (Author, 2020)
        citation_patterns = [
            r'\([A-Z][a-zA-Z\s&,]+,\s*\d{4}\)',  # (Author, 2020)
            r'\[[A-Z][a-zA-Z\s&,]+,\s*\d{4}\]',  # [Author, 2020]
        ]

        for pattern in citation_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                citations.append({
                    'raw_text': match,
                    'extracted_from': paper_result['title']
                })

        return citations[:10]  # Limit to first 10 citations

    except Exception as e:
        st.error(f"Failed to extract citations: {str(e)}")
        return []


class PaperUpload:
    def __init__(self, paper_processor, vector_store):
        self.paper_processor = paper_processor
        self.vector_store = vector_store

    def render(self):
        """Render the paper upload interface"""
        st.subheader("📤 Upload Research Papers")

        # File uploader
        uploaded_files = st.file_uploader(
            "Choose research papers",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help=f"Supported formats: {', '.join(SUPPORTED_FORMATS)}. Max size: {MAX_FILE_SIZE // (1024 * 1024)}MB per file"
        )

        # Batch upload options
        col1, col2 = st.columns(2)

        with col1:
            auto_extract_citations = st.checkbox("Auto-extract citations", value=True)

        with col2:
            generate_summaries = st.checkbox("Generate summaries", value=True)

        # Upload progress
        if uploaded_files:
            st.subheader("📋 Upload Queue")

            # Display files to be processed
            for i, file in enumerate(uploaded_files):
                file_size = len(file.getvalue())
                file_size_mb = file_size / (1024 * 1024)

                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(f"📄 {file.name}")

                with col2:
                    st.write(f"{file_size_mb:.2f} MB")

                with col3:
                    if file_size > MAX_FILE_SIZE:
                        st.error("Too large")
                    else:
                        st.success("Ready")

            # Process files
            if st.button("🚀 Process All Files"):
                self._process_files(uploaded_files, auto_extract_citations, generate_summaries)

    def _process_files(self, files: List, auto_extract_citations: bool, generate_summaries: bool):
        """Process uploaded files"""
        progress_bar = st.progress(0)
        status_text = st.empty()

        processed_count = 0
        total_files = len(files)

        for i, file in enumerate(files):
            status_text.text(f"Processing {file.name}...")

            # Check file size
            if len(file.getvalue()) > MAX_FILE_SIZE:
                st.error(f"❌ {file.name}: File too large (max {MAX_FILE_SIZE // (1024 * 1024)}MB)")
                continue

            # Process file
            try:
                result = self.paper_processor.process_uploaded_file(file)

                if result['success']:
                    # Add to vector store
                    success = self.vector_store.add_paper(
                        result['id'],
                        result['content'],
                        result['metadata']
                    )

                    if success:
                        processed_count += 1
                        st.success(f"✅ {file.name}: Processed successfully")

                        # Add to session state
                        if 'uploaded_papers' not in st.session_state:
                            st.session_state.uploaded_papers = []

                        st.session_state.uploaded_papers.append({
                            'id': result['id'],
                            'title': result['title'],
                            'filename': file.name,
                            'processed_at': result['metadata']['processed_at']
                        })

                        # Generate summary if requested
                        if generate_summaries:
                            with st.spinner(f"Generating summary for {file.name}..."):
                                summary = _generate_summary(result)
                                if summary:
                                    st.info(f"📝 Summary generated for {file.name}")

                        # Extract citations if requested
                        if auto_extract_citations:
                            with st.spinner(f"Extracting citations from {file.name}..."):
                                citations = _extract_citations(result)
                                if citations:
                                    st.info(f"📚 {len(citations)} citations extracted from {file.name}")

                    else:
                        st.error(f"❌ {file.name}: Failed to add to vector store")

                else:
                    st.error(f"❌ {file.name}: {result['error']}")

            except Exception as e:
                st.error(f"❌ {file.name}: {str(e)}")

            # Update progress
            progress_bar.progress((i + 1) / total_files)

        # Final status
        status_text.text(f"✅ Processing complete! {processed_count}/{total_files} files processed successfully.")

        if processed_count > 0:
            st.balloons()
