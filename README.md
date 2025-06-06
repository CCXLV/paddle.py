# Paddle SDK

A modern Python API wrapper for Paddle's API with type hints and async support.

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="Python Version"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
</p>

## Features

- 🚀 Synchronous and asynchronous client implementations
- 📦 Support for Paddle's API (in development)
- 🧩 Type hints throughout the codebase
- 🔄 Automatic retry mechanism for failed requests
- 🔧 Environment configuration (Sandbox/Production)
- 🛡️ Comprehensive error handling
- 📊 Extensive test coverage

## Installation

```bash
pip install paddle.py
```

## Quick Start

### Synchronous Client

```python
from paddle import Client, Environment

# Initialize the client
client = Client(
    api_key="API_KEY",
    environment=Environment.SANDBOX  # or Environment.PRODUCTION
)

# List products
products = client.products.list()
print(products)

# Get a specific product
product = client.products.get(product_id="pro_123456789")
print(product)
```

### Asynchronous Client

```python
import asyncio

from paddle.aio import AsyncClient
from paddle import Environment


async def main():
    async with AsyncClient(
        api_key="API_KEY",
        environment=Environment.SANDBOX,  # or Environment.PRODUCTION
    ) as client:
        # List products
        all_products = await client.products.list()
        print(all_products)

        # Get a product
        product = await client.products.get("pro_123456789")
        print(product)


if __name__ == "__main__":
    asyncio.run(main())
```

## Development

### Setup

1. Clone the repository:

```bash
git clone https://github.com/CCXLV/paddle.py.git
cd paddle.py
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -e .[dev]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=paddle
```

## Contributing

For detailed information on how to contribute to this project, please see our [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Roadmap

See the [CHANGELOG.md](CHANGELOG.md) for planned API endpoints and features.
