import pytest
import pytest_asyncio

from paddle.client import Client, Environment
from paddle.aio.client import AsyncClient


@pytest.fixture
def test_client():
    # Unit test version, no network calls
    return Client(api_key="fake-key", environment=Environment.SANDBOX)


@pytest_asyncio.fixture
async def test_async_client():
    # Unit test version, no network calls
    return AsyncClient(api_key="fake-key", environment=Environment.SANDBOX)
