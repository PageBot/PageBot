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
    description='Scripted page layout framework for Python.',
    url="https://github.com/PageBot/PageBot",
    author = 'Petr van Blokland, Michiel Kauw-A-Tjoe, Felipe Sanchez, Dave Crossland',
    author_email = 'r@petr.com',
    version='0.6',
    package_dir={'': 'Lib'},
    packages=find_packages('Lib'),
    include_package_data=True,
    package_data={'': ['*.txt', '*.md', '*.ttf', '*.png', '*.pdf', '*.jpg',
        '*.designspace', '*.scss', '*.css', '*.js', '*.idml', '*.indd',
        '*.html', '*.xml']},
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
    install_requires=['libsass', 'fontTools']
)
