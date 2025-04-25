API Reference
============

This section provides detailed documentation for the Paddle SDK's API.

Client
------

.. autoclass:: paddle.Client
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.aio.AsyncClient
   :members:
   :undoc-members:
   :show-inheritance:

Environment
----------

.. autoclass:: paddle.Environment
   :members:
   :undoc-members:
   :show-inheritance:

Resources
--------

Products
~~~~~~~~

.. autoclass:: paddle.models.resources.product.Product
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.resources.product.AsyncProduct
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

Product Models
~~~~~~~~~~~~~

.. autoclass:: paddle.models.responses.product.ProductData
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.ProductDataWithPrices
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.PriceData
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.UnitPrice
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.Quantity
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.BillingCycle
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.UnitPriceOverrides
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.ImportMeta
   :members:
   :undoc-members:
   :show-inheritance:

Response Models
~~~~~~~~~~~~~~

.. autoclass:: paddle.models.responses.product.ProductListResponse
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.ProductCreateResponse
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: paddle.models.responses.product.ProductGetResponse
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
---------

.. autoexception:: paddle.exceptions.PaddleAPIError
   :members:
   :show-inheritance:

.. autoexception:: paddle.exceptions.PaddleAuthenticationError
   :members:
   :show-inheritance:

.. autoexception:: paddle.exceptions.PaddlePermissionError
   :members:
   :show-inheritance:

.. autoexception:: paddle.exceptions.PaddleNotFoundError
   :members:
   :show-inheritance:

.. autoexception:: paddle.exceptions.PaddleValidationError
   :members:
   :show-inheritance:

.. autoexception:: paddle.exceptions.PaddleRateLimitError
   :members:
   :show-inheritance:

.. autoexception:: paddle.exceptions.PaddleServerError
   :members:
   :show-inheritance:

Utilities
--------

.. autofunction:: paddle.utils.decorators.validate_params
   :noindex:

.. autofunction:: paddle.utils.helpers.filter_none_kwargs
   :noindex:

.. autofunction:: paddle.utils.request.is_retryable_status_code
   :noindex:

.. autofunction:: paddle.utils.request.get_retry_delay
   :noindex:

Constants
--------

.. autodata:: paddle.utils.constants.TAX_CATEGORY
   :annotation:

.. autodata:: paddle.utils.constants.CURRENCY_CODE
   :annotation:

.. autodata:: paddle.utils.constants.COUNTRY_CODE
   :annotation: 