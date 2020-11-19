#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
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
#     filepaths.py
#
#
import os
import os.path
from sys import platform

HOME = os.path.expanduser('~')

# Various paths where system fonts are installed.
ROOT_FONT_PATHS = {'darwin': ['/System/Library/Fonts', '/Library/Fonts',
    '%s/Library/Fonts' % HOME], 'linux': ['/usr/share/fonts/',
        '%s/.local/share/fonts/' % HOME, '/usr/local/share/fonts']}

# NOTE: should stay at root level, else derived path won't be correct. Also
# note that these are file paths, not to be mixed up with BezierPath and
# DrawBotContext.BezierPath, which are "recorded" drawing instructions.
ROOT_PATH = '/'.join(__file__.split('/')[:-1])
BASE_PATH = os.path.abspath('.')

def getRootPath():
    """Answers the root path of the PageBot module for the current platform."""
    return ROOT_PATH

def getResourcesPath():
    # First check inside PageBot package.
    path = '%s/%s' % (ROOT_PATH, 'resources')

    if os.path.exists(path):
        return path

    # Check base in case of separate resources folder (Py2app).
    path = '%s/%s' % (BASE_PATH, 'resources')
    return path

def getExportPath():
    if os.path.exists(ROOT_PATH):
        path = '%s/%s' % (ROOT_PATH, '_export')
    else:
        # Check base in case of separate resources folder (Py2app).
        path = '%s/%s' % (BASE_PATH, '_export')

    if not os.path.exists(path):
        os.mkdir(path)

    return path

def getMampPath():
    return getContextMampPath()

def getContextMampPath():
    """Make sure MAMP_PATH is initialized depending on the context."""
    MAMP_PATH = None

    if platform == 'darwin':
        MAMP_PATH = '/Applications/MAMP/htdocs/'

    elif platform == 'linux':
        # TODO: implement connection to LAMP:
        # https://help.ubuntu.com/community/ApacheMySQLPHP
        MAMP_PATH = '/tmp/LAMP/'
    else:
        raise NotImplementedError

    return MAMP_PATH

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
