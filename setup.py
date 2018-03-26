# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages

VERSION = (1, 0, 0)
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'aws_switchrole_links',
    description = "Generate links for switching role in AWS console",
    license="Apache License, Version 2.0",
    url = "https://github.com/teekaay/aws-switchrole-links",
    long_description = io.open('README.md', 'r', encoding='utf-8').read(),
    platform='any',
    zip_safe=False,
    version = __versionstr__,
    author = "Thomas Klinger",
    author_email = "thomas.klinger@protonmail.com",
    packages=find_packages(exclude=('test*', )),
    classifiers = [
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    include_package_data=True,
    install_requires=[
        'jmespath'
    ],
    entry_points = {
        'console_scripts': [
            'aws-switchrole-links = aws_switchrole_links.__main__:main']
    },
    keywords='aws aws-console'
)
