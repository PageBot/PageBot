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
#     01_SpecimenApp.py
#
from pagebot import getResourcesPath
from pagebot.apps.specimenapp import SpecimenApp

fontPath = getResourcesPath() + '/testfonts/fontbureau'
app = SpecimenApp(fontPath)
