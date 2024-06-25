import IPython
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


# Access environment variables
PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION')
E2B_API_KEY = os.getenv('E2B_API_KEY')

app = IPython.Application.instance()

import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION)

import requests
from IPython.display import display, Markdown
from vertexai.generative_models import (
    FunctionDeclaration,
    GenerativeModel,
    GenerationConfig,
    Part,
    Tool,
)

execute_python = FunctionDeclaration(
    name="execute_python",
    description="Execute python code in a Jupyter notebook cell and returns any result, stdout, stderr, display_data, and error",
    parameters={
        "type": "object",
        "properties": {
            "code": {
                "type": "string",
                "description": "The python code to execute in a single cell",
            }
        },
    },
)

execution_tool = Tool(
    function_declarations=[
       execute_python
    ],
)

from e2b_code_interpreter import CodeInterpreter

with CodeInterpreter(api_key=E2B_API_KEY) as code_interpreter:
    def code_interpret(code_interpreter: code_interpreter, code: str):
        print(f"\n{'='*50}\n> Running following AI-generated code:\n{code}\n{'='*50}")
        exec_result = code_interpreter.notebook.exec_cell(
            code,
            on_stderr=lambda stderr: print("\n[Code Interpreter stderr]", stderr),
            on_stdout=lambda stdout: print("\n[Code Interpreter stdout]", stdout),
        )

        if exec_result.error:
            print("[Code Interpreter error]", exec_result.error)  # Runtime error
            return exec_result.error
        else:
            print(exec_result.results)
            return exec_result.results, exec_result.logs

function_handler = {
    "execute_python": code_interpret,
}

model = GenerativeModel(
    "gemini-1.0-pro",
    generation_config=GenerationConfig(temperature=0),
    tools=[execution_tool],
)
chat = model.start_chat(response_validation=False)

def send_chat_message(prompt):
    display(Markdown("#### Prompt"))
    print(prompt, "\n")
    combined_prompt = """
    If you're asked to execute code or visualize by the user, use the tool you have. It's a secure sandbox where you can execute code. Make sure you start by installing the required packages for whatever task you are assigned. After you execute the code, tell the user whatever the tool returns. Preamble results with the text 'here's the result'. The user's request starts here:
    """ + prompt

    response = chat.send_message(combined_prompt)
    display(Markdown("#### Sent chat successfully"))

    function_calling_in_process = True
    while function_calling_in_process:
        function_call = response.candidates[0].content.parts[0].function_call

        if function_call.name in function_handler.keys():
            function_name = function_call.name
            display(Markdown("#### Predicted function name"))
            print(function_name, "\n")

            params = {key: value for key, value in function_call.args.items()}
            display(Markdown("#### Predicted function parameters"))
            print(params, "\n")

            function_api_response = function_handler[function_name](params)[:20000]
            display(Markdown("#### API response"))
            print(function_api_response[:500], "...", "\n")

            response = chat.send_message(
                Part.from_function_response(
                    name=function_name,
                    response={"content": function_api_response},
                ),
            )
        else:
            function_calling_in_process = False

    display(Markdown("#### Natural language response"))
    print(response.text)

user_prompt = input('Enter your Prompt to the AI \n ')
send_chat_message(user_prompt)
