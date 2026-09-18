from fastapi import APIRouter
from pydantic import BaseModel
from uuid import uuid4

from app.conversation.chat import BiodiversityChat


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    message: str
    location_id: str | None = None
    session_id: str | None = None


chat_sessions = {}


@router.post("/")
def chat(request: ChatRequest):

    # Create a new session if one was not provided
    if request.session_id is None:
        session_id = str(uuid4())
        chat_sessions[session_id] = BiodiversityChat()
    else:
        session_id = request.session_id

        # If the session does not exist, create it
        if session_id not in chat_sessions:
            chat_sessions[session_id] = BiodiversityChat()

    chatbot = chat_sessions[session_id]

    result = chatbot.process_message(
        message=request.message,
        location_id=request.location_id
    )

    result["session_id"] = session_id

    return result