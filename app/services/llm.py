import os
from openai import OpenAI
from typing import List

class LLMService:
    def __init__(self):
        # Initialize the official OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_answer(self, question: str, contexts: List[str]) -> str:
        """Sends the structured context and user question to OpenAI."""
        if not contexts:
            return "I cannot find any relevant documents in my knowledge base to answer this question."

        # Merge the text chunks into one clean string block
        context_block = "\n\n---\n\n".join(contexts)
        
        # Strict instructions directing the AI to never make things up
        system_prompt = (
            "You are a helpful, factual assistant. You are given context blocks from an internal database.\n"
            "You must answer the user's question using ONLY the facts provided in the context blocks.\n"
            "If the answer cannot be found in the context blocks, say exactly: 'I don't know based on the provided data.'\n\n"
            f"CONTEXT BLOCKS:\n{context_block}"
        )

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Highly cost-efficient, lightning fast model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.0  # Forces the model to remain rigid, factual, and repeatable
        )
        
        return response.choices[0].message.content

# Create a singleton instance
llm_service = LLMService()