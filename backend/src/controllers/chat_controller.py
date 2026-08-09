from j import f
import json
from agents import Runner,Agent,set_tracing_export_api_key
from src.controllers.docs_generator import generate_assignment_docx
from src.models.pydantic_model import data
from src.agents.content_agent import content_agent
from src.configs.env_config import OPENAI_API_KEY
from src.controllers.generate_image import generate_image, generate_image_via_advanced_web

async def chat_controller(chat_data:data,agent_config,):
    set_tracing_export_api_key(OPENAI_API_KEY)

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
        - Semester
        - Student Name
        - Registration ID
        - Questions
        - Language

        Registration ID Rules

        - Never modify Registration ID.
        - Never remove leading zeros.
            Example:
            0000844005
            must remain
            0000844005 
                   
        Never generate academic content.

        If anything is missing, ask the user.

        When everything is complete don't ask confirmation questions just handoff to the Content Agent.
        """,
        handoffs=[content_agent]
    )
    result = await Runner.run(
        input=json_data,
        starting_agent=orchistrator_agent,
        run_config=agent_config.config(),

    )
    agent_raw_output = result.final_output
    # agent_raw_output = f
    if (isinstance(agent_raw_output,str)):
        dict_content = json.loads(agent_raw_output)
    else:
        dict_content = agent_raw_output

    if hasattr(dict_content, "model_dump"):
        data = dict_content.model_dump()
    elif hasattr(dict_content, "dict"):
        data = dict_content.dict()
    else:
        data = dict_content

    # dict_content = dict_content.model_dump()
    output_filename = f"Assignment_{chat_data.assignment_no}_{chat_data.student_name}_{chat_data.course_code}.docx"

    image_map = await generate_image_via_advanced_web(data)
    # image_map = {
    #     1: r"D:\AIOU\assignment-automation\backend\diagrams\temp_1.png",
    #     2: r"D:\AIOU\assignment-automation\backend\diagrams\temp_2.png",
    #     3: r"D:\AIOU\assignment-automation\backend\diagrams\temp_3.png",
    #     4: r"D:\AIOU\assignment-automation\backend\diagrams\temp_4.png",
    #     5: r"D:\AIOU\assignment-automation\backend\diagrams\temp_5.png",
    #     }

    await generate_assignment_docx(
        json_data_str=data,
        image_map=image_map,
        output_path=output_filename,
        logo_path="assets/aiou_logo.jpg"
    )
    # questions = data.get("questions", [])
    # print(questions)
    return {
        "status": "success",
        "dict_content": data,
        # "file_name": output_filename,
        "message": "Assignment Word document generated successfully!"
    }

