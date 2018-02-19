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
from pagebot.fonttoolbox.objects.font import getFontByName
for fontName in installedFonts():
    if 'Bitcount' in fontName and 'Prop' in fontName:
        f = getFontByName(fontName)
        for gName in f.keys():
            g = f[gName]
            w = g.width
            if w is None:
                print '_____', gName, w
            else:
                g.width += 25
                print f, gName, w, g.width
        f.info.familyName = f.info.familyName + '25'
        print '+#@+@+', f, f.info.familyName
        f.save(f.path.split('/')[0].replace('.ttf', '_25.ttf'))
        break