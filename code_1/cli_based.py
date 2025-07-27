import os
from dotenv import load_dotenv
from strands import Agent
from strands_tools import http_request, python_repl
from strands.models.openai import OpenAIModel

# Load environment variables from .env file
load_dotenv()

# Read API key and model ID from environment
api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4.1")

if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not set in environment or .env file.")

# Set up the model
model = OpenAIModel(
    client_args={
        "api_key": api_key,
    },
    model_id=model_id,
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

# Create agent
my_agent = Agent(
    model=model,
    tools=[http_request, python_repl]
)

# Prompt user input from CLI
print("🧠 Strands CLI Agent. Type your question below (type 'exit' to quit):\n")

while True:
    prompt = input(">>> ")
    if prompt.lower() in ["exit", "quit"]:
        print("👋 Exiting.")
        break

    try:
        response = my_agent(prompt)
        print("\n🗨️ Response:\n", response, "\n")
    except Exception as e:
        print("❌ Error:", e)
