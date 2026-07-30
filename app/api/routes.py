from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from app.agent.graph import agent_graph


router = APIRouter()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat_with_agent(request: ChatRequest):

    try:
        result = agent_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=request.message)
                ]
            }
        )

        final_message = result["messages"][-1]

        # Handle Gemini/LangChain content safely
        content = final_message.content

        if isinstance(content, str):
            response_text = content

        elif isinstance(content, list):
            response_text = ""

            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    response_text += item.get("text", "")

        else:
            response_text = str(content)

        return ChatResponse(
            response=response_text
        )

    except Exception as error:
        print(f"Agent API Error: {error}")

        raise HTTPException(
            status_code=500,
            detail="The cloud assistant encountered an error."
        )