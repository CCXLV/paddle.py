import asyncio

from paddle.aio import AsyncClient
from paddle.environment import Environment


async def main():
    async with AsyncClient(
        api_key="API_KEY",
        environment=Environment.SANDBOX,
    ) as client:

        price = await client.prices.create(
            description="Test",
            product_id="pro_1234567890",
            unit_price={"amount": "1000", "currency_code": "USD"},
            billing_cycle={"frequency": 1, "interval": "year"},
        )
        print(price)

        prices = await client.prices.list(include=["product"])
        print(prices.data)

        price = await client.prices.update(
            "pri_1234567890",
            description="Test",
        )
        print(price)

        price = await client.prices.get("pri_1234567890")
        print(price)


if __name__ == "__main__":
    asyncio.run(main())
