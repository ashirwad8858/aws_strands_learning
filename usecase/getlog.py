from strands import Agent
from strands_tools import file_read, file_write, speak, cron
from strands.models.openai import OpenAIModel
from strands import tool
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os



load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO", "ashirwadsharma12795+1@gmail.com)

@tool
def mail_send(subject: str, body: str, to_email: str = EMAIL_TO) -> str:
    """
    Sends an email with the given subject and body to the specified email address.

    If 'to_email' is not provided, it defaults to the one in the .env file.
    """

    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, [to_email], msg.as_string())

        return f"Email sent successfully to {to_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

model = OpenAIModel(
    client_args={
        "api_key": OPENAI_API_KEY
    },
    # **model_config
    model_id="gpt-4o",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)



system_prompt = """
    You are LogMon, an autonomous and vigilant monitoring agent.

Your role is to continuously watch system log files in real time. You must detect and immediately react to any critical entries — especially lines containing **"Error: 400"** and **"Error: 500"** . Upon encountering such an error, you must:
1. Quickly display a clear and concise report of the error, including the surrounding log context if available.
2. Optionally, trigger an email alert with the relevant log snippet, a timestamp, and a summary of the issue.

You are a high-reliability assistant for monitoring, diagnostics, and alerting. You do not miss important logs, and you never delay your response. You do not ignore even a single instance of `Error: 400` or `Error: 500`.

Your style is focused, brief, and informative — ideal for engineers in production environments. Avoid unnecessary explanations unless asked.

You are equipped with tools such as:
- `file_read`: to read and monitor log files.
-  `cron`: to schedule periodic checks every 5 second till 2 min.
- `file_write`: if any error found with 400 nad 500 then write in resul.md file.
- `mail_send`(sub, body): to send email notifications when any eroor found with 500 and 400 SUbject is Error and body should be all the line for that generated error.

Maintain professional tone, prioritize system health, and escalate critical issues immediately.

"""


agent = Agent(
    model = model,
    system_prompt = system_prompt,
    tools = [file_read, file_write,speak, cron, mail_send]
    )
# message = "What is the content of the file in agentic_ai_overview.txt file and summerize it less than 100 words in result.md file and last speak out the summary you have created to user, Make sure the vioce "

# agent(message)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit"]:
        break

    resopnce = agent(user_input)
    print("Agent: ",resopnce)
