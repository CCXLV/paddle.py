from typing import Protocol

from paddle.client import BaseClient


class ResourceBase(Protocol):
    """Base protocol for all resources."""

    def __init__(self, client: BaseClient):
        self._client = client
