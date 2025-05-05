import asyncio
import inspect

from functools import wraps
from typing import TypeVar, Callable, get_type_hints, cast, get_origin, get_args, Union

from pydantic import ValidationError, create_model

T = TypeVar("T", bound=Callable)


def validate_params(func: T) -> T:
    """
    Decorator that validates function parameters using Pydantic.
    Works with both synchronous and asynchronous functions.
    Properly handles optional parameters and default values.
    """
    # Get type hints and function signature
    hints = get_type_hints(func)
    sig = inspect.signature(func)

    # Remove return annotation if present
    hints.pop("return", None)

    # Check if the function is a method
    is_method = any(param.name == "self" for param in sig.parameters.values())

    # Create field definitions with proper defaults
    fields = {}
    for name, param in sig.parameters.items():
        # Skip 'self' parameter for methods
        if name == "self":
            continue

        if name in hints:
            # Determine if the parameter is optional
            is_optional = False
            annotation = hints[name]

            # Check if it's an Optional type (Union[Type, None])
            if get_origin(annotation) is Union and type(None) in get_args(annotation):
                is_optional = True

            # Check if it has a default value
            has_default = param.default is not param.empty

            if has_default:
                # Use the actual default value
                fields[name] = (annotation, param.default)
            elif is_optional:
                # For Optional types without defaults, use None
                fields[name] = (annotation, None)
            else:
                # Required field
                fields[name] = (annotation, ...)

    # Create validation model
    ValidatorModel = create_model(f"{func.__name__}Validator", **fields)

    # Check if the function is async
    is_async = asyncio.iscoroutinefunction(func)

    if is_async:
        if is_method:

            @wraps(func)
            async def async_method_wrapper(self, *args, **kwargs):
                try:
                    # Get the parameter names from the signature
                    param_names = list(sig.parameters.keys())
                    if is_method:
                        param_names.remove("self")

                    # Create a dict of all arguments
                    all_args = {}
                    for i, arg in enumerate(args):
                        all_args[param_names[i]] = arg
                    all_args.update(kwargs)

                    ValidatorModel(**all_args)
                    return await func(self, *args, **kwargs)
                except ValidationError as e:
                    print(f"Validation error in {func.__name__}: {e}")
                    raise

            return cast(T, async_method_wrapper)
        else:

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    # Get the parameter names from the signature
                    param_names = list(sig.parameters.keys())

                    # Create a dict of all arguments
                    all_args = {}
                    for i, arg in enumerate(args):
                        all_args[param_names[i]] = arg
                    all_args.update(kwargs)

                    ValidatorModel(**all_args)
                    return await func(*args, **kwargs)
                except ValidationError as e:
                    print(f"Validation error in {func.__name__}: {e}")
                    raise

            return cast(T, async_wrapper)
    else:
        if is_method:

            @wraps(func)
            def sync_method_wrapper(self, *args, **kwargs):
                try:
                    # Get the parameter names from the signature
                    param_names = list(sig.parameters.keys())
                    if is_method:
                        param_names.remove("self")

                    # Create a dict of all arguments
                    all_args = {}
                    for i, arg in enumerate(args):
                        all_args[param_names[i]] = arg
                    all_args.update(kwargs)

                    ValidatorModel(**all_args)
                    return func(self, *args, **kwargs)
                except ValidationError as e:
                    print(f"Validation error in {func.__name__}: {e}")
                    raise

            return cast(T, sync_method_wrapper)
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    # Get the parameter names from the signature
                    param_names = list(sig.parameters.keys())

                    # Create a dict of all arguments
                    all_args = {}
                    for i, arg in enumerate(args):
                        all_args[param_names[i]] = arg
                    all_args.update(kwargs)

                    ValidatorModel(**all_args)
                    return func(*args, **kwargs)
                except ValidationError as e:
                    print(f"Validation error in {func.__name__}: {e}")
                    raise

            return cast(T, sync_wrapper)
