#!/usr/bin/python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     runAllDocTests.py

# 
import pagebot
import pagebot.contexts
from pagebot.contexts.platform import getFontPaths
import pagebot.contexts.basecontext
import pagebot.contexts.drawbotcontext
import pagebot.contexts.flatcontext

print getFontPaths()