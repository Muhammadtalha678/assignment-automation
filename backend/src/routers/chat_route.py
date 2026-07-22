from fastapi import APIRouter,Request
from src.models.pydantic_model import data
from src.controllers.chat_controller import chat_controller
router = APIRouter(prefix="/api")

@router.post("/chat")
async def chat(request:Request,chatData:data):
    agent_config = request.app.state.agent_config
    print(chatData)
    return await chat_controller(agent_config=agent_config,chat_data=chatData)

