from typing_extensions import TypedDict
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from pathlib import Path

from backend.tools.arxiv import arxiv_search
from backend.tools.read import read_pdf
from backend.tools.write import render_latex_pdf
from backend.tools.comprehensive_paper import generate_comprehensive_paper

env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

gemini_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "write-your-model-here")
if not gemini_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

class State(TypedDict):
    messages: Annotated[list, add_messages]

tools = [arxiv_search, read_pdf, render_latex_pdf, generate_comprehensive_paper]
tool_node = ToolNode(tools)
model = ChatGoogleGenerativeAI(
    model=gemini_model,
    google_api_key=gemini_key,
    max_tokens=8000,
    temperature=0.3,
    top_p=0.8,
    top_k=40
).bind_tools(tools)

def call_model(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: State) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
