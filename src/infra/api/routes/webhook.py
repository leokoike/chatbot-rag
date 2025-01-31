from http import HTTPStatus

from fastapi import APIRouter, Depends, Query, Request, Response
from pydantic import ValidationError
from src.domain.use_cases import QAUseCase
from src.infra.client.whatsapp_api import WhatsAppAPI
from src.infra.config import settings
from src.infra.container import get_qa_use_case, get_whatsapp_client
from src.infra.dtos.whatsapp import TextContent, WARequest

router = APIRouter()


@router.post("/webhook", status_code=HTTPStatus.OK)
async def qa(
    data: Request,
    whatsapp_client: WhatsAppAPI = Depends(get_whatsapp_client),
    qa_use_case: QAUseCase = Depends(get_qa_use_case),
):
    data = await data.json()
    print(f"{__file__}: Got Webhook request")
    print(f"{__file__}: {data}")

    try:
        data_obj = WARequest.model_validate(data)
        phone_number = data_obj.entry[0].changes[0].value.messages[0].from_
        answer = await qa_use_case.execute(
            data=data_obj.entry[0].changes[0].value.messages[0].text.body
        )
        response = await whatsapp_client.send_message(answer, phone_number)
        print(f"{__file__}: {response}")
    except ValidationError:
        pass


@router.get("/webhook", status_code=HTTPStatus.OK)
async def verify_token(
    hub_mode: str = Query(alias="hub.mode"),
    hub_challenge: str = Query(alias="hub.challenge"),
    verify_token: str = Query(alias="hub.verify_token"),
):
    print(f"{hub_mode} {hub_challenge} {verify_token}")
    if hub_mode and verify_token and hub_challenge:
        if hub_mode == "subscribe" and verify_token == settings.META_WEBHOOK_TOKEN:
            return Response(content=hub_challenge)
    return Response(status_code=HTTPStatus.FORBIDDEN)


@router.post("/answer", status_code=HTTPStatus.OK)
async def get_answer(
    data: TextContent,
    qa_use_case: QAUseCase = Depends(get_qa_use_case),
):
    answer = await qa_use_case.execute(data=data.body)

    return Response(content=answer)


@router.post("/{phone_number}/message", status_code=HTTPStatus.OK)
async def send_message(
    phone_number: str,
    data: TextContent,
    whatsapp_client: WhatsAppAPI = Depends(get_whatsapp_client),
):
    response = await whatsapp_client.send_message(data.body, phone_number)

    return response
