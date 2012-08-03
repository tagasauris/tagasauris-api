#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="tagapi",
    version="0.01",
    author="10clouds",
    author_email="10clouds@10couds.com",
    description="Tagasauris API client",
    license='MIT',
    url="http://github.com/10clouds/tagasauris-api",
    packages=find_packages(),
    install_requires=['requests', ],
    keywords="tagasauris api client",
    zip_safe=True)
