import asyncio

from paddle.aio import AsyncClient
from paddle.environment import Environment


async def main():
    async with AsyncClient(
        api_key="API_KEY",
        environment=Environment.SANDBOX,
    ) as client:
        # Get all customers
        customers = await client.customers.list()
        print(customers)

        # Create a customer
        customer = await client.customers.create(
            email="test@example.com",
            name="Test Customer",
        )
        print(customer)

        # Get a customer
        customer = await client.customers.get("ctm_0123456789")
        print(customer)

        # Update a customer
        updated_customer = await client.customers.update(
            "ctm_0123456789",
            email="updated@example.com",
            name="Updated Customer",
        )
        print(updated_customer)

        # List credit balances
        credit_balances = await client.customers.list_credit_balances("ctm_0123456789")
        print(credit_balances)

        # Generate auth token
        auth_token = await client.customers.generate_auth_token("ctm_0123456789")
        print(auth_token)


if __name__ == "__main__":
    asyncio.run(main())
