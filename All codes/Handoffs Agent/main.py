from agents import Agent, Runner, handoff
import asyncio
from connection import config   # ← must be Groq version (see previous answer)

billing_agent = Agent(
    name="Billing Agent",
    instructions="You only answer questions related to billing."
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="You are responsible only for handling refund-related requests and guiding users through the refund process."
)

custon_refund_handoff = handoff(
    agent=refund_agent,
    tool_name_override="custom_refund_tool",
    tool_description_override="Handle user refund requests with extra care."
)

demage_refund_handoff = handoff(
    agent=refund_agent,
    tool_name_override="demage_refund_tool",
    tool_description_override="Handle refund due to damaged item."
)

late_delivery_refund_handoff = handoff(
    agent=refund_agent,
    tool_name_override="late_delivery_refund_tool",
    tool_description_override="Handle refund due to late delivery."
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="Read the user's request and decide which agent is best suited to handle it.",
    handoffs=[billing_agent, custon_refund_handoff, demage_refund_handoff, late_delivery_refund_handoff]
)

async def main():
    result = await Runner.run(
        triage_agent,
        "My order arrived 10 days late. I want a refund.",   # ✅ added comma here
        run_config=config
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())