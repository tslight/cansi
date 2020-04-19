# Copyright (c) 2018, Toby Slight. All rights reserved.
# ISC License (ISCL) - see LICENSE file for details.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cansi",
    version="0.0.2",
    author="Toby Slight",
    author_email="tslight@pm.me",
    description="Curses ANSI Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tslight/cansi",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ),
)
