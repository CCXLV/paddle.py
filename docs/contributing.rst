Contributing
============

We welcome contributions to the Paddle SDK! This document will help you get started with contributing to the project.

Development Setup
---------------

1. Fork the repository
2. Clone your fork:

.. code-block:: bash

   git clone https://github.com/your-username/paddle-sdk.git
   cd paddle-sdk

3. Create a virtual environment:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

4. Install development dependencies:

.. code-block:: bash

   pip install -e .[dev]

5. Install pre-commit hooks:

.. code-block:: bash

   pre-commit install

Code Style
---------

We use several tools to maintain code quality:

- Black for code formatting
- Ruff for linting
- mypy for type checking
- pytest for testing

Run the following commands to ensure your code meets our standards:

.. code-block:: bash

   # Format code
   black .

   # Run linter
   ruff check .

   # Run type checker
   mypy paddle tests

   # Run tests
   pytest

Writing Tests
------------

We use pytest for testing. When adding new features or fixing bugs, please include tests.

- Place tests in the ``tests`` directory
- Use descriptive test names
- Include both positive and negative test cases
- Use fixtures when appropriate
- Mock external API calls

Example test:

.. code-block:: python

   def test_product_creation(test_client):
       mock_response = {
           "data": {
               "id": "pro_123",
               "name": "Test Product",
               "tax_category": "standard",
               "type": "custom",
               "status": "active",
               "created_at": "2021-01-01",
               "updated_at": "2021-01-01",
           },
           "meta": {"request_id": "test"},
       }
       with patch.object(test_client.product, "_create", return_value=mock_response):
           response = test_client.product.create(
               name="Test Product", tax_category="standard", type="custom"
           )
           assert isinstance(response, ProductCreateResponse)
           assert response.data.id == "pro_123"

Documentation
------------

We use Sphinx for documentation. When adding new features:

1. Update the relevant RST files in the ``docs`` directory
2. Add docstrings to your code following the Google style
3. Include examples in the documentation
4. Update the changelog

Example docstring:

.. code-block:: python

   def create_product(self, name: str, tax_category: str) -> ProductCreateResponse:
       """Create a new product.

       Args:
           name: The name of the product
           tax_category: The tax category of the product

       Returns:
           A ProductCreateResponse containing the created product

       Raises:
           PaddleValidationError: If the product data is invalid
           PaddleAPIError: If the API request fails
       """

Pull Requests
------------

When submitting a pull request:

1. Create a new branch for your feature/fix
2. Write clear commit messages
3. Include tests
4. Update documentation
5. Ensure all tests pass
6. Submit the pull request

Example commit message:

.. code-block:: text

   feat: add product creation endpoint

   - Add Product.create method
   - Add tests for product creation
   - Update documentation
   - Fix linting issues

Code Review
----------

All pull requests require review before merging. Please:

1. Address review comments
2. Keep the discussion focused on the code
3. Be open to feedback
4. Update your pull request as needed

Release Process
--------------

1. Update version in ``pyproject.toml``
2. Update changelog
3. Create a release tag
4. Build and publish the package

.. code-block:: bash

   # Update version
   poetry version patch  # or minor/major

   # Build package
   poetry build

   # Publish package
   poetry publish 