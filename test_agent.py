from app.agent.agent import get_agent_llm


agent = get_agent_llm()


user_message = """
My application cannot access an S3 object.

Here are the logs:

2026-07-30 ERROR
botocore.exceptions.ClientError:
An error occurred (AccessDenied)
when calling the GetObject operation.
"""


response = agent.invoke(user_message)


print("CONTENT:")
print(response.content)

print("\nTOOL CALLS:")
print(response.tool_calls)