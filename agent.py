# agent.py
import os
from typing import Annotated, TypedDict
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import MemorySaver # 1. NEW IMPORT
from tools import tools

class State(TypedDict):
    messages: Annotated[list, add_messages]

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

llm = ChatOllama(model="llama3.1:8b", temperature=0, base_url=OLLAMA_BASE_URL)
llm_with_tools = llm.bind_tools(tools)

# --- NEW SYSTEM PROMPT ---
# agent.py (excerpt)
# agent.py (excerpt)
SYSTEM_PROMPT = SystemMessage(content="""You are SoleAgent, an AI assistant for a shoe store. 
Your ONLY job is to help customers check stock, list models, and place orders using the SQL database.

CRITICAL DIRECTIVES - YOU MUST OBEY THESE:
1. NEVER GUESS INVENTORY. You are strictly forbidden from telling a user an item is in stock or out of stock without successfully calling the `check_stock` tool first.
2. NEVER FAKE ORDERS. You are strictly forbidden from saying an order is placed unless you have successfully called the `place_order` tool and received a success message back from it.
3. NO MONEY, NO REFUNDS. We do not handle payments, credit cards, cash, or refunds. Never ask the user how they want to pay.
4. NO THINKING OUT LOUD. Do not narrate your actions. Never say "Let me call the tool" or "I am checking the database." Just silently use the tool and return the result.
5. USE THE RIGHT TOOL. If the user asks "List all brands" or "What models do you have", you MUST use the `list_available_models` tool.
6. REQUIRE QUANTITY FOR ORDERS. If the user wants to buy something, ensure you know the model, size, and QUANTITY before calling `place_order`.

Respond to the user in a friendly, concise manner based ONLY on the data the tools return.""")

def chatbot(state: State):
    # Prepend the system prompt to the messages so the LLM always remembers its rules
    messages_with_system = [SYSTEM_PROMPT] + state["messages"]
    response = llm_with_tools.invoke(messages_with_system)
    return {"messages": [response]}

# Build the Graph
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

# 2. ADD MEMORY TO THE COMPILED GRAPH
memory = MemorySaver()
app_agent = graph_builder.compile(checkpointer=memory)