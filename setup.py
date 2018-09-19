# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='bitoolbox',
    version='0.3.2',
    author='Thiago MadPin',
    author_email='thiago.pinto@catho.com',
    description="A toolbox for BI purpouses",
    packages=[
        'bitoolbox',
        'bitoolbox.dbtools',
        'bitoolbox.datetools',
        'bitoolbox.pogtools',
        'bitoolbox.omnitools',
        'bitoolbox.pdutils',
        'bitoolbox.birsttools',
        'bitoolbox.platformtools',
        'bitoolbox.logtools',
        'bitoolbox.tracksaletools',
    ],
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    install_requires=[
        # 'pandas',
        # 'configparser>=3.3.0.post2',
        # 'pandas>=0.17.0',
        # 'PyYAML>=3.11'
    ])
