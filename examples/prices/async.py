import asyncio

from paddle.aio import AsyncClient
from paddle.environment import Environment


async def main():
    async with AsyncClient(
        api_key="API_KEY",
        environment=Environment.SANDBOX,
    ) as client:

        price = await client.price.create(
            description="Test",
            product_id="pro_01jsj3zepax5fk3enjsevsd8ra",
            unit_price={"amount": "1000", "currency_code": "USD"},
            billing_cycle={"frequency": 1, "interval": "year"},
        )
        print(price)

        prices = await client.price.list(include=["product"])
        print(prices.data)

        price = await client.price.update(
            "pri_1234567890",
            description="Test",
        )
        print(price)

        price = await client.price.get("pri_1234567890")
        print(price)


if __name__ == "__main__":
    asyncio.run(main())
