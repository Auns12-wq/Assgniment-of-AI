# handoffs.py
import asyncio
from agents import Agent, Runner
from connection import config

# Single agent that handles both billing and refunds
unified_agent = Agent(
    name="CustomerSupportAgent",
    instructions="""You are a customer support assistant. 
    - If the user asks about billing, payments, invoices, or charges, answer helpfully.
    - If the user asks about refunds (late delivery, damaged item, etc.), guide them through the refund process: ask for order number, reason, and then explain the steps.
    - Be polite and professional.
    """
)

async def main():
    user_input = "My order arrived 10 days late. I want a refund."
    result = await Runner.run(unified_agent, user_input, run_config=config)
    print("\n=== Response ===\n")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())