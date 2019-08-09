import os
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = open(os.path.join(BASE_DIR, 'README.md')).read()

setup(
    name='greengen',
    version='1.0.1',
    description='Nesting generators using greenlets',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/guylapid/greengen",
    author='guylapid',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'greenlet',
        'decorator',
    ],
)
