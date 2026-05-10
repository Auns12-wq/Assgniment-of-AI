import os
import asyncio
import chainlit as cl
from dotenv import load_dotenv
from typing import cast
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel

load_dotenv(override=True)

# ----- Groq configuration -----
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set. Please add it to your .env file.")

# Available Groq models (free tier):
# - "llama-3.3-70b-versatile" (smartest)
# - "llama-3.1-8b-instant" (fastest)
# - "mixtral-8x7b-32768" (good balance)
MODEL_NAME = "llama-3.3-70b-versatile"   # you can change to any free Groq model

@cl.on_chat_start
async def start():
    # Groq uses OpenAI-compatible API
    external_client = AsyncOpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    model_instance = OpenAIChatCompletionsModel(
        model=MODEL_NAME,
        openai_client=external_client
    )

    agent = Agent(
        name="SMIU_Assistant",
        instructions="You are a helpful AI assistant.",
        model=model_instance
    )

    cl.user_session.set("agent", agent)
    cl.user_session.set("chat_history", [])

    await cl.Message(
        content="Welcome to the SMIU AI Assistant! (Powered by Groq)"
    ).send()


async def run_agent_with_retry(agent, history, max_retries=3):
    """Run agent with exponential backoff for Groq's rate limits (30 req/min)."""
    for attempt in range(max_retries):
        try:
            result = await Runner.run(starting_agent=agent, input=history)
            return result
        except Exception as e:
            error_str = str(e)
            # Groq returns 429 when rate limited
            if "429" in error_str or "rate limit" in error_str.lower():
                wait_time = 2 ** attempt  # 1, 2, 4 seconds
                print(f"Groq rate limit hit. Retrying in {wait_time}s (attempt {attempt+1}/{max_retries})")
                await asyncio.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded. Groq free tier limit reached. Please wait ~2 minutes and try again.")


@cl.on_message
async def main(message: cl.Message):
    thinking_msg = cl.Message(content="Thinking...")
    await thinking_msg.send()

    agent = cast(Agent, cl.user_session.get("agent"))
    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        result = await run_agent_with_retry(agent, history)
        response = result.final_output

        thinking_msg.content = response
        await thinking_msg.update()

        cl.user_session.set("chat_history", result.to_input_list())
        print(f"User: {message.content}\nAssistant: {response}")

    except Exception as e:
        error_msg = f"❌ Error: {str(e)}"
        if "429" in error_msg or "rate limit" in error_msg.lower():
            error_msg = "⚠️ Groq free tier rate limit exceeded. Please wait 1-2 minutes and try again."
        thinking_msg.content = error_msg
        await thinking_msg.update()
        print(f"Error details: {str(e)}")