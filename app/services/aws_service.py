import boto3

def get_s3_client():
    session = boto3.Session()
    return session.client("s3")


def list_s3_buckets():
    s3 = get_s3_client()
    response = s3.list_buckets()

    return [
        bucket["Name"]
        for bucket in response.get("Buckets", [])
    ]

def list_s3_objects(bucket_name: str):
    s3 = get_s3_client()
    response = s3.list_objects_v2(
        Bucket=bucket_name
    )

    objects = response.get("Contents", [])

    return [
        {
            "key": obj["Key"],
            "size": obj["Size"],
            "last_modified": str(obj["LastModified"])
        }
        for obj in objects
    ]