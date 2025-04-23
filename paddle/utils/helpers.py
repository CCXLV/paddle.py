from typing import Dict, Any


def filter_none_kwargs(**kwargs: Any) -> Dict[str, Any]:
    """
    Filter out None values from keyword arguments.

    Args:
        **kwargs: Any keyword arguments to filter

    Returns:
        Dict[str, Any]: Dictionary containing only non-None values

    Examples:
        >>> filter_none_kwargs(name="test", description=None, price=10)
        {'name': 'test', 'price': 10}
    """
    return {k: v for k, v in kwargs.items() if v is not None}
