import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent
from browser_use.llm import ChatAnthropic

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and claude",
        llm=ChatAnthropic(model="claude-sonnet-4-0", temperature=1.0),
    )
    await agent.run()

asyncio.run(main())