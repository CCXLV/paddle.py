"""
Paddle Products API endpoints.
"""

from typing import Union, Optional, Literal, Annotated, Dict, Any, List

from pydantic import Field

from paddle.client import Client
from paddle.aio.client import AsyncClient

from paddle.models.resources.base import ResourceBase
from paddle.models.responses.products import (
    ProductListResponse,
    ProductCreateResponse,
    ProductGetResponse,
)

from paddle.utils.constants import TAX_CATEGORY
from paddle.utils.decorators import validate_params
from paddle.utils.helpers import filter_none_kwargs

from paddle.exceptions import PaddleAPIError, create_paddle_error


class ProductBase(ResourceBase):
    """Base resource for Paddle Products API endpoints."""

    def __init__(self, client: Union[Client, AsyncClient]):
        self._client = client

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list products."""
        raise NotImplementedError("Subclasses must implement this method")

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def _get(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to get a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def _update(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a product."""
        raise NotImplementedError("Subclasses must implement this method")

    def list(
        self,
        *,
        after: Optional[str] = None,
        id: Optional[List[str]] = None,
        include: Optional[List[Literal["prices"]]] = None,
        order_by: Optional[
            Literal[
                "created_at[ASC]",
                "created_at[DESC]",
                "updated_at[ASC]",
                "updated_at[DESC]",
                "custom_data[ASC]",
                "custom_data[DESC]",
                "description[ASC]",
                "description[DESC]",
                "id[ASC]",
                "id[DESC]",
                "image_url[ASC]",
                "image_url[DESC]",
                "name[ASC]",
                "name[DESC]",
                "status[ASC]",
                "status[DESC]",
                "tax_category[ASC]",
                "tax_category[DESC]",
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        status: Optional[List[Literal["active", "archived"]]] = None,
        tax_category: Optional[List[TAX_CATEGORY]] = None,
        type: Optional[Literal["custom", "standard"]] = None,
    ) -> ProductListResponse:
        """
        Get all products.

        Parameters
        ----------

            after: Optional[str] = None
                Return entities after the specified Paddle ID when working with paginated endpoints.

            id: Optional[List[str]] = None
                Return only the IDs specified.

            include: Optional[List[Literal["prices"]]] = None
                Include related entities in the response.

            order_by: Optional[Literal[str]] = None
                Order returned entities by the specified field and direction ([ASC] or [DESC]).

            per_page: Optional[int] = 50
                Set how many entities are returned per page.
                Default: 50; Maximum: 200.

            status: Optional[List[Literal["active", "archived"]]] = None
                Return entities that match the specified status. Use a comma-separated list to specify multiple status values.

            tax_category: Optional[List[TAX_CATEGORY]] = None
                Return entities that match the specified tax category. Use a comma-separated list to specify multiple tax categories.

            type: Optional[Literal["custom", "standard"]] = None
                Return items that match the specified type.


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
            kwargs = filter_none_kwargs(
                after=after,
                id=",".join(id) if id else None,
                include=",".join(include) if include else None,
                order_by=order_by,
                per_page=per_page,
                status=",".join(status) if status else None,
                tax_category=",".join(tax_category) if tax_category else None,
                type=type,
            )
            response = self._list(**kwargs)

            return ProductListResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

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

        Parameters
        ----------

            name: str
                The name of the product.

            tax_category: TAX_CATEGORY
                Tax category for this product. Used for charging the correct rate of tax. Selected tax category must be enabled on your Paddle account.

            description: Optional[str] = None
                Short description for this product.

            type: Optional[Literal["custom", "standard"]] = None
                The type of the product.

            image_url: Optional[str] = None
                The image URL of the product.

            custom_data: Optional[Dict[str, Any]] = None
                Arbitrary data you can store with this product.

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
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    def get(
        self,
        product_id: str,
        *,
        include: Optional[List[Literal["prices"]]] = None,
    ) -> ProductGetResponse:
        """
        Gets a product by ID.

        Parameters
        ----------

            product_id: The ID of the product to get.

            include: Optional[List[Literal["prices"]]] = None
                Include related entities in the response.

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
            kwargs = filter_none_kwargs(
                include=",".join(include) if include else None,
            )
            response = self._get(product_id, **kwargs)

            return ProductGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

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

        Parameters
        ----------

            name: Optional[str] = None
                The name of the product.

            description: Optional[str] = None
                Short description for this product.

            type: Optional[Literal["custom", "standard"]] = None
                The type of the product.

            tax_category: Optional[TAX_CATEGORY] = None
                Tax category for this product. Used for charging the correct rate of tax. Selected tax category must be enabled on your Paddle account.

            image_url: Optional[str] = None
                The image URL of the product.

            custom_data: Optional[Dict[str, Any]] = None
                Arbitrary data you can store with this product.

            status: Optional[Literal["active", "archived"]] = None
                Whether this entity can be used in Paddle.

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
            raise create_paddle_error(e.status_code, e.message) from e


class Product(ProductBase):
    """Resource for Paddle Products API endpoints."""

    def __init__(self, client: Client):
        super().__init__(client)

    def _list(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to list products."""
        return self._client._request(
            method="GET",
            path="/products",
            params=kwargs,
        )

    def _create(self, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to create a product."""
        return self._client._request(
            method="POST",
            path="/products",
            json=kwargs,
        )

    def _get(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to get a product."""
        return self._client._request(
            method="GET",
            path=f"/products/{product_id}",
            params=kwargs,
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

    async def _get(self, product_id: str, **query_params: Any) -> Dict[str, Any]:
        """Internal method to get a product."""
        return await self._client._request(
            method="GET",
            path=f"/products/{product_id}",
            params=query_params,
        )

    async def _update(self, product_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Internal method to update a product."""
        return await self._client._request(
            method="PATCH",
            path=f"/products/{product_id}",
            json=kwargs,
        )

    async def list(
        self,
        *,
        after: Optional[str] = None,
        id: Optional[List[str]] = None,
        include: Optional[List[Literal["prices"]]] = None,
        order_by: Optional[
            Literal[
                "created_at[ASC]",
                "created_at[DESC]",
                "updated_at[ASC]",
                "updated_at[DESC]",
                "custom_data[ASC]",
                "custom_data[DESC]",
                "description[ASC]",
                "description[DESC]",
                "id[ASC]",
                "id[DESC]",
                "image_url[ASC]",
                "image_url[DESC]",
                "name[ASC]",
                "name[DESC]",
                "status[ASC]",
                "status[DESC]",
                "tax_category[ASC]",
                "tax_category[DESC]",
            ]
        ] = None,
        per_page: Optional[Annotated[int, Field(ge=1, le=200)]] = 50,
        status: Optional[List[Literal["active", "archived"]]] = None,
        tax_category: Optional[List[TAX_CATEGORY]] = None,
        type: Optional[Literal["custom", "standard"]] = None,
    ) -> ProductListResponse:
        """|coroutine|

        Get all products.

        Parameters
        ----------

            after: Optional[str] = None
                Return entities after the specified Paddle ID when working with paginated endpoints.

            id: Optional[List[str]] = None
                Return only the IDs specified.

            include: Optional[List[Literal["prices"]]] = None
                Include related entities in the response.

            order_by: Optional[Literal[str]] = None
                Order returned entities by the specified field and direction ([ASC] or [DESC]).

            per_page: Optional[int] = 50
                Set how many entities are returned per page.
                Default: 50; Maximum: 200.

            status: Optional[List[Literal["active", "archived"]]] = None
                Return entities that match the specified status. Use a comma-separated list to specify multiple status values.

            tax_category: Optional[List[TAX_CATEGORY]] = None
                Return entities that match the specified tax category. Use a comma-separated list to specify multiple tax categories.

            type: Optional[Literal["custom", "standard"]] = None
                Return items that match the specified type.

        Returns
        -------

            A list of products.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the product is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    products = await client.products.list()
                    print(products)

            asyncio.run(main())
        """
        try:
            kwargs = filter_none_kwargs(
                after=after,
                id=",".join(id) if id else None,
                include=",".join(include) if include else None,
                order_by=order_by,
                per_page=per_page,
                status=",".join(status) if status else None,
                tax_category=",".join(tax_category) if tax_category else None,
                type=type,
            )
            response = await self._list(**kwargs)

            return ProductListResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
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

        Parameters
        ----------

            name: str
                The name of the product.

            tax_category: TAX_CATEGORY
                Tax category for this product. Used for charging the correct rate of tax. Selected tax category must be enabled on your Paddle account.

            description: Optional[str] = None
                Short description for this product.

            type: Optional[Literal["custom", "standard"]] = None
                The type of the product.

            image_url: Optional[str] = None
                The image URL of the product.

            custom_data: Optional[Dict[str, Any]] = None
                Arbitrary data you can store with this product.

        Returns
        -------

            A new product.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleValidationError: If the product is not valid.

        Example
        -------- ::

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
            raise create_paddle_error(e.status_code, e.message) from e

    @validate_params
    async def get(
        self,
        product_id: str,
        *,
        include: Optional[List[Literal["prices"]]] = None,
    ) -> ProductGetResponse:
        """|coroutine|

        Gets a product by ID.

        Parameters
        ----------

            product_id: The ID of the product to get.

            include: Optional[List[Literal["prices"]]] = None
                Include related entities in the response.

        Returns
        -------

            A product by ID.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleNotFoundError: If the product is not found.

        Example
        -------- ::

            import asyncio
            from paddle.aio import AsyncClient

            async def main():
                async with AsyncClient(api_key="your_api_key") as client:
                    product = await client.products.get("pro_1234567890")
                    print(product)

            asyncio.run(main())
        """
        try:
            response = await self._get(product_id, include=",".join(include) if include else None)
            return ProductGetResponse(response)
        except PaddleAPIError as e:
            raise create_paddle_error(e.status_code, e.message) from e

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

        Parameters
        ----------

            name: Optional[str] = None
                The name of the product.

            description: Optional[str] = None
                Short description for this product.

            type: Optional[Literal["custom", "standard"]] = None
                The type of the product.

            tax_category: Optional[TAX_CATEGORY] = None
                Tax category for this product. Used for charging the correct rate of tax. Selected tax category must be enabled on your Paddle account.

            image_url: Optional[str] = None
                The image URL of the product.

            custom_data: Optional[Dict[str, Any]] = None
                Arbitrary data you can store with this product.

            status: Optional[Literal["active", "archived"]] = None
                Whether this entity can be used in Paddle.

        Returns
        -------

            Updated product.

        Raises
        ------

            PaddleAPIError: If the API request fails.
            PaddleValidationError: If the product is not valid.

        Example
        -------- ::

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
            raise create_paddle_error(e.status_code, e.message) from e
