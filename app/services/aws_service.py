import boto3

session = boto3.Session()

s3 = session.client("s3")


def list_s3_buckets():
    response = s3.list_buckets()

    return [
        bucket["Name"]
        for bucket in response.get("Buckets", [])
    ]

def list_s3_objects(bucket_name: str):
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