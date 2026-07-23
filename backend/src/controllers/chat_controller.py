from agents import Runner,Agent,set_tracing_export_api_key
from src.controllers.docs_generator import generate_assignment_docx
from src.models.pydantic_model import data
from src.agents.content_agent import content_agent
from src.configs.env_config import OPENAI_API_KEY
async def chat_controller(chat_data:data,agent_config,):
    # set_tracing_export_api_key(OPENAI_API_KEY)

    # json_data = chat_data.model_dump_json()
    # orchistrator_agent = Agent(
    #     name="orchistrator agent",
    #     instructions="""
    #     You are an Assignment Orchestrator.

    #     You never write assignment answers.

    #     Your responsibilities are:

    #     1. Understand the user's request.
    #     2. Collect all missing information.
    #     3. Validate the information.
    #     4. Create a structured request.
    #     5. Handoff the request to the Content Agent.

    #     Collect:

    #     - Assignment Number
    #     - Course Code
    #     - Course Title
    #     - Student Name
    #     - Registration ID
    #     - Questions
    #     - Language

    #     Never generate academic content.

    #     If anything is missing, ask the user.

    #     When everything is complete, handoff to the Content Agent.
    #     """,
    #     handoffs=[content_agent]
    # )
    # result = await Runner.run(
    #     input=json_data,
    #     starting_agent=orchistrator_agent,
    #     run_config=agent_config.config(),

    # )
    # agent_raw_output = result.final_output
    # agent_raw_output = result.final_output
    import json
    agent_raw_output = "{\n  \"assignment\": {\n    \"assignment_no\": 1,\n    \"course_code\": 301,\n    \"course_title\": \"GIAIC\",\n    \"student_name\": \"Talha\",\n    \"registration_id\": 123456,\n    \"questions\": [\n      {\n        \"question_number\": 1,\n        \"question_text\": \"What is javascript\",\n        \"introduction\": \"JavaScript is a dynamic programming language widely used in web development. It is primarily known for adding interactive elements to websites, enabling features that enhance user experience. Developed in the early 1990s, JavaScript has evolved significantly over the years and is now a fundamental technology alongside HTML and CSS in creating modern web applications.\",\n        \"sections\": [\n          {\n            \"heading\": \"History of JavaScript\",\n            \"detailed_explanation\": \"JavaScript was created by Brendan Eich while working at Netscape Communications. Initially developed in a mere ten days, it was designed to enable client-side scripting in web browsers. Since its inception in 1995, JavaScript has undergone numerous changes, leading to the establishment of ECMAScript as its standardized version.\"\n          },\n          {\n            \"heading\": \"Core Features\",\n            \"detailed_explanation\": \"JavaScript is characterized by its capabilities such as event-driven programming, first-class functions, and prototype-based object orientation. These features allow developers to build complex applications that can respond to user inputs in real-time.\"\n          },\n          {\n            \"heading\": \"Client-side vs Server-side\",\n            \"detailed_explanation\": \"Initially, JavaScript was restricted to client-side scripting, executing commands in the user's browser. However, with the advent of Node.js, JavaScript has expanded to include server-side programming, allowing complete web applications to be built using just one language on both the client and server.\"\n          },\n          {\n            \"heading\": \"JavaScript Frameworks and Libraries\",\n            \"detailed_explanation\": \"Numerous frameworks and libraries such as React, Angular, and Vue.js have been developed to streamline JavaScript development. These tools provide pre-written code to optimize projects, facilitate easier coding practices, enhance functionalities, and improve overall development efficiency.\"\n          },\n          {\n            \"heading\": \"Asynchronous Programming\",\n            \"detailed_explanation\": \"JavaScript supports asynchronous programming through callbacks, promises, and async/await syntax. This feature allows developers to write code that executes without blocking other operations, significantly improving application performance, especially in handling I/O tasks.\"\n          },\n          {\n            \"heading\": \"ES6 and Modern JavaScript\",\n            \"detailed_explanation\": \"ECMAScript 2015 or ES6 introduced many important features like let and const declarations, arrow functions, template literals, destructuring, and more. These improvements render JavaScript more powerful and maintainable, making it a favorite among developers.\"\n          },\n          {\n            \"heading\": \"JavaScript in Web Development\",\n            \"detailed_explanation\": \"JavaScript integrates seamlessly with HTML and CSS, forming the backbone of web development. It supports various APIs that facilitate interaction with the hardware and services, enabling features like geolocation, web storage, and more.\"\n          }\n        ],\n        \"diagram_description\": \"A flow diagram illustrating the JavaScript execution model would show the event loop, which handles asynchronous processes, highlighting how JavaScript executes code in a non-blocking manner while managing callbacks and promises, enhancing the understanding of its event-driven nature.\",\n        \"conclusion\": \"In conclusion, JavaScript is an essential language in the digital world, providing interactive capabilities to websites and facilitating versatile application development. Its evolution, particularly with ES6 and the introduction of frameworks, has solidified its place in modern programming, enabling developers to create rich, functional, and responsive applications.\"\n      }\n    ]\n  }\n}" 
    if (isinstance(agent_raw_output,str)):
        dict_content = json.loads(agent_raw_output)
    else:
        dict_content = agent_raw_output

    output_filename = f"Assignment_{chat_data.assignment_no}_{chat_data.student_name}.docx"

    generate_assignment_docx(
        json_data_str=dict_content,
        output_path=output_filename,
        logo_path="assets/aiou_logo.jpg"
    )

    return {
        "status": "success",
        "file_name": output_filename,
        "message": "Assignment Word document generated successfully!"
    }