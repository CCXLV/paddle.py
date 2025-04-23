import json

import pytest
import httpx

from unittest.mock import patch
from paddle.client import Client, Environment
from paddle.aio.client import AsyncClient
from paddle.exceptions import PaddleAPIError


def test_client_initialization():
    """Test client initialization with different parameters."""
    client = Client(api_key="test-key", environment=Environment.SANDBOX)
    assert client.api_key == "test-key"
    assert client.base_url == Environment.SANDBOX.base_url.rstrip("/")
    assert client.timeout == 30  # default timeout
    assert client.max_retries == 3  # default retries


def test_successful_request(test_client):
    """Test successful API request."""
    mock_response = httpx.Response(200, json={"success": True})
    with patch.object(test_client._client, "request", return_value=mock_response):
        resp = test_client._request("GET", "/test")
        assert resp == {"success": True}


def test_retry_on_error(test_client):
    """Test request retry mechanism."""
    responses = [
        httpx.Response(500, json={"error": "Server Error"}),
        httpx.Response(200, json={"success": True}),
    ]

    with patch.object(test_client._client, "request", side_effect=responses):
        resp = test_client._request("GET", "/test")
        assert resp == {"success": True}


def test_max_retries_exceeded(test_client):
    """Test that max retries are respected."""
    mock_response = httpx.Response(500, json={"error": "Server Error"})

    with patch.object(test_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 500


def test_client_context_manager():
    """Test client works as context manager."""
    with Client(api_key="test-key", environment=Environment.SANDBOX) as client:
        assert isinstance(client._client, httpx.Client)


def test_network_error(test_client):
    """Test network error handling."""
    with patch.object(
        test_client._client, "request", side_effect=httpx.RequestError("Network error")
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client._request("GET", "/test")
        assert exc_info.value.status_code == 500
        assert "Network error" in str(exc_info.value)


@pytest.mark.asyncio
async def test_async_client_initialization():
    """Test client initialization with different parameters."""
    client = AsyncClient(api_key="test-key", environment=Environment.SANDBOX)
    assert client.api_key == "test-key"
    assert client.base_url == Environment.SANDBOX.base_url.rstrip("/")
    assert client.timeout == 30  # default timeout
    assert client.max_retries == 3  # default retries


@pytest.mark.asyncio
async def test_async_successful_request(test_async_client):
    """Test successful API request."""
    mock_response = httpx.Response(200, json={"success": True})
    with patch.object(test_async_client._client, "request", return_value=mock_response):
        resp = await test_async_client._request("GET", "/test")
        assert resp == {"success": True}


@pytest.mark.asyncio
async def test_async_retry_on_error(test_async_client):
    """Test request retry mechanism."""
    responses = [
        httpx.Response(500, json={"error": "Server Error"}),
        httpx.Response(200, json={"success": True}),
    ]

    with patch.object(test_async_client._client, "request", side_effect=responses):
        resp = await test_async_client._request("GET", "/test")
        assert resp == {"success": True}


@pytest.mark.asyncio
async def test_async_max_retries_exceeded(test_async_client):
    """Test that max retries are respected."""
    mock_response = httpx.Response(500, json={"error": "Server Error"})

    with patch.object(test_async_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            await test_async_client._request("GET", "/test")
        assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_async_client_context_manager():
    """Test async client works as context manager."""
    async with AsyncClient(api_key="test-key", environment=Environment.SANDBOX) as client:
        assert isinstance(client._client, httpx.AsyncClient)
    # Client should be closed after context


@pytest.mark.asyncio
async def test_custom_timeout_and_retries():
    """Test client initialization with custom timeout and retries."""
    client = AsyncClient(
        api_key="test-key", environment=Environment.SANDBOX, timeout=60, max_retries=5
    )
    assert client.timeout == 60
    assert client.max_retries == 5


@pytest.mark.asyncio
async def test_invalid_response_format(test_async_client):
    """Test handling of invalid response format."""
    mock_response = httpx.Response(200, text="invalid json")
    mock_response.json = lambda: json.loads("invalid json")  # This will raise JSONDecodeError

    with patch.object(test_async_client._client, "request", return_value=mock_response):
        with pytest.raises(PaddleAPIError) as exc_info:
            await test_async_client._request("GET", "/test")
        assert exc_info.value.status_code == 200
        assert "Invalid JSON response" in str(exc_info.value)


@pytest.mark.asyncio
async def test_async_network_error(test_async_client):
    """Test network error handling."""
    with patch.object(
        test_async_client._client, "request", side_effect=httpx.RequestError("Network error")
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            await test_async_client._request("GET", "/test")
        assert exc_info.value.status_code == 500
