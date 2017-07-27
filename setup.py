# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     setup.py

from setuptools import setup, find_packages

# TODO: Add download/install for markdown, if it does not exist.
# https://pypi.python.org/pypi/Markdown

# TODO: Add download/install for pyscss, if it does not exist.
# https://github.com/Kronuz/pyScss

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
