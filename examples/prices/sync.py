from paddle import Client, Environment

client = Client(
    api_key="API_KEY",
    environment=Environment.SANDBOX,
)

price = client.prices.create(
    description="Test",
    product_id="pro_1234567890",
    unit_price={"amount": "10", "currency_code": "USD"},
)
print(price)

prices = client.prices.list(include=["product"])
print(prices)

price = client.prices.update(
    "pri_1234567890",
    description="Test",
)
print(price)

price = client.prices.get("pri_1234567890")
print(price)
