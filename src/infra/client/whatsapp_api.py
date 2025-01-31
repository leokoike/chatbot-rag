from aiohttp import ClientSession

from src.infra.config import settings


class WhatsAppAPI:
    def __init__(self, base_url: str, headers: dict):
        self.client = ClientSession(base_url=base_url, headers=headers)

    def __create_message_payload(self, message: str, phone_number: str) -> dict:
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {"body": message},
        }

    async def send_message(self, message: str, phone_number: str) -> dict:
        body = self.__create_message_payload(message, phone_number)
        data = None
        async with self.client as session:
            response = await session.post(
                url=f"v21.0/{settings.META_ID_NUMBER}/messages/",
                json=body,
            )
            async with response:
                print(f"{__file__}: Status code: {response.status}")
                # assert response.status == 200

                data = await response.json()

        return data
