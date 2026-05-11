# playground.py
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

print("GOOGLE_API_KEY carregada:", bool(os.getenv("GOOGLE_API_KEY")))

from agno.playground import Playground, serve_playground_app
from agent.events_agent import create_agent

agent = create_agent()

app = Playground(agents=[agent]).get_app(use_async=True)

if __name__ == "__main__":
    serve_playground_app("playground:app", port=7778, reload=False)