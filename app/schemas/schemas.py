from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    session_id: str | None = None

class BookingCreate(BaseModel):
    name: str
    email: str
    date: str
    time: str
