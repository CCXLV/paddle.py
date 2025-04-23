import httpx
import pytest

from unittest.mock import patch

from paddle.exceptions import PaddleAPIError


def test_authentication_error(test_client):
    """Test authentication error handling."""
    mock_response = httpx.Response(401, json={"error": "Authentication error"})
    with patch.object(test_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 401
        assert "Authentication error" in str(exc_info.value)


def test_permission_error(test_client):
    """Test permission error handling."""
    mock_response = httpx.Response(403, json={"error": "Permission error"})
    with patch.object(test_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 403
        assert "Permission error" in str(exc_info.value)


def test_not_found_error(test_client):
    """Test not found error handling."""
    mock_response = httpx.Response(404, json={"error": "Not found error"})
    with patch.object(test_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 404
        assert "Not found error" in str(exc_info.value)


def test_validation_error(test_client):
    """Test validation error handling."""
    mock_response = httpx.Response(422, json={"error": "Validation error"})
    with patch.object(test_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 422
        assert "Validation error" in str(exc_info.value)


def test_rate_limit_error(test_client):
    """Test rate limit error handling."""
    mock_response = httpx.Response(429, json={"error": "Rate limit error"})
    with patch.object(test_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 429
        assert "Rate limit error" in str(exc_info.value)


def test_server_error(test_client):
    """Test server error handling."""
    mock_response = httpx.Response(500, json={"error": "Server error"})
    with patch.object(test_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 500
        assert "Server error" in str(exc_info.value)
