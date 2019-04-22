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
#     books/__init__.py
#
from pagebot.publications.books.literature import Literature
from pagebot.publications.books.photobook import PhotoBook

BOOK_CLASSES = {
	'Literature': Literature, # Single column
	#'Multilingual': Multilingual,
	'Photo book': PhotoBook,
	#'Poetry': Poetry
	#'Children book', ChildrenBook
	#'Study book': StudyBook,
}

if __name__ == "__main__":
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
