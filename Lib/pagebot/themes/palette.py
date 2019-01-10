#!/usr/bin/env python3
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
#     palette.py
#
from pagebot.toolbox.color import spot, rgb

class Palette:
    """
    
    >>> c = BusinessAsUsual()
    >>> c.c2
    Color(spot=877)
    >>> c[3]
    Color(spot=541)
    >>> sorted(PALETTES.keys())
    ['BackToTheCity', 'BusinessAsUsual', 'FairyTales', 'FreshAndShiny', 'IntoTheWoods', 'SeasoningTheDish', 'SomethingInTheAir', 'WordlyWise']
    """
    def __init__(self):
        self.name = self.__class__.__name__
        for attrName, value in self.COLORS.items():
            setattr(self, attrName, value)

    def __repr__(self):
        s = self.name
        for n in range(12):
            s += ' %s' % self[n].spot
        return '<%s>' % s

    def __getitem__(self, index):
        return getattr(self, 'c%d' % index)

class BusinessAsUsual(Palette):
    COLORS = dict(
        c0=spot('blacku'),c1=spot(404),  c2=spot(877),   c3=spot(541),   c4=spot(542),   c5=spot(545),
        c6=spot(506),   c7=spot(111),   c8=spot(459),   c9=spot(568),   c10=spot(3145), c11=spot(139),
    )

class SeasoningTheDish(Palette):
    COLORS = dict(
        c0=spot(412),   c1=spot(404),   c2=spot(403),   c3=spot(401),   c4=spot(103),   c5=spot(124),
        c6=spot(158),   c7=spot(200),   c8=spot(314),   c9=spot(3272),  c10=spot(369),  c11=spot(389),
    )

class WordlyWise(Palette):
    COLORS = dict(
        c0=spot(195),   c1=spot(187),   c2=spot(214),   c3=spot(258),   c4=spot(270),   c5=spot(265),
        c6=spot(280),   c7=spot(278),   c8=spot(286),   c9=spot(427),   c10=spot(429),  c11=spot(430),
    )

class FreshAndShiny(Palette):
    COLORS = dict(
        c0=spot('coolgray11u'),c1=spot('coolgray9u'),c2=spot('coolgray6u'),c3=spot(165),   c4=spot(375),   c5=spot('rhodamineredu'), 
        c6=spot(2995),  c7=spot('yellow'),c8=spot(265),  c9=spot('processblacku'),     c10=spot('red032u'), c11=spot('processblacku'),
    )

class IntoTheWoods(Palette):
    COLORS = dict(
        c0=spot(350),   c1=spot(348),   c2=spot(381),   c3=spot(392),   c4=spot(398),   c5=spot(376),
        c6=spot('warmgray10u'),c7=spot('warmgray8u'),   c8=spot('warmgray4u'),     c9=spot(2975),  c10=spot(305),  c11=spot('processblue'),
    )

class FairyTales(Palette):
    COLORS = dict(
        c0=spot(473),   c1=spot(373),   c2=spot(197),   c3=spot(278),   c4=spot(237),   c5=spot(305),
        c6=spot(465),   c7=spot(453),   c8=spot(420),   c9=spot(451),   c10=spot(422),  c11=spot(425),
    )

class BackToTheCity(Palette):
    COLORS = dict(
        c0=spot(476),   c1=spot(478),   c2=spot(500),   c3=spot(480),   c4=spot(1405),  c5=spot(139),
        c6=spot(145),   c7=spot(157),   c8=spot(1815),  c9=spot(193),   c10=spot(421),  c11=spot(423),
    )

class SomethingInTheAir(Palette):
    COLORS = dict(
        c0=spot(540),   c1=spot(542),   c2=spot(544),   c3=spot(2985),  c4=spot('reflexblue'),c5=spot(307),
        c6=spot(306),   c7=spot(3005),  c8=spot('yellow'),c9=spot(137),  c10=spot(190),  c11=spot(245),
    )

PALETTES = {}
for cls in (BusinessAsUsual, SeasoningTheDish, WordlyWise, FreshAndShiny, 
    IntoTheWoods, FairyTales, BackToTheCity, SomethingInTheAir):
    PALETTES[cls.__name__] = cls()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
