#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name="ttgen",
    use_scm_version=True,
    author="Alexandre Andrade",
    author_email="kaniabi@gmail.com",
    url="https://github.com/kaniabi/tabletop_generator",
    description="Generate tabletop workshop mods from simple, pure-text, versionable DSL.",
    long_description="",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="development environment, shell, operations",
    include_package_data=True,
    packages=["ttgen"],
    install_requires=[],
    setup_requires=["setuptools_scm"],
    tests_require=[],
    license="MIT license",
    entry_points="""
    [zops.plugins]
    main=ttgen.cli:main
""",
)
