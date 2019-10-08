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
#	  themes/__init__.py
#

from pagebot.themes.basetheme import BaseTheme
from pagebot.themes.backtothecity import BackToTheCity
from pagebot.themes.businessasusual import BusinessAsUsual
from pagebot.themes.fairytales import FairyTales
from pagebot.themes.freshandshiny import FreshAndShiny
from pagebot.themes.intothewoods import IntoTheWoods
from pagebot.themes.seasoningthedish import SeasoningTheDish
from pagebot.themes.somethingintheair import SomethingInTheAir
from pagebot.themes.wordlywise import WordlyWise
from pagebot.themes.happyholidays import HappyHolidays

ThemeClasses = {}

for themeClass in (
    BaseTheme,
    BackToTheCity, 
    BusinessAsUsual, 
    FairyTales, 
    FreshAndShiny, 
    IntoTheWoods, 
    SeasoningTheDish, 
    SomethingInTheAir, 
    WordlyWise,
    HappyHolidays):
        ThemeClasses[themeClass.NAME] = themeClass

DEFAULT_THEME_CLASS = FreshAndShiny

