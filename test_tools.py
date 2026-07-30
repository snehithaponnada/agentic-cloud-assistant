from app.tools.log_analyzer import analyze_logs


sample_log = """
2026-07-30 14:32:10 ERROR
botocore.exceptions.ClientError:
An error occurred (AccessDenied) when calling
the GetObject operation on S3.
"""


result = analyze_logs.invoke(sample_log)

print(result)