from paddle.models.responses.product import (
    ProductListResponse,
    ProductCreateResponse,
    ProductGetResponse,
    ProductData,
    ProductDataWithPrices,
    ProductMeta,
    ProductMetaWithPagination,
    Prices,
    PriceData,
    UnitPrice,
    Quantity,
    ImportMeta,
)


def test_prices_response():
    response = {
        "data": [
            {
                "id": "123",
                "name": "Test product",
                "tax_category": "standard",
                "description": "Test price",
                "type": "custom",
                "status": "active",
                "created_at": "2021-01-01",
                "updated_at": "2021-01-01",
                "prices": None,
            }
        ],
        "meta": {
            "request_id": "123",
            "pagination": {"per_page": 10, "next": "123", "has_more": True, "estimated_total": 100},
        },
    }

    response = ProductListResponse(response)

    assert response.data is not None
    assert response.meta is not None


def test_prices_with_data():
    """Test Prices class with non-None data."""
    price_data = PriceData(
        id="price_123",
        product_id="pro_123",
        description="Test price",
        type="standard",
        tax_mode="account_setting",
        unit_price=UnitPrice(amount="10.00", currency_code="USD"),
        quantity=Quantity(minimum=1, maximum=10),
        status="active",
        created_at="2021-01-01",
        updated_at="2021-01-01",
    )
    prices = Prices(data=[price_data])
    assert prices.data is not None
    assert len(prices.data) == 1
    assert prices.data[0].id == "price_123"


def test_product_data_with_all_fields():
    """Test ProductData with all optional fields."""
    product = ProductData(
        id="pro_123",
        name="Test Product",
        tax_category="standard",
        type="custom",
        status="active",
        created_at="2021-01-01",
        updated_at="2021-01-01",
        description="Test description",
        image_url="https://example.com/image.jpg",
        custom_data={"key": "value"},
        import_meta=ImportMeta(imported_from="paddle_classic"),
    )
    assert product.description == "Test description"
    assert product.image_url == "https://example.com/image.jpg"
    assert product.custom_data == {"key": "value"}
    assert product.import_meta is not None
    assert product.import_meta.imported_from == "paddle_classic"


def test_product_data_with_prices():
    """Test ProductDataWithPrices with prices."""
    price_data = PriceData(
        id="price_123",
        product_id="pro_123",
        description="Test price",
        type="standard",
        tax_mode="account_setting",
        unit_price=UnitPrice(amount="10.00", currency_code="USD"),
        unit_price_overrides=[],
        quantity=Quantity(minimum=1, maximum=10),
        status="active",
        created_at="2021-01-01",
        updated_at="2021-01-01",
    )
    prices = Prices(data=[price_data])

    product = ProductDataWithPrices(
        id="pro_123",
        name="Test Product",
        tax_category="standard",
        type="custom",
        status="active",
        created_at="2021-01-01",
        updated_at="2021-01-01",
        prices=prices,
    )
    assert product.prices is not None
    assert product.prices.data is not None
    assert len(product.prices.data) == 1
    assert product.prices.data[0].id == "price_123"


def test_product_meta():
    """Test ProductMeta and ProductMetaWithPagination."""
    meta = ProductMeta(request_id="req_123")
    assert meta.request_id == "req_123"

    meta_with_pagination = ProductMetaWithPagination(
        request_id="req_123",
        pagination={"per_page": 10, "next": "next_123", "has_more": True, "estimated_total": 100},
    )
    assert meta_with_pagination.request_id == "req_123"
    assert meta_with_pagination.pagination.per_page == 10
    assert meta_with_pagination.pagination.next == "next_123"
    assert meta_with_pagination.pagination.has_more is True
    assert meta_with_pagination.pagination.estimated_total == 100


def test_product_create_response():
    """Test ProductCreateResponse."""
    response = {
        "data": {
            "id": "pro_123",
            "name": "Test Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
            "description": "Test description",
            "image_url": "https://example.com/image.jpg",
            "custom_data": {"key": "value"},
            "import_meta": {"imported_from": "paddle_classic"},
        },
        "meta": {"request_id": "req_123"},
    }

    product_response = ProductCreateResponse(response)
    assert product_response.data.id == "pro_123"
    assert product_response.data.description == "Test description"
    assert product_response.meta.request_id == "req_123"


def test_product_get_response():
    """Test ProductGetResponse."""
    response = {
        "data": {
            "id": "pro_123",
            "name": "Test Product",
            "tax_category": "standard",
            "type": "custom",
            "status": "active",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
            "prices": {
                "data": [
                    {
                        "id": "price_123",
                        "product_id": "pro_123",
                        "description": "Test price",
                        "type": "standard",
                        "tax_mode": "account_setting",
                        "unit_price": {"amount": "10.00", "currency_code": "USD"},
                        "unit_price_overrides": [],
                        "quantity": {"minimum": 1, "maximum": 10},
                        "status": "active",
                        "created_at": "2021-01-01",
                        "updated_at": "2021-01-01",
                    }
                ]
            },
        },
        "meta": {"request_id": "req_123"},
    }

    product_response = ProductGetResponse(response)
    assert product_response.data.id == "pro_123"
    assert product_response.data.prices is not None
    assert len(product_response.data.prices.data) == 1
    assert product_response.data.prices.data[0].id == "price_123"
    assert product_response.meta.request_id == "req_123"
