Examples
========

This section provides practical examples of using the Paddle SDK.

Basic Product Operations
-----------------------

Synchronous Example
~~~~~~~~~~~~~~~~~

.. code-block:: python

   from paddle import Client, Environment

   # Initialize the client
   client = Client(
       api_key="your-api-key",
       environment=Environment.SANDBOX,
   )

   # Create a product
   product = client.product.create(
       name="My Product",
       tax_category="standard",
       description="A test product",
       image_url="https://example.com/image.png",
       custom_data={"key": "value"},
   )
   print(f"Created product: {product.data.id}")

   # List products
   products = client.product.list(
       status=["active"],
       tax_category=["standard"],
       order_by="created_at[DESC]",
       per_page=10,
   )
   print(f"Found {len(products.data)} products")

   # Get a product
   product = client.product.get(
       product_id=product.data.id,
       include=["prices"],
   )
   print(f"Product details: {product.data}")

   # Update a product
   updated_product = client.product.update(
       product_id=product.data.id,
       name="Updated Product",
       description="Updated description",
       status="archived",
   )
   print(f"Updated product: {updated_product.data}")

Asynchronous Example
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from paddle.aio import AsyncClient
   from paddle.environment import Environment

   async def main():
       async with AsyncClient(
           api_key="your-api-key",
           environment=Environment.SANDBOX,
       ) as client:
           # Create a product
           product = await client.product.create(
               name="My Product",
               tax_category="standard",
               description="A test product",
               image_url="https://example.com/image.png",
               custom_data={"key": "value"},
           )
           print(f"Created product: {product.data.id}")

           # List products
           products = await client.product.list(
               status=["active"],
               tax_category=["standard"],
               order_by="created_at[DESC]",
               per_page=10,
           )
           print(f"Found {len(products.data)} products")

           # Get a product
           product = await client.product.get(
               product_id=product.data.id,
               include=["prices"],
           )
           print(f"Product details: {product.data}")

           # Update a product
           updated_product = await client.product.update(
               product_id=product.data.id,
               name="Updated Product",
               description="Updated description",
               status="archived",
           )
           print(f"Updated product: {updated_product.data}")

   if __name__ == "__main__":
       asyncio.run(main())

Error Handling
-------------

.. code-block:: python

   from paddle import Client
   from paddle.exceptions import (
       PaddleAPIError,
       PaddleNotFoundError,
       PaddleValidationError,
   )

   client = Client(api_key="your-api-key")

   try:
       # Try to get a non-existent product
       product = client.product.get("non-existent-id")
   except PaddleNotFoundError as e:
       print(f"Product not found: {e}")
   except PaddleAPIError as e:
       print(f"API error: {e}")

   try:
       # Try to create a product with invalid data
       product = client.product.create(
           name="",  # Empty name is invalid
           tax_category="invalid-category",  # Invalid tax category
       )
   except PaddleValidationError as e:
       print(f"Validation error: {e}")

Retry Mechanism
--------------

.. code-block:: python

   from paddle import Client

   # Configure retry behavior
   client = Client(
       api_key="your-api-key",
       max_retries=5,  # Increase max retries
   )

   try:
       # This request will be retried if it fails
       response = client._request("GET", "/endpoint")
   except PaddleAPIError as e:
       print(f"Request failed after retries: {e}")

   try:
       # This request won't be retried
       response = client._request("GET", "/endpoint", retry_on_error=False)
   except PaddleAPIError as e:
       print(f"Request failed without retries: {e}") 