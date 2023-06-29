from setuptools import setup, find_packages

setup(
    name="aiodanbooru",
    version="1.0.0",
    description="A Python library for interacting with the Danbooru API",
    author="lrdcxdes",
    author_email="lordgrief176@email.com",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "aiohttp",
        "pydantic",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    project_urls={
        "Source": "https://github.com/lrdcxdes/aiodanbooru",
    },
    long_description=open("README.md").read(),
)
