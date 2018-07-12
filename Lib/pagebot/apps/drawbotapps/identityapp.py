# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     identityapp.py
#
from pagebot.apps.drawbotapps.baseapp import BaseApp
from pagebot.publications.identity import Identity

class IdentityApp(BaseApp):
    u"""Will be developed."""
    PUBLICATION_CLASS = Identity

if __name__ == '__main__':
    app = IdentityApp()
    app.build()

