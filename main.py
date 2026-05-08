# main.py (excerpt)
from fastapi import FastAPI
from pydantic import BaseModel
from agent import app_agent
from langchain_core.messages import HumanMessage, SystemMessage

app = FastAPI(title="SoleAgent API")

class ChatRequest(BaseModel):
    message: str
    session_id: str
    customer_name: str # <--- NEW FIELD

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # Invisibly remind the agent of the user's name every time they chat
    context_msg = f"System Note: The customer you are speaking to is named {req.customer_name}."
    
    inputs = {"messages": [
        SystemMessage(content=context_msg),
        HumanMessage(content=req.message)
    ]}
    
    config = {"configurable": {"thread_id": req.session_id}}
    result = app_agent.invoke(inputs, config=config)
    
    ai_message = result["messages"][-1].content
    return {"response": ai_message}

