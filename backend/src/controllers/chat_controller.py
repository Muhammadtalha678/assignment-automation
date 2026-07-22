from agents import Runner,Agent
from src.models.pydantic_model import data
from src.agents.content_agent import content_agent

async def chat_controller(chat_data:data,agent_config,):
    json_data = chat_data.model_dump_json()
    orchistrator_agent = Agent(
        name="orchistrator agent",
        instructions="""
        You are an Assignment Orchestrator.

        You never write assignment answers.

        Your responsibilities are:

        1. Understand the user's request.
        2. Collect all missing information.
        3. Validate the information.
        4. Create a structured request.
        5. Handoff the request to the Content Agent.

        Collect:

        - Assignment Number
        - Course Code
        - Course Title
        - Student Name
        - Registration ID
        - Questions
        - Language

        Never generate academic content.

        If anything is missing, ask the user.

        When everything is complete, handoff to the Content Agent.
        """,
        handoffs=[content_agent]
    )
    result = await Runner.run(
        input=json_data,
        starting_agent=orchistrator_agent,
        run_config=agent_config.config()
    )
    print(result.final_output)
    return {"message":"success"}