from app.services.llm import get_llm
from app.tools.log_analyzer import analyze_logs


def get_agent_llm():

    llm = get_llm()

    tools = [analyze_logs]

    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools