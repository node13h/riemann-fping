#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(
    name='riemann-fping',

    version=version,

    description='Ping data collector for RIEMANN',
    long_description=long_description,

    url='https://github.com/node13h/riemann-fping',

    author='Sergej Alikov',
    author_email='sergej.alikov@gmail.com',

    license='GPL-3.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],

    keywords='riemann ping fping',

    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    # See https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'riemann-client',
    ],

    entry_points={
        'console_scripts': [
            'riemann-fping = riemann_fping.riemann_fping:main',
        ],
    }
)
