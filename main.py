from src.agents import QAAgent
from src.controllers import QAController
import asyncio

async def main():
    qa_controller = QAController(qa_agent=QAAgent())

    async for result in qa_controller.astream("Who are you?" \
    "Tell me what you know about your profession."):
        await asyncio.sleep(0.0001)
        print(result, end="", flush=True)
    


if __name__ == "__main__":
    asyncio.run(main())
