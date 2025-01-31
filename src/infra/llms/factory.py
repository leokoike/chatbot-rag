from src.domain.llm import LLM
from .handlers import BasicChatOllama


class LLMFactory:
    @staticmethod
    def get_llm(name: str) -> LLM:
        match name:
            case "ollama":
                return BasicChatOllama()
            case _:
                pass
