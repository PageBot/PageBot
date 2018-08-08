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
#     Elements with behavior that works best as website output (e.g. because
#     they are animated or interactive). Yet, these elements can still be used
#     building in static output media, such as PDF or PNG.
#
from pagebot.elements.web.simplesite.header import Header
from pagebot.elements.web.simplesite.navigation import Navigation
from pagebot.elements.web.simplesite.banner import Banner
from pagebot.elements.web.simplesite.logo import Logo
from pagebot.elements.web.simplesite.introduction import Introduction
from pagebot.elements.web.simplesite.hero import Hero
from pagebot.elements.web.simplesite.featured import Featured
from pagebot.elements.web.simplesite.content import WideContent
from pagebot.elements.web.simplesite.footer import Footer
from pagebot.elements.web.simplesite.style_css import simpleTheme, simpleCssCode
