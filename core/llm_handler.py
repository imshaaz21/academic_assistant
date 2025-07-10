import ollama
from datetime import datetime
from typing import Dict, List
from config.settings import OLLAMA_BASE_URL, MODEL_NAME
from utils.logger import get_logger


class LLMHandler:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.logger.info(f"Initializing LLMHandler with model: {MODEL_NAME}")
        self.client = ollama.Client(host=OLLAMA_BASE_URL)
        self.model_name = MODEL_NAME

    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using DeepSeek model"""
        self.logger.info(f"Generating response for prompt: {prompt[:50]}...")
        try:
            full_prompt = f"""
            Context: {context}

            User Query: {prompt}

            Please provide a comprehensive and accurate response based on the context provided.
            If you need to cite sources, use proper academic citation format.
            """

            self.logger.debug(f"Sending request to model: {self.model_name}")
            response = self.client.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': full_prompt
                }],
                stream=False
            )

            self.logger.info("Response generated successfully")
            return response['message']['content']
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}", exc_info=True)
            return f"Error generating response: {str(e)}"

    def summarize_paper(self, paper_content: str, title: str = "") -> Dict:
        """Generate paper summary with key insights"""
        self.logger.info(f"Summarizing paper: {title if title else 'Untitled'}")
        self.logger.debug(f"Paper content length: {len(paper_content)} characters")

        prompt = f"""
        Analyze the following research paper and provide:
        1. Main research question/hypothesis
        2. Key methodology used
        3. Primary findings/results
        4. Significance and implications
        5. Limitations mentioned
        6. Future research directions suggested

        Paper Title: {title}
        Content: {paper_content}

        Format your response as a structured summary.
        """

        summary = self.generate_response(prompt)

        result = {
            "title": title,
            "summary": summary,
            "generated_at": datetime.now().isoformat()
        }

        self.logger.info(f"Paper summary generated successfully for: {title if title else 'Untitled'}")
        return result

    def suggest_research_directions(self, topic: str, current_papers: List[str]) -> List[str]:
        """Suggest new research directions based on current work"""
        self.logger.info(f"Suggesting research directions for topic: {topic}")
        self.logger.debug(f"Using {len(current_papers)} papers as context")

        papers_context = "\n".join(current_papers)
        prompt = f"""
        Based on the following research topic and existing papers, suggest 5 potential research directions:

        Topic: {topic}
        Existing Papers Context: {papers_context}

        Provide specific, actionable research questions or directions.
        """

        response = self.generate_response(prompt)
        directions = response.split('\n')

        self.logger.info(f"Generated {len(directions)} research directions for topic: {topic}")
        self.logger.debug(f"Research directions: {directions}")

        return directions
