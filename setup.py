#!/usr/bin/env python

import sys
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(name='youtube_alexa_python',
      version='1.2.6',
      description='youtube for alexa',
      long_description=README,
      author='andrewstech',
      author_email='hello@andrewstech.ne',
      url='https://github.com/unofficial-skills/youtube-alexa-python',
      py_modules=['youtube_alexa_python'],
      scripts=['main.py'],
      license='Apache License, Version 2.0',
      install_requires=['youtube_dl'],
     )
