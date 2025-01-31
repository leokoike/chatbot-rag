from pydantic import BaseModel, ConfigDict, Field


class TextContent(BaseModel):
    body: str


class Message(BaseModel):
    from_: str = Field(alias="from")
    id: str
    timestamp: str
    text: TextContent
    type: str


class ContentValueWA(BaseModel):
    messaging_product: str
    metadata: dict
    contacts: list[dict]
    messages: list[Message]

    model_config = ConfigDict(extra="allow")


class ChangeWA(BaseModel):
    value: ContentValueWA
    field: str


class EntryDataWA(BaseModel):
    id: str
    changes: list[ChangeWA]


class WARequest(BaseModel):
    object: str
    entry: list[EntryDataWA]
