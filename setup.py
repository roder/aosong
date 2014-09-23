#!/usr/bin/env python
from setuptools import setup, find_packages
import os

def contents_of(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return 'Error loading long_description'

package = 'aosong'

setup(name='aosong',
      version="0.0.1",
      description='AOSONG Sensors.',
      long_description=contents_of('README.md'),
      author='Sopwith',
      author_email='sopwith@ismesllsmoke.net',
      maintainer='Matt Heitzenroder',
      maintainer_email='mheitzenroder@gmail.com',
      url='http://sopwith.ismellsmoke.net/?p=104',
      license="Apache-2.0",
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
      ],
      install_requires=['quick2wire-api>=0.0.0.2'],
      dependency_links=['http://github.com/quick2wire/quick2wire-python-api/tarball/master#egg=quick2wire-api-0.0.0.2'],
      platforms=['Linux'],
      packages=find_packages(),
      test_suite="tests"
      
)

