from fastapi import APIRouter,Request,Depends,BackgroundTasks
from src.models.pydantic_model import data as ChatDataModal
from src.controllers.chat_controller import chat_controller
from src.lib.upload_image_dependency_funct import upload_images_and_get_chat_data
router = APIRouter(prefix="/api")

@router.post("/chat")
async def chat(request:Request,backgroundTask:BackgroundTasks,chatData:ChatDataModal = Depends(upload_images_and_get_chat_data)):
    agent_config = request.app.state.agent_config
    print(chatData)
    return await chat_controller(agent_config=agent_config,chat_data=chatData, backgroundTask=backgroundTask)

