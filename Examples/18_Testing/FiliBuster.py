#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Example written by Frederik Berlaen
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testFiliBusterArticle.py
#
from pagebot.contributions.filibuster.blurb import Blurb

NO_TAGS = True # Flag to show/hide HTML tags in output

blurb = Blurb()

print(blurb.getBlurb('news_headline', noTags=NO_TAGS)+'\n')
print(blurb.getBlurb('article_ankeiler', noTags=NO_TAGS)+'\n')
print(blurb.getBlurb('article_summary', noTags=NO_TAGS)+'\n')
print(blurb.getBlurb('article', noTags=NO_TAGS)+'\n')
