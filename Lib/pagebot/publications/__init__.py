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
from pagebot.publications.ads import AD_CLASSES
from pagebot.publications.books import BOOK_CLASSES
from pagebot.publications.brochures import BROCHURE_CLASSES
from pagebot.publications.calendars import CALENDAR_CLASSES
from pagebot.publications.catalogs import CATALOG_CLASSES
from pagebot.publications.identities import IDENTITY_CLASSES
from pagebot.publications.magazines import MAGAZINE_CLASSES
from pagebot.publications.manuals import MANUAL_CLASSES
from pagebot.publications.newspapers import NEWSPAPER_CLASSES
from pagebot.publications.portfolios import PORTFOLIO_CLASSES
from pagebot.publications.posters import POSTER_CLASSES
from pagebot.publications.typespecimens import TYPE_SPECIMEN_CLASSES
from pagebot.publications.websites import WEBSITE_CLASSES

PublicationCategories = dict(
	Ad=AD_CLASSES,
	Book=BOOK_CLASSES,
	Brochure=BROCHURE_CLASSES,
	Calendars=CALENDAR_CLASSES,
	Catalog=CATALOG_CLASSES,
	#Collection=COLLEDCTION_CLASSES,
	Identity=IDENTITY_CLASSES,
	Magazine=MAGAZINE_CLASSES,
	Manual=MANUAL_CLASSES,
	Newspaper=NEWSPAPER_CLASSES,
	#Newsletter=NEWSLETTER_CLASSES,
	#Paper=SCIENTIFIC_PAPER
	Portfolio=PORTFOLIO_CLASSES,
	Poster=POSTER_CLASSES,
	#Report=ANNUAL_REPORT_CLASSES,
	#Thesis=THESIS_CLASSES,
	TypeSpecimen=TYPE_SPECIMEN_CLASSES,
	Website=WEBSITE_CLASSES,
)
