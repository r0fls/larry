"""
Sanic
"""
import codecs
import os
import re
from setuptools import setup

setup(
    name='Larry',
    version='0.0.3',
    url='http://github.com/r0fls/larry/',
    license='MIT',
    author='Raphael Deem',
    author_email='raphael.deem@gmail.com',
    description='Caching library',
    packages=['larry'],
    platforms='any',
    install_requires=[
        'redis',
        'fakeredis',
        'dill',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
