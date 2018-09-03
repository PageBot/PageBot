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

setup(
    name='pagebot',
    url="https://github.com/TypeNetwork/PageBot",
    version='0.6',
    package_dir={'': 'Lib'},
    packages=find_packages('Lib'),
    include_package_data=True,
    package_data={'': ['*.txt', '*.md', '*.ttf']}
)
