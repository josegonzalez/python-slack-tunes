#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from slack_tunes import __version__

try:
    from setuptools import setup

    setup  # workaround for pyflakes issue #13
except ImportError:
    from distutils.core import setup

# Hack to prevent stupid TypeError: 'NoneType' object is not callable error on
# exit of python setup.py test # in multiprocessing/util.py _exit_function when
# running python setup.py test (see
# http://www.eby-sarna.com/pipermail/peak/2010-May/003357.html)
try:
    import multiprocessing

    multiprocessing
except ImportError:
    pass


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


setup(
    name="slack-tunes",
    version=__version__,
    author="Jose Diaz-Gonzalez",
    author_email="slack-tunes@josediazgonzalez.com",
    packages=["slack_tunes"],
    scripts=["bin/slack-tunes"],
    url="http://github.com/josegonzalez/python-slack-tunes",
    license=open("LICENSE.txt").read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Archiving :: Backup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    description="send slack music notifications from spotify",
    long_description=open_file("README.rst").read(),
    install_requires=open_file("requirements.txt").readlines(),
    zip_safe=True,
)
