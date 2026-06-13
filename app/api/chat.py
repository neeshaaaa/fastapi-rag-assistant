from fastapi import APIRouter, Depends
from pydantic import BaseModel
from uuid import uuid4

from app.services.rag import search_similar_chunks
from app.services.llm import generate_answer
from app.services.memory import save_message, get_history

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import ChatRequest
from app.db.models import Booking

router = APIRouter()

@router.post("/query")
def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):

    # 1. session id
    session_id = req.session_id or str(uuid4())

    # 2. save user message
    try:
        save_message(session_id, "user", req.question)
    except Exception as e:
        print(f"Redis memory error: {e}")

    # 3. retrieve similar chunks
    chunks = search_similar_chunks(req.question)

    context = "\n\n".join(chunks)

    # 4. get chat history (optional memory)
    history = []
    try:
        history = get_history(session_id)
    except Exception as e:
        print(f"Redis memory error: {e}")

    # Exclude the current question we just pushed if we want a cleaner prompt, 
    # but for now we just use the history as is.
    history_text = "\n".join(
        [f"{m['role']}: {m['message']}" for m in history]
    )

    # 5. build final prompt
    full_context = f"""
Chat History:
{history_text}

Document Context:
{context}
"""

    # 6. generate answer
    try:
        answer = generate_answer(full_context, req.question, db)
    except Exception as e:
        answer = f"Sorry, I encountered an error with the AI provider: {str(e)}"

    # 7. save assistant response
    try:
        save_message(session_id, "assistant", answer)
    except Exception as e:
        pass

    return {
        "session_id": session_id,
        "answer": answer,
        "sources": chunks
    }