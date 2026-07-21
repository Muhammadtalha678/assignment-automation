from fastapi import FastAPI
from src.routers.chat_route import router as ChatRouter
from src.configs.agent_config import AgentConfig
from src.configs import env_config 
from contextlib import asynccontextmanager
@asynccontextmanager
def lifespan(app:FastAPI):
    config_agent = AgentConfig(
        api_key= env_config.api_key,
        base_url=env_config.base_url,
        model_name=env_config.model_name
    )

    app.state.agent_config = config_agent

    yield

    print("Apllication closed successfully")


app = FastAPI()

app.include_router(ChatRouter)