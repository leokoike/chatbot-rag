from fastapi import Depends
from src.domain.llm import LLM
from src.domain.use_cases import QAUseCase
from src.infra.client.whatsapp_api import WhatsAppAPI
from src.infra.llms.factory import LLMFactory
from src.infra.config import settings

__all__ = ["get_qa_use_case", "get_whatsapp_client"]


async def get_llm() -> LLM:
    return LLMFactory.get_llm("ollama")


async def get_qa_use_case(llm: LLM = Depends(get_llm)) -> QAUseCase:
    return QAUseCase(llm=llm)


async def get_whatsapp_client() -> WhatsAppAPI:
    return WhatsAppAPI(
        base_url="https://graph.facebook.com/",
        headers={
            "Authorization": f"Bearer {settings.META_ACCESS_TOKEN}",
        },
    )
