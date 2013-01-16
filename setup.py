#!/usr/bin/env python

version = '0.3.0'

try:
    from setuptools import setup, find_packages
    from setuptools.command.test import test
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
    from setuptools.command.test import test


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
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
    ],
    test_suite='readonly.tests',
    include_package_data=True,
    cmdclass={"test": mytest},
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development'
    ],
)
