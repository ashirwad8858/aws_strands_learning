from strands import Agent
from strands_tools import file_read, file_write
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



system_prompt = """
    You are helpful to personal assistence capable of performing local file anction and simple task
    You Key Capability:
    1. Read, understand and summerize the file
    2. Create and writ files.
    3. List directory contents and provide information on the file
    4. Summerize the text context.

    You can use the ollowing tools to perform these action
    - file_read: Read the file and return the content
    - file_write: Write to a file
"""


agent = Agent(
    model = model,
    system_prompt = system_prompt,
    tools = [file_read, file_write]
    )
message = "What is the content of the file in agentic_ai_overview.txt file and summerize it less than 100 words in result.md file"

agent(message)