#!/bin/env python

# Import setup from setuptools to do setup.
from setuptools import setup

# Use that to set it up.
setup(
        name='WordCloudGenerator',
        license='MIT(?)',
        version='1.0.5',
        description='A tool to generate a word-cloud for a given issue.',
        author='Chris Johnson',
        url="https://crisistrends.org",
        packages=['WordCloudGenerator'],
        install_requires=[''],
        scripts=['scripts/generate']
        )

