from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.chat_route import router as ChatRouter
from src.configs.agent_config import AgentConfig
from src.configs import env_config 
from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app:FastAPI):
    config_agent = AgentConfig(
        api_key= env_config.api_key,
        base_url=env_config.base_url,
        model_name=env_config.model_name
    )

    app.state.agent_config = config_agent

    yield

    print("Apllication closed successfully")


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allows all origins for development testing
    allow_origins=["https://assignment-automation-rose.vercel.app"],  # Allows all origins for development testing
    allow_credentials=True,
    # allow_methods=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
    allow_headers=["*"],
)
app.include_router(ChatRouter)
