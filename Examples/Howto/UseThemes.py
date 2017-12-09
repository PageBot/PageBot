# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     UseThemes.py
#
from pagebot.themes import Themes

theme = Themes['Metallic Office']
print theme

# By default the style in a theme is a copy from the root style.
# It is possible give fields a label name instead of a real value.
theme[theme.ROOT]['font'] = '@bodyFont'
theme[theme.ROOT]['fontSize'] = '@bodySize'
theme[theme.ROOT]['textFill'] = '@bodyColor'
theme[theme.H1]['textFill'] = '@h1Color'

palettes = dict(
     bodyColor='#123456',
     h1Color=(1, 0, 0),   
     bodyFont='Verdana',
     bodySize=12, 
)

theme.applyPalette(palettes)
print theme[theme.ROOT]['font'] # Font name is substituted.
print theme[theme.ROOT]['fontSize'] # Font size now a number.
print theme[theme.ROOT]['textFill'] # Color is substituted by hex.
print theme[theme.H1]['textFill'] # Color is substituted by tuple
