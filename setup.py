# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     setup.py

from setuptools import setup, find_packages

setup(
    name='pagebot',
     url="https://github.com/TypeNetwork/PageBot",
    version='0.1',
    packages=find_packages('Lib'),
    package_dir={'': 'Lib'},
    #entry_points={
    #    'console_scripts': [
    #        'pagebot = pagebot.__main__:main'
    #    ]
    #}
)
