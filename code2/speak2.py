import os
from strands import Agent
from strands_tools import file_read, file_write, speak
from strands.models.openai import OpenAIModel
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("OPENAI_MODEL_ID", "gpt-4o")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not set")

model = OpenAIModel(
    client_args={"api_key": api_key},
    model_id=model_id,
    params={"max_tokens": 1000, "temperature": 0.7}
)

agent = Agent(
    model=model,
    system_prompt="""
You are a file‑handling agent:
- Read a file
- Summarize it
- Write the summary to a new file
- Then speak the summary aloud using Polly
""",
    tools=[file_read, file_write, speak]
)

def process(file_path: str, summary_path: str = "result.md"):
    content = agent.tool.file_read(path=file_path)
    summary_prompt = (f"Summarize the following file content in under 100 words:\n\n{content}")
    summary = str(agent(summary_prompt))

    agent.tool.file_write(path=summary_path, content=summary)
    print(f"✅ Summary saved to {summary_path}\n")
    agent.tool.speak(text=summary, style="neutral", mode="polly")
    print("🔉 Spoken via Amazon Polly")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python app.py ./home/ashirwad/Desktop/AI/AWS_Strands/code2/inputdata.txt")
        sys.exit(1)
    process(sys.argv[1])
