#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#    01_Dependencies.py
#

import sys, os

print('System: %s, %s' % (os.name, sys.platform))
print('Python version is:')
print(sys.version)
print('Python executable: %s' % sys.executable)

CLEAN = True

print('\nChecking installation paths... \n')

try:
    # Note: inside DrawBot site.pyc needs to be removed from root level.
    import site
    print('Found site at %s' % site.__file__)
    packages = site.getsitepackages()
    for p in packages:
        print(' - %s' % p)
except:
    print('x Could not read site packages :S')

# TODO: add svgwrite, flat, markdown etc?
# TODO automate, eval()?

if sys.platform == 'darwin':
    required = ['pagebot', 'fontTools', 'objc', 'AppKit', 'vanilla', 'drawBot', 'sass']
    optional = ['flat', 'simple_idml']
else:
    required = ['pagebot', 'fontTools', 'sass', 'flat']
    optional = ['simple_idml']

missing = []

for l in required:
    try:
        __import__(l)
        print('Required dependency %s installed at %s' % (l, __import__(l).__file__))
    except:
        print('Required dependency x %s not installed' % l)
        missing.append(l)
        CLEAN = False

for l in optional:
    try:
        __import__(l)
        print('Optional dependency %s installed at %s' % (l, __import__(l).__file__))
    except:
        print('Optional dependency x %s not installed' % l)
        missing.append(l)

if not CLEAN:
    print('Not all dependencies are installed, please install missing ones:')
    print(', '.join(missing))
else:
    print('Found all dependencies, running some test...')

    # Testing PageBot context.
    from pagebot import getContext
    context = getContext()
    print('The default PageBot context is %s' % context)
    print('The default builder module is %s' % context.b)
