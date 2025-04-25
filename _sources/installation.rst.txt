Installation
============

Requirements
-----------

- Python 3.8 or higher
- pip (Python package installer)

Installing the Package
--------------------

You can install the Paddle SDK using pip:

.. code-block:: bash

   pip install paddle-sdk

Development Installation
----------------------

If you want to contribute to the project or run the tests, you'll need to install the package in development mode:

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/CCXLV/paddle-sdk.git
   cd paddle-sdk

2. Create a virtual environment:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

3. Install development dependencies:

.. code-block:: bash

   pip install -e .[dev]

Running Tests
------------

To run the test suite:

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=paddle

Dependencies
-----------

The package has the following dependencies:

- httpx: For making HTTP requests
- pydantic: For data validation and settings management
- pytest: For running tests
- pytest-asyncio: For running async tests
- pytest-cov: For test coverage
- black: For code formatting
- ruff: For linting 