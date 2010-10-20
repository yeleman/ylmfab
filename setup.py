#!/usr/bin/env python
# encoding=utf-8
# maintainer: rgaudin

import setuptools

setuptools.setup(
    name='ylmfab',
    version=__import__('ylmfab').__version__,
    license = 'GNU Lesser General Public License (LGPL), Version 3',

    install_requires = ['Fabric>=0.9.2'],
    provides = ['ylmfab'],

    description='fabfile helper.',
    long_description=open('README.rst').read(),

    url='http://github.com/yeleman/ylmfab',

    packages=['ylmfab'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python',
    ],
)
