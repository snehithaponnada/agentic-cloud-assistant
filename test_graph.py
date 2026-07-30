from langchain_core.messages import HumanMessage

from app.agent.graph import agent_graph


user_question = """
Inspect my AWS S3 environment.

Find my application log file and read its contents.

If you find an error:
1. Analyze the error.
2. Search the cloud troubleshooting knowledge base for relevant information.
3. Identify the likely root cause.
4. Recommend how I should fix it.

Do not assume the error beforehand. Inspect the AWS environment
and determine the problem yourself.
"""


result = agent_graph.invoke(
    {
        "messages": [
            HumanMessage(content=user_question)
        ]
    }
)


print("\n===== AGENT WORKFLOW =====\n")

for message in result["messages"]:

    print(type(message).__name__)

    if message.content:
        print(message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print("Tool Calls:", message.tool_calls)

    print("-" * 50)