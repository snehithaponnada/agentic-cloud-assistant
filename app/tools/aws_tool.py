from langchain_core.tools import tool

from app.services.aws_service import (
    list_s3_buckets,
    list_s3_objects
)

@tool
def inspect_s3_buckets() -> str:
    """
    Inspect the user's AWS account and list available Amazon S3 buckets.
    Use this tool when the user asks about their actual S3 environment,
    buckets, or cloud storage resources.
    """

    try:
        buckets = list_s3_buckets()

        if not buckets:
            return (
                "AWS connection successful. "
                "No S3 buckets currently exist in the AWS account."
            )

        return (
            "S3 buckets found:\n"
            + "\n".join(f"- {bucket}" for bucket in buckets)
        )

    except Exception as error:
        return f"Unable to inspect S3: {str(error)}"


@tool
def inspect_s3_objects(bucket_name: str) -> str:
    """
    Inspect the objects stored inside a specific Amazon S3 bucket.

    Use this tool when the user asks what files or objects exist
    inside an S3 bucket.
    """

    try:
        objects = list_s3_objects(bucket_name)

        if not objects:
            return f"The S3 bucket '{bucket_name}' is empty."

        result = [
            f"Objects found in bucket '{bucket_name}':"
        ]

        for obj in objects:
            result.append(
                f"- {obj['key']} | "
                f"Size: {obj['size']} bytes | "
                f"Last Modified: {obj['last_modified']}"
            )

        return "\n".join(result)

    except Exception as error:
        return f"Unable to inspect S3 bucket: {str(error)}"