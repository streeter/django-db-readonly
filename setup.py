#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="django-db-readonly",
    version="0.7.0",
    description="Add a global database read-only setting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="django database readonly",
    author="Chris Streeter",
    author_email="pypi@chrisstreeter.com",
    url="https://github.com/streeter/django-db-readonly",
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["readonly"],
    package_dir={"readonly": "readonly"},
    install_requires=["Django>=1.9"],
    extras_require={"test": ["pytest", "pytest-django", "flake8"]},
    tests_require=["readonly[test]"],
)
