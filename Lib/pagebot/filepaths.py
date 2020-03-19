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
#     paths.py
#
#
#    NOTE: should stay at root level, else derived path won't be correct.
#    Also note that these are file paths, not to be mixed up with
#    PageBotPath and DrawBotContext.BezierPath, which are "recorded"
#    drawing instructions.
#

from os.path import expanduser

HOME = expanduser('~')
ROOT_FONT_PATHS = {'darwin': ['/System/Library/Fonts', '/Library/Fonts',
    '%s/Library/Fonts' % HOME], 'linux': ['/usr/share/fonts/',
        '%s/.local/share/fonts/' % HOME, '/usr/local/share/fonts']}

ROOT_PATH = '/'.join(__file__.split('/')[:-1])
RESOURCES_PATH = ROOT_PATH + '/resources'
DEFAULT_FONT_NAME = 'PageBot-Regular'
DEFAULT_FONT_PATH = RESOURCES_PATH + '/testfonts/typetr/%s.ttf' % DEFAULT_FONT_NAME
