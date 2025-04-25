Usage Guide
===========

This guide will help you get started with the Paddle SDK. We'll cover the basic usage patterns and show you how to use both the synchronous and asynchronous clients.

Client Initialization
-------------------

The SDK provides two types of clients: synchronous and asynchronous. Both support the same features but have different usage patterns.

Synchronous Client
~~~~~~~~~~~~~~~~

.. code-block:: python

   from paddle import Client, Environment

   # Initialize the client
   client = Client(
       api_key="your-api-key",
       environment=Environment.SANDBOX,  # or Environment.PRODUCTION
       timeout=30,  # optional: request timeout in seconds
       max_retries=3,  # optional: maximum number of retries
   )

   # Use the client
   products = client.product.list()

Asynchronous Client
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from paddle.aio import AsyncClient
   from paddle.environment import Environment

   async def main():
       async with AsyncClient(
           api_key="your-api-key",
           environment=Environment.SANDBOX,  # or Environment.PRODUCTION
           timeout=30,  # optional: request timeout in seconds
           max_retries=3,  # optional: maximum number of retries
       ) as client:
           products = await client.product.list()

   if __name__ == "__main__":
       asyncio.run(main())

Environment Configuration
-----------------------

The SDK supports two environments:

- ``Environment.SANDBOX``: For testing and development
- ``Environment.PRODUCTION``: For production use

.. code-block:: python

   from paddle import Environment

   # Use sandbox environment for testing
   sandbox_client = Client(api_key="test-key", environment=Environment.SANDBOX)

   # Use production environment for live data
   production_client = Client(api_key="live-key", environment=Environment.PRODUCTION)

Error Handling
------------

The SDK provides comprehensive error handling through custom exceptions:

.. code-block:: python

   from paddle import Client
   from paddle.exceptions import (
       PaddleAPIError,
       PaddleAuthenticationError,
       PaddlePermissionError,
       PaddleNotFoundError,
       PaddleValidationError,
       PaddleRateLimitError,
       PaddleServerError,
   )

   try:
       client.product.get("non-existent-id")
   except PaddleNotFoundError as e:
       print(f"Product not found: {e}")
   except PaddleAPIError as e:
       print(f"API error: {e}")

Available Resources
-----------------

The SDK currently supports the following resources:

Products
~~~~~~~~

.. code-block:: python

   # List products
   products = client.product.list()

   # Get a specific product
   product = client.product.get(product_id="pro_123")

   # Create a product
   new_product = client.product.create(
       name="My Product",
       tax_category="standard",
       description="Product description",
   )

   # Update a product
   updated_product = client.product.update(
       product_id="pro_123",
       name="Updated Name",
       description="Updated description",
   )

Retry Mechanism
--------------

The SDK includes an automatic retry mechanism for failed requests. It will retry requests that fail with:

- 5xx server errors
- 429 rate limit errors
- 408 request timeout errors

The retry mechanism uses exponential backoff and respects the ``Retry-After`` header when present.

.. code-block:: python

   # Configure retry behavior
   client = Client(
       api_key="your-api-key",
       max_retries=5,  # Increase max retries
   )

   # Disable retries for a specific request
   try:
       response = client._request("GET", "/endpoint", retry_on_error=False)
   except PaddleAPIError as e:
       print(f"Request failed: {e}") 