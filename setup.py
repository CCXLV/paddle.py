import re

from setuptools import setup


def get_version():
    with open("paddle/__init__.py") as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")


setup(version=get_version())
