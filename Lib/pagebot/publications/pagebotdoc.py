#!/usr/bin/env python
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
#     pagebotdoc.py
#
#     Generic Type Specimen Publiction. Use straight, if the default behavior
#     and templates are hood enough. Inherit the redefine functions otherwise.
#     Example of an inherited publications is FBFamilySpecimen.py
#
from pagebot.fonttoolbox.objects.family import Family
from pagebot.fonttoolbox.objects.font import Font
from pagebot.publications.publication import Publication


class PageBotDoc(Publication):

    MIN_STYLES = 4 # Don't show, if families have fewer amount of style.

    FONT_CLASS = Font
    FAMILY_CLASS = Family

    def __init__(self):
        Publication.__init__(self)

