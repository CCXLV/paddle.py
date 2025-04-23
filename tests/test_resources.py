import pytest

from unittest.mock import patch

from paddle.client import BaseClient
from paddle.models.resources.base import ResourceBase
from paddle.models.resources.products import ProductsBase
from paddle.models.responses.products import (
    ProductListResponse,
    ProductCreateResponse,
    ProductGetResponse,
)
from paddle.exceptions import PaddleAPIError, PaddleNotFoundError, PaddleValidationError


def test_products_resource_list(test_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        test_client.products._list()
    assert exc_info.value.status_code == 403


def test_products_resource_create(test_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        test_client.products._create()
    assert exc_info.value.status_code == 403


def test_products_resource_get(test_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        test_client.products._get("pre_123")
    assert exc_info.value.status_code == 404


def test_products_resource_update(test_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        test_client.products._update("pre_123")
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_async_products_resource_list(test_async_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        await test_async_client.products._list()
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_async_products_resource_create(test_async_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        await test_async_client.products._create()
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_async_products_resource_get(test_async_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        await test_async_client.products._get("pre_123")
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_async_products_resource_update(test_async_client):
    with pytest.raises(PaddleAPIError) as exc_info:
        await test_async_client.products._update("pre_123")
    assert exc_info.value.status_code == 404


def test_products_base(test_client):
    products = ProductsBase(test_client)
    with pytest.raises(NotImplementedError) as exc_info:
        products._list()
    assert str(exc_info.value) == "Subclasses must implement this method"

    with pytest.raises(NotImplementedError) as exc_info:
        products._create()
    assert str(exc_info.value) == "Subclasses must implement this method"

    with pytest.raises(NotImplementedError) as exc_info:
        products._get("pre_123")
    assert str(exc_info.value) == "Subclasses must implement this method"

    with pytest.raises(NotImplementedError) as exc_info:
        products._update("pre_123")
    assert str(exc_info.value) == "Subclasses must implement this method"


def test_products_list(test_client):
    mock_response = {
        "data": [],
        "meta": {
            "request_id": "test",
            "pagination": {"per_page": 50, "next": "", "has_more": False, "estimated_total": 0},
        },
    }
    with patch.object(test_client.products, "_list", return_value=mock_response):
        response = test_client.products.list()
        assert isinstance(response, ProductListResponse)
        assert response.data == []
        assert response.meta.request_id == "test"


def test_failed_products_list(test_client):
    with patch.object(test_client.products, "_list", side_effect=PaddleAPIError(404, "Not found")):
        with pytest.raises(PaddleNotFoundError) as exc_info:
            test_client.products.list()
        assert exc_info.value.status_code == 404
        assert str(exc_info.value) == "Paddle API Error: 404 - No products found"

    with patch.object(test_client.products, "_list", side_effect=PaddleAPIError(403, "Forbidden")):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client.products.list()
        assert exc_info.value.status_code == 403
        assert str(exc_info.value) == "Paddle API Error: 403 - Forbidden"


def test_products_create(test_client):
    mock_response = {
        "data": {
            "id": "pre_123",
            "name": "Test Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
        },
        "meta": {"request_id": "test"},
    }
    with patch.object(test_client.products, "_create", return_value=mock_response):
        response = test_client.products.create(
            name="Test Product", tax_category="standard", type="custom"
        )
        assert isinstance(response, ProductCreateResponse)
        assert response.data.id == "pre_123"
        assert response.data.name == "Test Product"
        assert response.data.tax_category == "standard"
        assert response.data.type == "custom"
        assert response.data.status == "active"


def test_products_create_validation_error(test_client):
    with patch.object(
        test_client.products, "_create", side_effect=PaddleAPIError(422, "Validation error")
    ):
        with pytest.raises(PaddleValidationError) as exc_info:
            test_client.products.create(name="Test Product", tax_category="standard", type="custom")
        assert str(exc_info.value) == "Paddle API Error: 422 - Validation error"


def test_products_create_other_error(test_client):
    with patch.object(
        test_client.products, "_create", side_effect=PaddleAPIError(500, "Internal server error")
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client.products.create(name="Test Product", tax_category="standard", type="custom")
        assert exc_info.value.status_code == 500
        assert str(exc_info.value) == "Paddle API Error: 500 - Internal server error"


@pytest.mark.asyncio
async def test_async_products_create_other_error(test_async_client):
    with patch.object(
        test_async_client.products,
        "_create",
        side_effect=PaddleAPIError(500, "Internal server error"),
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            await test_async_client.products.create(
                name="Test Product", tax_category="standard", type="custom"
            )
        assert exc_info.value.status_code == 500
        assert str(exc_info.value) == "Paddle API Error: 500 - Internal server error"

    with patch.object(
        test_async_client.products, "_create", side_effect=PaddleAPIError(422, "Validation error")
    ):
        with pytest.raises(PaddleValidationError) as exc_info:
            await test_async_client.products.create(
                name="Test Product", tax_category="standard", type="custom"
            )
        assert str(exc_info.value) == "Paddle API Error: 422 - Validation error"


@pytest.mark.asyncio
async def test_async_products_get_other_error(test_async_client):
    with patch.object(
        test_async_client.products, "_get", side_effect=PaddleAPIError(500, "Internal server error")
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            await test_async_client.products.get("pre_123")
        assert exc_info.value.status_code == 500
        assert str(exc_info.value) == "Paddle API Error: 500 - Internal server error"

    with patch.object(
        test_async_client.products, "_get", side_effect=PaddleAPIError(404, "Not found")
    ):
        with pytest.raises(PaddleNotFoundError) as exc_info:
            await test_async_client.products.get("pre_123")
        assert str(exc_info.value) == "Paddle API Error: 404 - Not found"


@pytest.mark.asyncio
async def test_async_products_update_other_error(test_async_client):
    with patch.object(
        test_async_client.products,
        "_update",
        side_effect=PaddleAPIError(500, "Internal server error"),
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            await test_async_client.products.update("pre_123", name="Updated Product")
        assert exc_info.value.status_code == 500
        assert str(exc_info.value) == "Paddle API Error: 500 - Internal server error"

    with patch.object(
        test_async_client.products, "_update", side_effect=PaddleAPIError(404, "Not found")
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            await test_async_client.products.update("pre_123", name="Updated Product")
        assert str(exc_info.value) == "Paddle API Error: 404 - Not found"

    with patch.object(
        test_async_client.products, "_update", side_effect=PaddleAPIError(422, "Validation error")
    ):
        with pytest.raises(PaddleValidationError) as exc_info:
            await test_async_client.products.update("pre_123", name="Updated Product")
        assert str(exc_info.value) == "Paddle API Error: 422 - Validation error"


def test_products_get(test_client):
    mock_response = {
        "data": {
            "id": "pre_123",
            "name": "Test Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
            "prices": {"data": []},
        },
        "meta": {"request_id": "test"},
    }
    with patch.object(test_client.products, "_get", return_value=mock_response):
        response = test_client.products.get("pre_123")
        assert isinstance(response, ProductGetResponse)
        assert response.data.id == "pre_123"
        assert response.data.name == "Test Product"
        assert response.data.tax_category == "standard"
        assert response.data.type == "custom"
        assert response.data.status == "active"
        assert response.data.prices.data == []


def test_products_get_not_found(test_client):
    with patch.object(test_client.products, "_get", side_effect=PaddleAPIError(404, "Not found")):
        with pytest.raises(PaddleNotFoundError) as exc_info:
            test_client.products.get("pre_123")
        assert exc_info.value.status_code == 404
        assert str(exc_info.value) == "Paddle API Error: 404 - Not found"

    with patch.object(
        test_client.products, "_get", side_effect=PaddleAPIError(500, "Internal server error")
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client.products.get("pre_123")
        assert exc_info.value.status_code == 500
        assert str(exc_info.value) == "Paddle API Error: 500 - Internal server error"


def test_products_update(test_client):
    mock_response = {
        "data": {
            "id": "pre_123",
            "name": "Updated Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
        },
        "meta": {"request_id": "test"},
    }
    with patch.object(test_client.products, "_update", return_value=mock_response):
        response = test_client.products.update("pre_123", name="Updated Product")
        assert isinstance(response, ProductCreateResponse)
        assert response.data.id == "pre_123"
        assert response.data.name == "Updated Product"
        assert response.data.tax_category == "standard"
        assert response.data.type == "custom"
        assert response.data.status == "active"


def test_products_update_validation_error(test_client):
    with patch.object(
        test_client.products, "_update", side_effect=PaddleAPIError(422, "Validation error")
    ):
        with pytest.raises(PaddleValidationError) as exc_info:
            test_client.products.update("pre_123", name="Updated Product")
        assert str(exc_info.value) == "Paddle API Error: 422 - Validation error"

    with patch.object(
        test_client.products, "_update", side_effect=PaddleAPIError(500, "Internal server error")
    ):
        with pytest.raises(PaddleAPIError) as exc_info:
            test_client.products.update("pre_123", name="Updated Product")
        assert exc_info.value.status_code == 500
        assert str(exc_info.value) == "Paddle API Error: 500 - Internal server error"


@pytest.mark.asyncio
async def test_async_products_list(test_async_client):
    mock_response = {
        "data": [],
        "meta": {
            "request_id": "test",
            "pagination": {"per_page": 50, "next": "", "has_more": False, "estimated_total": 0},
        },
    }
    with patch.object(test_async_client.products, "_list", return_value=mock_response):
        response = await test_async_client.products.list()
        assert isinstance(response, ProductListResponse)
        assert response.data == []
        assert response.meta.request_id == "test"


@pytest.mark.asyncio
async def test_async_products_create(test_async_client):
    mock_response = {
        "data": {
            "id": "pre_123",
            "name": "Test Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
        },
        "meta": {"request_id": "test"},
    }
    with patch.object(test_async_client.products, "_create", return_value=mock_response):
        response = await test_async_client.products.create(
            name="Test Product", tax_category="standard", type="custom"
        )
        assert isinstance(response, ProductCreateResponse)
        assert response.data.id == "pre_123"
        assert response.data.name == "Test Product"
        assert response.data.tax_category == "standard"
        assert response.data.type == "custom"
        assert response.data.status == "active"


@pytest.mark.asyncio
async def test_async_products_get(test_async_client):
    mock_response = {
        "data": {
            "id": "pre_123",
            "name": "Test Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
            "prices": {"data": []},
        },
        "meta": {"request_id": "test"},
    }
    with patch.object(test_async_client.products, "_get", return_value=mock_response):
        response = await test_async_client.products.get("pre_123")
        assert isinstance(response, ProductGetResponse)
        assert response.data.id == "pre_123"
        assert response.data.name == "Test Product"
        assert response.data.tax_category == "standard"
        assert response.data.type == "custom"
        assert response.data.status == "active"
        assert response.data.prices.data == []


@pytest.mark.asyncio
async def test_async_products_update(test_async_client):
    mock_response = {
        "data": {
            "id": "pre_123",
            "name": "Updated Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
        },
        "meta": {"request_id": "test"},
    }
    with patch.object(test_async_client.products, "_update", return_value=mock_response):
        response = await test_async_client.products.update("pre_123", name="Updated Product")
        assert isinstance(response, ProductCreateResponse)
        assert response.data.id == "pre_123"
        assert response.data.name == "Updated Product"
        assert response.data.tax_category == "standard"
        assert response.data.type == "custom"
        assert response.data.status == "active"


def test_resource_base_initialization(test_client):
    """Test that a resource can be initialized with a client."""

    class TestResource(ResourceBase):
        def __init__(self, client: BaseClient):
            super().__init__(client)
            self.test_value = "test"

    resource = TestResource(test_client)

    assert resource._client == test_client
    assert resource.test_value == "test"
    assert resource._client.base_url == "https://sandbox-api.paddle.com"
    assert resource._client.timeout == 30
    assert resource._client.max_retries == 3
