from strands import Agent
from strands_tools import http_request, python_repl
from strands.models.openai import OpenAIModel
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4.1")

if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not set in environment.")
  
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

my_agent = Agent(
    model=model,
    tools = [http_request, python_repl]
)
# response = my_agent("Give me the name of CEO of Bebo Technology Chandigarh.")

# print(response)
my_agent("Figure out where the ISS is relative to portlan, Oregon")