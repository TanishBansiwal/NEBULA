from pydantic import BaseModel


class SearchRequest(BaseModel):
    conversation_id: int
    query: str