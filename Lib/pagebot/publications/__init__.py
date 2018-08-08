# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     __init__.py
#
#	  from pagebot.publications import Magazine, Specimen
#
#     class FashionMagazine(Magazine):
#         pass
#
#	  fm = FashionMagazine('myFile.md')
#     fm.export('MyMagazine.pdf')
#
#     class MyVariableSpecimen(Specimen):
#		  pass
#
#     fm = FashionMagazine('myDataMarkDown.md')
#     fm.export('MySpeciment.pdf')
#
from book import Book
from website import Website
from poster import Poster
from brochure.brochure import Brochure
from newspaper.newspaper import Newspaper

