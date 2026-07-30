import boto3
from langchain_core.tools import tool
from botocore.exceptions import ClientError


@tool
def read_s3_object(bucket_name: str, object_key: str) -> str:
    """
    Read the text content of an object stored in an AWS S3 bucket.

    Use this tool when you need to inspect the actual contents of
    a file such as an application log or configuration file.
    """

    try:
        s3 = boto3.client("s3")

        response = s3.get_object(
            Bucket=bucket_name,
            Key=object_key
        )

        content = response["Body"].read().decode("utf-8")

        return (
            f"Contents of s3://{bucket_name}/{object_key}:\n\n"
            f"{content}"
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]

        return (
            f"AWS S3 error while reading '{object_key}' "
            f"from bucket '{bucket_name}'.\n"
            f"Error code: {error_code}\n"
            f"Message: {error_message}"
        )

    except Exception as e:
        return f"Unexpected error while reading S3 object: {str(e)}"