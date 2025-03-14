import os
import requests
from typing import List, Optional, Any
from langchain.llms.base import LLM
from pydantic import Field

class GroqLangChainWrapper(LLM):
    """
    A custom LangChain LLM wrapper for interacting with the Groq API.
    """
    model_name: str = Field(default='groq', exclude=True)
    groq_client: Any = Field(default=None, exclude=True)
    model_name: str

    class Config:
        arbitrary_types_allowed = True

    @property
    def _llm_type(self) -> str:
        return 'groq'
    
    def _call(self, query: str, stop: Optional[List[str]] = None) -> str:
        """Calls the Groq API with a query."""
        try:
            response = self.groq_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant whom translate questions into SQL queries. The database contains geodata and you might need to use postGIS. Return only the query (so that the user may verify) and the result. Do not return the result if the query is invalid."},
                    {"role": "user", "content": query}
                ],                
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error calling Groq: {e}"