import pytest

from paddle.utils import handle_status_code, is_retryable_status_code, get_retry_delay
from paddle.exceptions import PaddleAPIError


def test_handle_status_code():
    """Test handle_status_code function."""
    # Test successful status code
    assert handle_status_code(200, lambda x: x, None) == {}

    # Test with error handler
    error = handle_status_code(400, None, lambda x: x)
    assert isinstance(error, PaddleAPIError)
    assert error.status_code == 400
    assert error.message == "API Error"

    # Test without error handler - should raise exception
    with pytest.raises(PaddleAPIError) as exc_info:
        handle_status_code(400, None, None)
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "API Error"


def test_is_retryable_status_code():
    """Test is_retryable_status_code function."""
    assert is_retryable_status_code(429)
    assert not is_retryable_status_code(200)
    assert not is_retryable_status_code(400)
    assert is_retryable_status_code(500)
    assert is_retryable_status_code(502)
    assert is_retryable_status_code(503)
    assert is_retryable_status_code(504)
    assert is_retryable_status_code(408)


def test_get_retry_delay():
    """Test get_retry_delay function."""
    assert get_retry_delay(429) == 5.0
    assert get_retry_delay(500) == 1.0
    assert get_retry_delay(408) == 0.5
    assert get_retry_delay(400) == 1.0
    assert get_retry_delay(400, "10") == 10.0
    assert get_retry_delay(400, "not-a-number") == 1.0
