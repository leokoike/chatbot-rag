from src.domain.llm import LLM
from src.domain.use_cases.base import BaseUseCase


class QAUseCase(BaseUseCase):
    def __init__(self, llm: LLM):
        self.llm = llm

    async def execute(self, data: str) -> str:
        print("Init inference")
        answer = await self.llm.invoke(query=data)

        print(f"Question: {data}\nAnswer: {answer}\n")
        return answer
