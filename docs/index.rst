.. paddle-sdk documentation master file, created by
   sphinx-quickstart on Sat Apr 26 01:51:05 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Paddle SDK's documentation!
====================================

Paddle SDK is a modern Python SDK for Paddle's API with type hints and async support.

Features
--------

- 🚀 Synchronous and asynchronous client implementations
- 📦 Support for Paddle's API (in development)
- 🧩 Type hints throughout the codebase
- 🔄 Automatic retry mechanism for failed requests
- 🔧 Environment configuration (Sandbox/Production)
- 🛡️ Comprehensive error handling
- 📊 Extensive test coverage

Installation
-----------

.. code-block:: bash

   pip install paddle-sdk

Quick Start
----------

Synchronous Client
~~~~~~~~~~~~~~~~

.. code-block:: python

   from paddle import Client, Environment

   # Initialize the client
   client = Client(
       api_key="your-api-key",
       environment=Environment.SANDBOX  # or Environment.PRODUCTION
   )

   # List products
   products = client.product.list()
   print(products)

   # Get a specific product
   product = client.product.get(product_id="pro_123")
   print(product)

Asynchronous Client
~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio

   from paddle.aio import AsyncClient
   from paddle.environment import Environment

   async def main():
       async with AsyncClient(
           api_key="API_KEY",
           environment=Environment.SANDBOX,  # or Environment.PRODUCTION
       ) as client:
           # List products
           all_products = await client.product.list()
           print(all_products)

           # Get a product
           product = await client.product.get("pro_123456789")
           print(product)

   if __name__ == "__main__":
       asyncio.run(main())

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   api
   examples
   contributing
   changelog

