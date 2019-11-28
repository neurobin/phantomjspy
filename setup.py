# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
from codecs import open
from setuptools import setup

sys.path[0:0] = ['phantomjspy']

from version import __version__

def get_readme(filename):
    content = ""
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as readme:
            content = readme.read()
    except Exception as e:
        pass
    return content

setup(name="phantomjspy",
      version=__version__,
      author="Md. Jahidul Hamid",
      author_email="jahidulhamid@yahoo.com",
      description="Python Markdown extension to include local or remote files",
      license="BSD",
      keywords="markdown include local remote file",
      url="https://github.com/neurobin/phantomjspy",
      packages=["phantomjspy"],
      long_description=get_readme("README.md"),
      long_description_content_type="text/markdown",
      classifiers=[
        # See: https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup',
      ],
      install_requires=[],
test_suite="phantomjspy.test.test")
