from typing import Union, Optional, Literal, Dict, Any

from paddle.client import Client
from paddle.aio.client import AsyncClient

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.product import ProductListResponse, ProductCreateResponse, ProductGetResponse

from paddle.utils.decorators import validate_params
from paddle.utils.constants import TAX_CATEGORY
from paddle.utils.helpers import filter_none_kwargs
from paddle.exceptions import PaddleAPIError, PaddleValidationError, PaddleNotFoundError


class ProductBase(ResourceBase):
    """Base resource for Paddle Products API endpoints."""

    def __init__(self, client: Union[Client, AsyncClient]):
        self._client = client

    def _list(self) -> Dict[str, Any]:
        """Internal method to list products."""
        raise NotImplementedError("Subclasses must implement this method")

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def _get(self, product_id: str) -> Dict[str, Any]:
        """Internal method to get a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def _update(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def list(self) -> ProductListResponse:
        """
        Get all products.

        Returns
        -------

        A list of products.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleNotFoundError: If the product is not found.

        Examples
        --------

        Getting all products ::

            from paddle import Client

            client = Client(api_key="your_api_key")

            products = client.products.list()
            print(products)
        """
        try:
            response = self._list()
            return ProductListResponse(response)
        except PaddleAPIError as e:
            if e.status_code == 404:
                raise PaddleNotFoundError("No products found") from e
            raise

    @validate_params
    def create(
        self,
        *,
        name: str,
        tax_category: TAX_CATEGORY,
        description: Optional[str] = None,
        type: Optional[Literal["custom", "standard"]] = None,
        image_url: Optional[str] = None,
        custom_data: Optional[Dict[str, Any]] = None,
    ) -> ProductCreateResponse:
        """
        Create a new product.

        Args
        ---- ::

            name: str
            tax_category: Literal[
                "digital-goods",
                "ebooks",
                "implementation-services",
                "professional-services",
                "saas",
                "software-programming-services",
                "standard",
                "training-services",
                "website-hosting",
            ]
            description: Optional[str] = None
            type: Optional[Literal["custom", "standard"]] = None
            image_url: Optional[str] = None
            custom_data: Optional[Dict[str, Any]] = None

        Returns
        -------

        A new product.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleValidationError: If the product is not valid.

        Examples
        --------

        Creating a new product ::

            from paddle import Client

            client = Client(api_key="your_api_key")

            product = client.products.create(
                name="My Product",
                tax_category="standard",
                description="My Product Description",
            )
            print(product)
        """
        try:
            kwargs = filter_none_kwargs(
                name=name,
                tax_category=tax_category,
                description=description,
                type=type,
                image_url=image_url,
                custom_data=custom_data,
            )
            response = self._create(**kwargs)
            
            return ProductCreateResponse(response)
        except PaddleAPIError as e:
            if e.status_code == 422:
                raise PaddleValidationError(e.message) from e
            raise

    @validate_params
    def get(self, product_id: str) -> ProductGetResponse:
        """
        Gets a product by ID.

        Args
        ----

            product_id: The ID of the product to get.

        Returns
        -------

        A product by ID.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleNotFoundError: If the product is not found.

        Examples
        --------

        Getting a product by ID ::

            from paddle import Client

            client = Client(api_key="your_api_key")

            product = client.products.get("pro_1234567890")
            print(product)
        """
        try:
            response = self._get(product_id)
            return ProductGetResponse(response)
        except PaddleAPIError as e:
            if e.status_code == 404:
                raise PaddleNotFoundError(e.message) from e
            raise

    @validate_params
    def update(
        self,
        product_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[Literal["custom", "standard"]] = None,
        tax_category: Optional[TAX_CATEGORY] = None,
        image_url: Optional[str] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        status: Optional[Literal["active", "archived"]] = None,
    ) -> ProductCreateResponse:
        """
        Update a product.

        Args
        ---- ::

            name: Optional[str] = None
            description: Optional[str] = None
            type: Optional[Literal["custom", "standard"]] = None
            tax_category: Optional[Literal[
                "digital-goods",
                "ebooks",
                "implementation-services",
                "professional-services",
                "saas",
                "software-programming-services",
                "standard",
                "training-services",
                "website-hosting",
            ]] = None
            image_url: Optional[str] = None
            custom_data: Optional[Dict[str, Any]] = None
            status: Optional[Literal["active", "archived"]] = None

        Returns
        -------

        Updated product.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleValidationError: If the product is not valid.

        Examples
        --------

        Updating a product ::

            from paddle import Client

            client = Client(api_key="your_api_key")

            product = client.products.update(
                "pro_1234567890",
                name="My Updated Product",
                tax_category="standard",
            )
            print(product)
        """
        try:
            kwargs = filter_none_kwargs(
                product_id=product_id,
                name=name,
                description=description,
                type=type,
                tax_category=tax_category,
                image_url=image_url,
                custom_data=custom_data,
                status=status,
            )

            response = self._update(**kwargs)
            return ProductCreateResponse(response)
        except PaddleAPIError as e:
            if e.status_code == 422:
                raise PaddleValidationError(e.message) from e
            raise


class Product(ProductBase):
    """Resource for Paddle Products API endpoints."""

    def __init__(self, client: Client):
        super().__init__(client)

    def _list(self) -> Dict[str, Any]:
        """Internal method to list products."""
        return self._client._request(
            method="GET",
            path="/products",
        )

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a price."""
        return self._client._request(
            method="POST",
            path="/products",
            json=kwargs,
        )

    def _get(self, product_id: str) -> Dict[str, Any]:
        """Internal method to get a price."""
        return self._client._request(
            method="GET",
            path=f"/products/{product_id}",
        )

    def _update(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a product."""
        return self._client._request(
            method="PATCH",
            path=f"/products/{product_id}",
            json=kwargs,
        )


class AsyncProduct(ProductBase):
    """Resource for Paddle Products API endpoints."""

    def __init__(self, client: AsyncClient):
        super().__init__(client)

    async def _list(self) -> Dict[str, Any]:
        """Internal method to list products."""
        return await self._client._request(
            method="GET",
            path="/products",
        )

    async def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a product."""
        return await self._client._request(
            method="POST",
            path="/products",
            json=kwargs,
        )

    async def _get(self, product_id: str) -> Dict[str, Any]:
        """Internal method to get a product."""
        return await self._client._request(
            method="GET",
            path=f"/products/{product_id}",
        )

    async def _update(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a product."""
        return await self._client._request(
            method="PATCH",
            path=f"/products/{product_id}",
            json=kwargs,
        )

    async def list(self) -> ProductListResponse:
        """|coroutine|

        Get all products.

        Returns
        -------

        A list of products.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleNotFoundError: If the product is not found.

        Examples
        --------

        Getting all products ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    products = await client.products.list()
                    print(products)

            asyncio.run(main())
        """
        response = await self._list()
        return ProductListResponse(response)

    async def create(
        self,
        *,
        name: str,
        tax_category: TAX_CATEGORY,
        description: Optional[str] = None,
        type: Optional[Literal["custom", "standard"]] = None,
        image_url: Optional[str] = None,
        custom_data: Optional[Dict[str, Any]] = None,
    ) -> ProductCreateResponse:
        """|coroutine|

        Create a new product.

        Args
        ---- ::

            name: str
            tax_category: Literal[
                "digital-goods",
                "ebooks",
                "implementation-services",
                "professional-services",
                "saas",
                "software-programming-services",
                "standard",
                "training-services",
                "website-hosting",
            ]
            description: Optional[str] = None
            type: Optional[Literal["custom", "standard"]] = None
            image_url: Optional[str] = None
            custom_data: Optional[Dict[str, Any]] = None

        Returns
        -------

        A new product.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleValidationError: If the product is not valid.

        Examples
        --------

        Creating a new product ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    product = await client.products.create(
                        name="My Product",
                        tax_category="standard",
                        description="My Product Description",
                    )
                    print(product)

            asyncio.run(main())
        """
        try:
            kwargs = filter_none_kwargs(
                name=name,
                tax_category=tax_category,
                description=description,
                type=type,
                image_url=image_url,
                custom_data=custom_data,
            )
            response = await self._create(**kwargs)

            return ProductCreateResponse(response)
        except PaddleAPIError as e:
            if e.status_code == 422:
                raise PaddleValidationError(e.message) from e
            raise

    @validate_params
    async def get(self, product_id: str) -> ProductGetResponse:
        """|coroutine|

        Gets a product by ID.

        Args
        ----

            product_id: The ID of the product to get.

        Returns
        -------

            A product by ID.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleNotFoundError: If the product is not found.

        Examples
        --------

        Getting a product by ID ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    product = await client.products.get("pro_1234567890")
                    print(product)

            asyncio.run(main())
        """
        try:
            response = await self._get(product_id)
            return ProductGetResponse(response)
        except PaddleAPIError as e:
            if e.status_code == 404:
                raise PaddleNotFoundError(e.message) from e
            raise

    @validate_params
    async def update(
        self,
        product_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[Literal["custom", "standard"]] = None,
        tax_category: Optional[TAX_CATEGORY] = None,
        image_url: Optional[str] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        status: Optional[Literal["active", "archived"]] = None,
    ) -> ProductCreateResponse:
        """|coroutine|

        Update a product.

        Args
        ---- ::

            name: Optional[str] = None
            description: Optional[str] = None
            type: Optional[Literal["custom", "standard"]] = None
            tax_category: Optional[Literal[
                "digital-goods",
                "ebooks",
                "implementation-services",
                "professional-services",
                "saas",
                "software-programming-services",
                "standard",
                "training-services",
                "website-hosting",
            ]] = None
            image_url: Optional[str] = None
            custom_data: Optional[Dict[str, Any]] = None
            status: Optional[Literal["active", "archived"]] = None

        Returns
        -------

        Updated product.

        Raises
        ------

        PaddleAPIError: If the API request fails.
        PaddleValidationError: If the product is not valid.

        Examples
        --------

        Updating a product ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    product = await client.products.update(
                        "pro_1234567890",
                        name="My Updated Product",
                        tax_category="standard",
                    )
                    print(product)

            asyncio.run(main())
        """
        try:
            kwargs = filter_none_kwargs(
                product_id=product_id,
                name=name,
                description=description,
                type=type,
                tax_category=tax_category,
                image_url=image_url,
                custom_data=custom_data,
                status=status,
            )
            response = await self._update(**kwargs)

            return ProductCreateResponse(response)
        except PaddleAPIError as e:
            if e.status_code == 422:
                raise PaddleValidationError(e.message) from e
            raise
