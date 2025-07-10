import streamlit as st
from typing import Dict
import uuid
from datetime import datetime


def _display_message(message: Dict):
    """Display a chat message"""
    if message['role'] == 'user':
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧑‍💼 You:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 Assistant:</strong><br>
            {message['content']}
        </div>
        """, unsafe_allow_html=True)

        if 'sources' in message:
            with st.expander("📚 Sources"):
                for source in message['sources']:
                    st.write(f"• **{source['title']}** (Distance: {source['distance']:.3f})")


def _save_conversation():
    """Save current conversation to history"""
    if len(st.session_state.current_conversation) >= 2:  # At least one exchange
        conversation_id = str(uuid.uuid4())
        title = st.session_state.current_conversation[0]['content'][:50]

        conversation = {
            'id': conversation_id,
            'title': title,
            'messages': st.session_state.current_conversation.copy(),
            'created_at': datetime.now().isoformat()
        }

        st.session_state.chat_history.append(conversation)
        if len(st.session_state.chat_history) > 50:
            st.session_state.chat_history.pop(0)


class ChatInterface:
    def __init__(self, llm_handler, vector_store):
        self.llm_handler = llm_handler
        self.vector_store = vector_store

        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_conversation' not in st.session_state:
            st.session_state.current_conversation = []

    def render(self):
        """Render the chat interface"""
        # Chat history sidebar
        with st.sidebar:
            st.subheader("💬 Chat History")
            if st.button("🆕 New Conversation"):
                st.session_state.current_conversation = []
                st.rerun()

            for i, chat in enumerate(st.session_state.chat_history[-10:]):
                if st.button(f"Chat {i + 1}: {chat['title'][:20]}...", key=f"chat_{i}"):
                    st.session_state.current_conversation = chat['messages']
                    st.rerun()

        st.subheader("🤖 Research Assistant Chat")

        chat_container = st.container()

        with chat_container:
            for message in st.session_state.current_conversation:
                _display_message(message)

        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])

            with col1:
                user_input = st.text_area(
                    "Ask your research question...",
                    placeholder="e.g., 'Summarize the key findings from my papers about machine learning' or 'What are the research gaps in my current work?'",
                    height=100,
                    key="user_input"
                )

            with col2:
                st.write("")  # Spacing
                use_rag = st.checkbox("Use RAG", value=True, help="Search your papers for relevant context")
                submit_button = st.form_submit_button("Send 🚀")

        if submit_button and user_input:
            self._process_user_input(user_input, use_rag)

    def _process_user_input(self, user_input: str, use_rag: bool):
        """Process user input and generate response"""
        user_message = {
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.current_conversation.append(user_message)

        with st.spinner("🤔 Thinking..."):
            context = ""
            sources = []

            if use_rag:
                # Search for relevant papers
                relevant_papers = self.vector_store.search_papers(user_input, n_results=3)

                if relevant_papers:
                    context = "\n\n".join([
                        f"Paper: {paper['metadata'].get('title', 'Unknown')}\n{paper['content'][:500]}..."
                        for paper in relevant_papers
                    ])

                    sources = [{
                        'title': paper['metadata'].get('title', paper['id']),
                        'distance': paper['distance']
                    } for paper in relevant_papers]

            response = self.llm_handler.generate_response(user_input, context)

            assistant_message = {
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat(),
                'sources': sources
            }
            st.session_state.current_conversation.append(assistant_message)

            _save_conversation()

            st.rerun()

