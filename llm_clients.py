import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pathlib import Path
from system.tools import tools

env_path = Path(__file__).parent / "API_KEY.env"

load_dotenv(env_path)
API_KEY = os.getenv("API_KEY")

llm_int = ChatGroq(
    api_key=API_KEY,
    model='qwen/qwen3-32b',
    reasoning_format="hidden",
    #model='openai/gpt-oss-120b',
    temperature=0.5
).bind_tools(tools)

llm_obs = ChatGroq(
    api_key=API_KEY,
    model='qwen/qwen3-32b',
    #model='openai/gpt-oss-120b',
    #model='openai/gpt-oss-20b',
    reasoning_format="hidden",
    temperature=0.5
)