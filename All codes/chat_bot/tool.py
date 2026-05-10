from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Runner
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# ----- Groq configuration -----
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set. Please ensure it is defined in your .env file.")

# Groq's OpenAI-compatible endpoint
external_client = AsyncOpenAI(
    api_key=groq_api_key,
    base_url="https://api.groq.com/openai/v1"
)

# Choose a free Groq model (change if you prefer another)
# Options: "llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"
model = OpenAIChatCompletionsModel(
    model="llama-3.3-70b-versatile",   # <-- Groq model name
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# ----- Agent definition -----
agent = Agent(
    name='General Agent',
    instructions="You are a helpful assistant. Your task is to help the user with their queries."
)

# Run a synchronous query
result = Runner.run_sync(
    agent,
    "what is the weather of Islamabad",
    run_config=config
)

print(result.final_output)