from strands import Agent
from strands_tools import calculator, current_time
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={
        "api_key": "",
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)

agent = Agent(
    model = model,
    tools = [calculator,current_time]
    )

message = "I am born in 1995, tell me my age"

agent(message)