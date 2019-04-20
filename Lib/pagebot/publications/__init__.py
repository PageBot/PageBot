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
#     Publications, e.g. Book and Magazine
#     These are technically elements, with all their behavior, but typically
#     they are not placed in a layout. Instead they contain a set of pages,
#     that get transfered to a new created Document during composition.
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
from pagebot.publications.web.nanosite import BaseSite
from pagebot.publications.web.nanosite import NanoSite
from pagebot.publications.ad.ad import Ad
from pagebot.publications.book import Book
from pagebot.publications.poster import Poster
from pagebot.publications.catalog import Catalog
from pagebot.publications.identity import Identity
from pagebot.publications.portfolio.portfolio import Portfolio
from pagebot.publications.brochure.brochure import Brochure
from pagebot.publications.magazine.magazine import Magazine
from pagebot.publications.typespecimen import TypeSpecimen

PublicationClasses = dict(
	Ad=Ad,
	Specimen=TypeSpecimen,
	Magazine=Magazine,
	Book=Book,
	Site=NanoSite,
	Identity=Identity,
	Portfolio=Portfolio,
	#Manual=Manual,
	Catalog=Catalog,
	Brochure=Brochure,
	Poster=Poster,
)