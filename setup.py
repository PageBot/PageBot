#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     setup.py

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pagebot',
    #use_scm_version=True,
    version='1.0.2',
    description='Scripted page layout framework for Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/PageBot/PageBot",
    author = 'Petr van Blokland, Michiel Kauw-A-Tjoe, Felipe Sanches, Dave Crossland',
    author_email = 'r@petr.com',
    package_dir={'': 'Lib'},
    packages=find_packages('Lib'),
    include_package_data=True,
    package_data={'': ['*.txt', '*.md', '*.ttf', '*.png', '*.pdf', '*.jpg',
        '*.designspace', '*.scss', '*.css', '*.js', '*.idml', '*.indd',
        '*.html', '*.xml', '*.sketch']},
    setup_requires=['fontTools'],
    license = 'MIT',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Artistic Software',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Graphics :: Editors',
        'Topic :: Multimedia :: Graphics :: Editors :: Raster-Based',
        'Topic :: Multimedia :: Graphics :: Editors :: Vector-Based',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Multimedia :: Graphics :: Viewers',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Fonts'],
    install_requires=[
        'booleanOperations',
        #'flat',
        'fontTools',
        'libsass',
        'markdown',
        'Pillow',
        'svgwrite',
        'tornado',]
    )
