from src.agents import QAAgent
from src.configs import setup_logger
from logging import Logger
from langchain_core.messages import AIMessage
from typing import AsyncIterator
from dataclasses import dataclass

class QAController:
    """The quality routing controller"""

    qa_agent: QAAgent
    logger: Logger

    def __init__(self, qa_agent: QAAgent):
        self.qa_agent = qa_agent
        self.logger = setup_logger(logger_name=__name__, level='info')


    # Main Methods
    async def ainvoke(self, request: str) -> str | None:
        """
        Asynchrounosly invoke the quality assurance agent
        
        ### Args:
        - request (str): The user request

        ### Returns:
            the agent's final response
        """
        try:
            result = await self.qa_agent.ainvoke(request=request)
        except Exception as e:
            self.logger.error(f"Message streaming failed in the controller, message: {e}")
            return None
        return result[-1]


    async def astream(self, request: str) -> AsyncIterator[str]:
        """
        Stream the QA's agent run

        ### Args:
        - request (str): the user's request
        - thread_id (str): The thread's ID

        ### Returns:
            A stream of the agent's run
        """
        try:
                
            async for msg in self.qa_agent.astream(request=request):
                for ch in msg['agent']['messages'][0].content:
                    yield ch
        
        except Exception as e:
            self.logger.error(f"Message streaming failed in the controller, message: {e}")
            yield None
