from typing import Dict, Any, Optional, Callable, TypeVar

from paddle.exceptions import PaddleAPIError

T = TypeVar("T")


def handle_status_code(
    status_code: int,
    success_handler: Callable[[Dict[str, Any]], T],
    error_handler: Optional[Callable[[PaddleAPIError], T]] = None,
) -> T:
    """
    Utility function to handle different status codes.

    Args:
        status_code: The HTTP status code
        success_handler: Function to call if status code is successful (2xx)
        error_handler: Optional function to call for specific error status codes

    Returns:
        The result of the appropriate handler function

    Raises:
        PaddleAPIError: If no error handler is provided for a non-successful status code
    """
    if 200 <= status_code < 300:
        return success_handler({})

    if error_handler:
        return error_handler(PaddleAPIError(status_code, "API Error"))

    raise PaddleAPIError(status_code, "API Error")


def is_retryable_status_code(status_code: int) -> bool:
    """
    Check if a status code is retryable.

    Args:
        status_code: The HTTP status code

    Returns:
        True if the status code is retryable, False otherwise
    """
    # 5xx errors are server errors that might be temporary
    if 500 <= status_code < 600:
        return True

    # 429 is rate limit exceeded, might be retryable after waiting
    if status_code == 429:
        return True

    # 408 is request timeout, might be retryable
    if status_code == 408:
        return True

    return False


def get_retry_delay(status_code: int, retry_after_header: Optional[str] = None) -> float:
    """
    Get the recommended delay before retrying a request.

    Args:
        status_code: The HTTP status code
        retry_after_header: The value of the Retry-After header if present

    Returns:
        The recommended delay in seconds
    """
    if retry_after_header:
        try:
            return float(retry_after_header)
        except ValueError:
            pass

    # Default retry delays based on status code
    if status_code == 429:  # Rate limit
        return 5.0
    elif 500 <= status_code < 600:  # Server error
        return 1.0
    elif status_code == 408:  # Request timeout
        return 0.5

    return 1.0
