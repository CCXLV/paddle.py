class PaddleAPIError(Exception):
    """Exception raised for errors in the Paddle API."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Paddle API Error: {status_code} - {message}")


class PaddleAuthenticationError(PaddleAPIError):
    """Exception raised for authentication errors (401)."""

    def __init__(self, message: str):
        super().__init__(401, message)


class PaddlePermissionError(PaddleAPIError):
    """Exception raised for permission errors (403)."""

    def __init__(self, message: str):
        super().__init__(403, message)


class PaddleNotFoundError(PaddleAPIError):
    """Exception raised for not found errors (404)."""

    def __init__(self, message: str):
        super().__init__(404, message)


class PaddleValidationError(PaddleAPIError):
    """Exception raised for validation errors (400)."""

    def __init__(self, message: str):
        super().__init__(400, message)


class PaddleRateLimitError(PaddleAPIError):
    """Exception raised for rate limit errors (429)."""

    def __init__(self, message: str):
        super().__init__(429, message)


class PaddleServerError(PaddleAPIError):
    """Exception raised for server errors (5xx)."""

    def __init__(self, status_code: int, message: str):
        super().__init__(status_code, message)


class PaddleConflictError(PaddleAPIError):
    """Exception raised for conflict errors (409)."""

    def __init__(self, message: str):
        super().__init__(409, message)


def create_paddle_error(status_code: int, message: str) -> PaddleAPIError:
    """Factory function to create the appropriate Paddle error based on status code."""
    if status_code == 401:
        return PaddleAuthenticationError(message)
    elif status_code == 403:
        return PaddlePermissionError(message)
    elif status_code == 404:
        return None
    elif status_code == 400:
        return PaddleValidationError(message)
    elif status_code == 429:
        return PaddleRateLimitError(message)
    elif 500 <= status_code < 600:
        return PaddleServerError(status_code, message)
    else:
        return PaddleAPIError(status_code, message)
