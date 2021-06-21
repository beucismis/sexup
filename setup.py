import sys
import backupill as bp
from setuptools import setup


if sys.version_info < (3, 5):
    raise RuntimeError("backupill requires Python 3.5 or later")

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requires = f.read().splitlines()

setup(
    name="backupill",
    packages=["backupill"],
    version=bp.__version__,
    description=bp.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=bp.__source__,
    author=bp.__author__,
    author_email=bp.__contact__,
    license=bp.__license__,
    classifiers=[],
    platforms=["Linux"],
    python_requires=">=3.5",
    install_requires=requires,
    keywords=[],
    entry_points={
        "console_scripts": [
            "backupill = backupill.cli:main",
        ],
    },
)
