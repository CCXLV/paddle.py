__all__ = ["Environment"]


class Production:
    base_url = "https://api.paddle.com"


class Sandbox:
    base_url = "https://sandbox-api.paddle.com"


class Environment:
    """Environment for Paddle API."""

    PRODUCTION = Production
    SANDBOX = Sandbox
