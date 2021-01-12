#!/usr/bin/env python3

from setuptools import setup

setup(
    name='reclada.extractor',
    description='Dict Extractor step for Reclada Parser',
    version='0.1',
    packages=['reclada.extractor', 'reclada.extractor.dicts'],
    install_requires=[
        'reclada.connector',
        'pyahocorasick',
        'dataclasses;python_version<"3.7"',
    ],
    entry_points={
        'console_scripts': ['reclada-dicts-extractor=reclada.extractor.dicts.main:main'],
    },
    python_requires='>=3.6',
)
