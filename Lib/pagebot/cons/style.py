js#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     style.py
#
# Pre-replacement in font names, to get standard non-CamelCase style names
# Works togehter with toolbox.transformer.path2StyleNameParts().
# From --> To pattern replacement.

STYLE_REPLACEMENTS = (
    # Weight
    ('UltraLight', 'Ultralight'),
    ('UltLt', 'Ultralight'),
    ('SemiLight', 'Semilight'),
    ('SemiBold', 'Semibold'),
    ('SemBold', 'Semibold'),
    ('ExtraBold', 'Extrabold'),
    ('UltraBlack', 'Ultrablack'),
    ('Ultra Black', 'Ultrablack'),
    ('Ultra-Black', 'Ultrablack'),
    ('Ultra_Black', 'Ultrablack'),
    ('ExtrBlack', 'Extrablack'),
    ('ExtBlack', 'Extrablack'),
    ('ExBla', 'Extrablack'),
    ('ExBlck', 'Extrablack'),

    # Width
    ('UltCnd', 'Ultracondensed'),
    ('UltraCondensed', 'Ultracondensed'),
    ('ExtraCondensed', 'Extracondensed'),
    ('Ultra Condensed', 'Ultracondensed'),
    ('Extra Condensed', 'Extracondensed'),
    ('Ultra-Condensed', 'Ultracondensed'),
    ('Extra-Condensed', 'Extracondensed'),
    ('Ultra_Condensed', 'Ultracondensed'),
    ('Extra_Condensed', 'Extracondensed'),

    ('ExtraExtended', 'Extraextended'),
    ('UltraExtended', 'Ultraextended'),
    ('Extra Extended', 'Extraextended'),
    ('Ultra Extended', 'Ultraextended'),
    ('Extra-Extended', 'Extraextended'),
    ('Ultra-Extended', 'Ultraextended'),
    ('Extra_Extended', 'Extraextended'),
    ('Ultra_Extended', 'Ultraextended'),
)
