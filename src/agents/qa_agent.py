from langchain_litellm import ChatLiteLLM
from src import settings
from langfuse import observe
from langchain_core.messages import AIMessage, SystemMessage, AnyMessage
from src.configs import setup_logger
from logging import Logger
from .prompts import QAPrompts
from typing import List, Literal, AsyncIterator, Dict, Any
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.state import CompiledStateGraph
from .tools import play_a_game, make_pancakes
from langgraph.checkpoint.memory import MemorySaver

class QAAgent:
    """A quality assurance agent with writing tools to create excel sheets, and web search tools"""
    logger: Logger

    llm: ChatLiteLLM
    graph: CompiledStateGraph[MessagesState, None, MessagesState, MessagesState]
    messages: List[AnyMessage]

    def __init__(self):
        self.logger = setup_logger(logger_name = __name__)

        self.llm = ChatLiteLLM(
            model=settings.QA_MODEL,
            api_key=settings.OPENROUTER_API_KEY,
            temperature=settings.QA_TEMPERATURE
        )

        self.llm = self.llm.bind_tools([play_a_game, make_pancakes])

        self.graph = self._build_graph()

        self.logger.info("Quaity assurance agent initialized successfully")

    def _build_graph(self) -> CompiledStateGraph[MessagesState, None, MessagesState, MessagesState]:
        workflow = StateGraph(MessagesState)

        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", ToolNode([play_a_game, make_pancakes]))

        workflow.add_edge(START, "agent")
        workflow.add_conditional_edges(
            "agent",
            tools_condition,
        )
        workflow.add_edge("tools", "agent")
        workflow.add_edge("agent", END)
        
        memory = MemorySaver()

        graph = workflow.compile(checkpointer=memory)

        return graph

    # Graph Nodes
    @observe(name="LLM Call", capture_input=True, capture_output=True, as_type='generation')
    async def _call_model(self, state: MessagesState) -> MessagesState:

        if not any(isinstance(msg, SystemMessage) for msg in state["messages"]):
            system_message = QAPrompts.get_system_prompt()
            state['messages'].insert(0, system_message)

        response = await self.llm.ainvoke(input=state['messages'])
        return {'messages': [response]}

    def _should_continue(self, state: MessagesState) -> Literal["END", "tools"]:
        
        last_message = state['messages'][-1]

        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        else:
            return "END"

    @observe(name="QA Agent", capture_input=True, capture_output=True, as_type='agent')
    async def ainvoke(self, request: str, thread_id: str = "default") -> List[AnyMessage] | None:
        """
        Invoke a request asynchronously to the QA agent requesting a quality assurance testing sheet

        ### Args:
        - request (str): The request
        - thread_id (str): The thread ID for the conversation

        ### Returns:
            A tool call or an answer to the user's request
        """

        try:
            config = {
                "configurable": {
                    "thread_id": thread_id
                }
            }

            result = await self.graph.ainvoke(
                input= {"messages": request},
                config=config,
            )

        except Exception as e:
            self.logger.error(f"Graph invokation failed, message: {e}")
            return {"messages": []}

        self.logger.info("Quality assurance agent invoked successfully")
        return result

    @observe(name="QA Agent", capture_input=True, capture_output=True, as_type='agent')
    async def astream(self, request: str, thread_id: str ="default") -> AsyncIterator[Dict[str, Any]] | None:
        """
        Stream the QA's agent run

        ### Args:
        - request (str): the user's request
        - thread_id (str): The thread's ID

        ### Returns:
            A stream of the agent's run
        """

        try:
            config = {
                "configurable":{
                    "thread_id":thread_id
                }
            }

            async for result in self.graph.astream(input={"messages": request},config=config):
                yield result

        except Exception as e:
            self.logger.error(f"Graph streaming failed, message: {e}")
            yield None
        
        self.logger.info("Quality assurance agent run streamed successfully")
