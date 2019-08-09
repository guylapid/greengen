from setuptools import setup, find_packages

setup(
    name='greengen',
    version='1.0',
    packages=find_packages(),
    author='user',
    description='',
    install_requires=[
        'greenlet',
        'decorator',
    ],
)
