import re

from setuptools import setup


def get_version():
    with open("paddle/__init__.py") as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


def get_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="paddle-sdk",
    description="A modern Python SDK for Paddle's API with type hints and async support",
    author="CCXLV",
    version=get_version(),
    packages=["paddle"],
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "setuptools",
            "black",
            "ruff",
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "pytest-asyncio",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    url="https://github.com/CCXLV/paddle-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/CCXLV/paddle-sdk/issues",
        "Source Code": "https://github.com/CCXLV/paddle-sdk",
    },
    keywords=["paddle", "api", "wrapper", "sdk", "async", "types"],
    license="MIT",
)
