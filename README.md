# Gemini-Code-Intepreter
Googles Gemini Model with the ability to execute code using a code intepreter using function calling
# AI Code Interpreter Project

This project leverages IPython, Vertex AI, and a generative model to interpret and execute Python code within a secure environment. The setup uses environment variables to manage sensitive information securely.

## Features

- **IPython Integration**: Use IPython to manage and execute notebook cells.
- **Vertex AI Initialization**: Seamlessly integrate with Vertex AI to use generative models.
- **Secure Execution**: Execute AI-generated code in a sandboxed environment.
- **Environment Variables**: Manage sensitive data using environment variables.

## Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-code-interpreter.git
cd ai-code-interpreter
```

2. Install Required Packages

``` bash
pip install -r requirements.txt
```

## Environment Variables

create a .env file in the root of this projects directory

```makefile
PROJECT_ID=*********
LOCATION=***********
E2B_API_KEY=***********************
```
## Run the application

```bash
python3 intepreter.py
```

## Usage
Once the application is running, you can enter your prompts to interact with the AI code interpreter.
File Structure

interpreter.py: Main script that sets up and runs the AI code interpreter.
.env: Environment variables for sensitive data (not included in the repository).

Contributing
Contributions are welcome! Please create a pull request or open an issue to discuss any changes or improvements.
License
This project is licensed under the MIT License. 
