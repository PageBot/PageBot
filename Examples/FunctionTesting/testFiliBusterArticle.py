#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting usage of DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFiliBusterArticle.py
#
from pagebot.contributions.filibuster.blurb import Blurb

NO_TAGS = True # Flag to show/hide HTML tags in output

w = Blurb()

print w.getBlurb('article_ankeiler', noTags=NO_TAGS)
print
print w.getBlurb('article_summary', noTags=NO_TAGS)
print
print w.getBlurb('article', noTags=NO_TAGS)
