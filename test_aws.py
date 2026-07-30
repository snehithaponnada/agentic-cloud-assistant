from app.services.aws_service import list_s3_buckets

print("\n===== AWS CONNECTION TEST =====")

buckets = list_s3_buckets()

if buckets:
    print("S3 Buckets:")
    for bucket in buckets:
        print("-", bucket)
else:
    print("AWS connected successfully.")
    print("No S3 buckets found.")