#!/usr/bin/env python
from setuptools import setup

requires = [
    'Django==1.4',
#    'psycopg2==2.4.5',
    'Jinja2==2.6',
    'Coffin==0.3.6',
    'Fabric==1.4.2',
]

setup(
    name='seahobo',
    version='1.0',
    description='seahobo description',
    author='Greg Reinbach',
    author_email='greg@reinbach.com',
    url='https://github.com/reinbach/seahobo',
    install_requires=requires,
)