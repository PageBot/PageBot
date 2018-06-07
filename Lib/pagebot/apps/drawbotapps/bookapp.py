# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     bookapp.py
#
from pagebot.apps.drawbotapps.baseapp import BaseApp
from pagebot.publications.book import Book

class BookApp(BaseApp):
    """Will be developed."""
    PUBLICATION_CLASS = Book

if __name__ == '__main__':
    app = BookApp()
    app.build()
    
    
