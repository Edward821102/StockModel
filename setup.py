# coding=utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setuptools.setup(
    name="stock_model",
    version="0.0.1",
    packages=setuptools.find_packages(),
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.10.0",
    install_requires=[
                    "line-bot-sdk",
                    "twstock"
                     ]
)