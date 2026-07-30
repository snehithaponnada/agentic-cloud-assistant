from langchain_core.tools import tool


@tool
def analyze_logs(log_text: str) -> str:
    """
    Analyze application logs and identify common cloud-related errors.
    """

    log_lower = log_text.lower()

    if "accessdenied" in log_lower or "access denied" in log_lower:
        return (
            "IAM_PERMISSION_ERROR: Access was denied. "
            "The application may not have sufficient IAM permissions."
        )

    if "nosuchbucket" in log_lower or "bucket does not exist" in log_lower:
        return (
            "S3_BUCKET_ERROR: The requested S3 bucket could not be found."
        )

    if "timeout" in log_lower or "timed out" in log_lower:
        return (
            "TIMEOUT_ERROR: The application encountered a timeout. "
            "Check network connectivity, service availability, "
            "or execution timeout configuration."
        )

    if "connection refused" in log_lower:
        return (
            "CONNECTION_ERROR: The application could not connect "
            "to the requested service."
        )

    return (
        "UNKNOWN_ERROR: No known cloud error pattern was detected. "
        "Further investigation is required."
    )