from paddle import Client, Environment

client = Client(
    api_key="API_KEY",
    environment=Environment.SANDBOX,
)

price = client.price.create(
    description="Test",
    product_id="pro_01jsj3zepax5fk3enjsevsd8ra",
    unit_price={"amount": "10", "currency_code": "USD"},
)
print(price)

prices = client.price.list(include=["product"])
print(prices.data)
