#!/usr/bin/env python3

from setuptools import setup

setup(
    name='reclada.dicts_extractor',
    description='Dict Extractor step for Reclada Parser',
    version='0.1',
    packages=['reclada.dicts_extractor'],
    install_requires=[
        'reclada.connector',
        'pyahocorasick',
        'dataclasses;python_version<"3.7"',
    ],
    entry_points = {
        'console_scripts': ['reclada-dicts-extractor=reclada.dicts_extractor.main:main'],
    },
    python_requires='>=3.6',
)
