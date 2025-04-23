import pytest
from typing import Optional
from pydantic import ValidationError

from paddle.utils.decorators import validate_params


class TestClass:
    @validate_params
    def sync_method(self, name: str, age: int, email: Optional[str] = None):
        return {"name": name, "age": age, "email": email}

    @validate_params
    async def async_method(self, name: str, age: int, email: Optional[str] = None):
        return {"name": name, "age": age, "email": email}


def test_sync_method_valid_params():
    test_obj = TestClass()
    with pytest.raises(ValidationError):
        test_obj.sync_method(name="John", age="thirty")


def test_sync_method_with_optional_param():
    test_obj = TestClass()
    result = test_obj.sync_method(name="John", age=30, email="john@example.com")
    assert result == {"name": "John", "age": 30, "email": "john@example.com"}


def test_sync_method_invalid_params():
    test_obj = TestClass()
    with pytest.raises(ValidationError):
        test_obj.sync_method(name="John", age="thirty")  # age should be int


@pytest.mark.asyncio
async def test_async_method_valid_params():
    test_obj = TestClass()
    result = await test_obj.async_method(name="John", age=30, email="john@example.com")
    assert result == {"name": "John", "age": 30, "email": "john@example.com"}


@pytest.mark.asyncio
async def test_async_method_with_optional_param():
    test_obj = TestClass()
    result = await test_obj.async_method(name="John", age=30, email="john@example.com")
    assert result == {"name": "John", "age": 30, "email": "john@example.com"}


@pytest.mark.asyncio
async def test_async_method_invalid_params():
    test_obj = TestClass()
    with pytest.raises(ValidationError):
        await test_obj.async_method(name="John", age="thirty")  # age should be int


def test_missing_required_params():
    test_obj = TestClass()
    with pytest.raises(ValidationError):
        test_obj.sync_method(name="John")  # missing required age param


@pytest.mark.asyncio
async def test_async_missing_required_params():
    test_obj = TestClass()
    with pytest.raises(ValidationError):
        await test_obj.async_method(name="John")  # missing required age param


def test_validate_params_with_optional_params():
    @validate_params
    def function(name: str, age: int, email: Optional[str]):
        return {"name": name, "age": age, "email": email}

    result = function(name="John", age=30, email="john@example.com")
    assert result == {"name": "John", "age": 30, "email": "john@example.com"}


@pytest.mark.asyncio
async def test_validate_params_with_function_decorator():
    @validate_params
    async def function(name: str, age: int, email: Optional[str] = None):
        return {"name": name, "age": age, "email": email}

    result = await function(name="John", age=30, email="john@example.com")
    assert result == {"name": "John", "age": 30, "email": "john@example.com"}


@pytest.mark.asyncio
async def test_validate_params_with_class_method_decorator():
    class TestClass:
        @validate_params
        async def async_method(self, name: str, age: int, email: Optional[str] = None):
            return {"name": name, "age": age, "email": email}

    test_obj = TestClass()
    result = await test_obj.async_method(name="John", age=30, email="john@example.com")
    assert result == {"name": "John", "age": 30, "email": "john@example.com"}


@pytest.mark.asyncio
async def test_async_wrapper_error_handling():
    @validate_params
    async def async_function(name: str, age: int):
        return {"name": name, "age": age}

    with pytest.raises(ValidationError) as exc_info:
        await async_function(name="John", age="thirty")
    assert exc_info.value.error_count() == 1
    assert "age" in str(exc_info.value)


def test_sync_wrapper_error_handling():
    @validate_params
    def sync_function(name: str, age: int):
        return {"name": name, "age": age}

    with pytest.raises(ValidationError) as exc_info:
        sync_function(name="John", age="thirty")
    assert exc_info.value.error_count() == 1
    assert "age" in str(exc_info.value)
