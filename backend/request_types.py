from typing import List
from pydantic import BaseModel


class ChatMessage(BaseModel):
  type: str
  text: str

class ChatRequest(BaseModel):
    opportunity_id: int
    messages: List[ChatMessage]