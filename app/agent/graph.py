from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from app.services.llm import get_llm

from app.tools.log_analyzer import analyze_logs
from app.tools.knowledge_tool import search_cloud_knowledge
from app.tools.aws_tool import (
    inspect_s3_buckets,
    inspect_s3_objects
)
from app.tools.s3_tools import read_s3_object

tools = [analyze_logs,search_cloud_knowledge,inspect_s3_buckets,inspect_s3_objects,read_s3_object]

llm = get_llm()
llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are an Agentic AI Cloud Support Assistant specializing in AWS.

You have access to tools that help you diagnose cloud problems.

Available capabilities:

1. analyze_logs
   Use this when the user provides application logs, error logs,
   stack traces, or cloud service errors that need analysis.

2. search_cloud_knowledge
   Use this when you need AWS troubleshooting knowledge about
   services such as S3, Lambda, IAM, or CloudWatch.

3. inspect_s3_buckets
   Use this when the user asks about the actual S3 buckets
   or cloud storage resources available in their AWS account.

4. inspect_s3_objects
   Use this when the user asks what files or objects exist
   inside a specific Amazon S3 bucket.

Choose tools based on the user's request.

You may use more than one tool when necessary.

After gathering enough information:
1. Identify the likely root cause.
2. Explain the problem clearly.
3. Recommend practical troubleshooting steps.

Do not call tools unnecessarily.
"""


def assistant_node(state: MessagesState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


builder = StateGraph(MessagesState)

builder.add_node(
    "assistant",
    assistant_node
)

builder.add_node(
    "tools",
    ToolNode(tools)
)


builder.add_edge(
    START,
    "assistant"
)


builder.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools": "tools",
        END: END
    }
)


builder.add_edge(
    "tools",
    "assistant"
)


agent_graph = builder.compile()