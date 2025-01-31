from abc import ABC, abstractmethod

class LLM(ABC):

    @abstractmethod
    async def invoke(self, query: str) -> str:
        pass

