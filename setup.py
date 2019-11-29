# -*- coding: utf-8 -*-
import os
import sys
from codecs import open
from setuptools import setup

sys.path[0:0] = ['phantomjs']

from version import __version__

def get_readme(filename):
    content = ""
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as readme:
            content = readme.read()
    except Exception as e:
        pass
    return content

setup(name="phantomjs",
      version=__version__,
      author="Md. Jahidul Hamid",
      author_email="jahidulhamid@yahoo.com",
      description="Python Markdown extension to include local or remote files",
      license="BSD",
      keywords="markdown include local remote file",
      url="https://github.com/neurobin/phantomjs",
      packages=["phantomjs"],
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
        'Programming Language :: Python :: 3',
      ],
      install_requires=[],
test_suite="phantomjs.testio")
