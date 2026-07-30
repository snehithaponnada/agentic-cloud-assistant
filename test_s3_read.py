from app.tools.s3_tools import read_s3_object

result = read_s3_object.invoke({
    "bucket_name": "snehitha-agentic-cloud-demo-2026",
    "object_key": "application.log"
})

print(result)