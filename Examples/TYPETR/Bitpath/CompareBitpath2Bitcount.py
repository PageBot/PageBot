# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     CompareBitpath2Bitcount.py

from pagebot import newFS
from random import shuffle

ITALIC = False

bitpaths = []
bitcounts = []

for fontName in installedFonts():
    if 'Bitcount' in fontName:
        if 'Italic' in fontName:
            continue
        bitcounts.append(fontName)
    if 'Bitpath' in fontName:
        if 'Italic' in fontName:
            continue
        bitpaths.append(fontName)
        
bitpaths=[]
print len(bitpaths)
print len(bitcounts)

for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
    #newPage(1200, 500)
    newPage(500, 500)
    s = 'Bitcount & Bitpath'
    s = c
    fonts = bitpaths + bitcounts
    print len(fonts)
    shuffle(fonts)
    for name in fonts:
        #if not 'Double' in name:
        #   continue
        if not 'Single' in name:
            continue
        if not 'Mono' in name:
            continue
        fs = newFS(s, style=dict(font=name, fontSize=400, 
            openTypeFeatures=dict(ss01=True, ss02=True, ss03=True),
            #textFill=None,
            textFill=(random(), random(), random(), 0.05), 
            textStroke=(random(), random(), random(), 0.5), textStrokeWidth=0.5,
        ))
        text(fs, (130, 130))
        
saveImage('_export/CompareBitpath2Bitcount.pdf')