#!/usr/bin/env python

version = '0.4.2'

import os
import sys

from setuptools import setup
from setuptools.command.test import test


if sys.argv[-1] == 'publish':
    os.system('python setup.py register sdist bdist_wheel upload')
    sys.exit()


packages = [
    'readonly',
]

requires = [
]


class mytest(test):
    def run(self, *args, **kwargs):
        from runtests import runtests
        runtests()
        # Upgrade().run(dist=True)
        # test.run(self, *args, **kwargs)

setup(
    name='django-db-readonly',
    version=version,
    author='Chris Streeter',
    author_email='pypi@chrisstreeter.com',
    url='http://github.com/streeter/django-db-readonly',
    description='Add a global database read-only setting.',
    long_description=open('README.rst').read(),
    packages=packages,
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    test_suite='readonly.tests',
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
)
