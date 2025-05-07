import asyncio

from paddle.aio import AsyncClient
from paddle.environment import Environment


async def main():
    async with AsyncClient(
        api_key="API_KEY",
        environment=Environment.SANDBOX,
    ) as client:
        initial_product = await client.products.create(
            name="Test Product",
            tax_category="standard",
            description="Test Description",
            image_url="https://example.com/image.png",
            custom_data={"key": "value"},
        )
        print(initial_product)

        # List products
        all_products = await client.products.list()
        print(all_products)

        # Get a product
        product = await client.products.get(initial_product.data.id)
        print(product)

        # Update a product
        updated_product = await client.products.update(
            initial_product.data.id,
            name="Updated Product",
            description="Updated Description",
            image_url="https://example.com/updated-image.png",
            custom_data={"key": "updated-value"},
        )
        print(updated_product)


if __name__ == "__main__":
    asyncio.run(main())
