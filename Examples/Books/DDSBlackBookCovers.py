# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Free to use. Licensed under MIT conditions
#
#     Supporting usage of DrawBot, www.drawbot.com
#     Supporting usage of Flat, https://github.com/xxyxyz/flat
# -----------------------------------------------------------------------------
#
#     bookCovers.py
#
import math

from pagebot.contexts import defaultContext as context
from pagebot.fonttoolbox.objects.family import getFamily
from pagebot import Gradient, Shadow
from pagebot.toolbox.dating import now

family = getFamily('Roboto')
robotoLight = family.findFont('Light')
robotoLightItalic = family.findFont('Light', italic=True)
robotoRegular = family.findFont('Regular')
robotoRegularItalic = family.findFont('Regular', italic=True)
robotoMedium = family.findFont('Medium')
robotoBold = family.findFont('Bold')
robotoBlack = family.findFont('Black')
robotoBlackItalic = family.findFont('Black', italic=True)
robotoThin = family.findFont('Thin')
robotoThinItalic = family.findFont('Thin', italic=True)

# Page size and margin (actual used as padding in the page).
W, H = 400, 600
M = 10

def buildCoverPages1(w, h, v):

    
    # Page 66
    context.newPage(w, h) 
    
    context.fill(0.1)
    context.rect(0, 0, w, h)
    
    c1 = (0.2, 0.7, 1)
    c2 = 0.8
    
    y = h-M
    
    # Title of cover, make it fit in with and add shadow
    coverTitleStyle = dict(font=robotoLight.path, fontSize=100, textFill=c1)
    bs = context.newString('THE', style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))
    
    y -= bh-by+M/2

    coverTitleStyle = dict(font=robotoLightItalic.path, fontSize=100, textFill=c1)
    bs = context.newString('LONGEST', style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))

    y -= bh-by+M/2

    # Title of cover, make it fit in with and add shadow
    coverTitleStyle = dict(font=robotoMedium.path, fontSize=100, textFill=c1, rTracking=0.05)
    bs = context.newString('MELLIFLUOUSLY', style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))

    y -= bh-by+M/2

    coverTitleStyle = dict(font=robotoLight.path, fontSize=100, textFill=c1, rTracking=0.07)
    bs = context.newString('supercalifragilisticexpialidociously'.upper(), style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))

    y -= bh-by+M/2

    coverTitleStyle = dict(font=robotoThin.path, fontSize=100, textFill=c1, rTracking=0.07)
    bs = context.newString('pneumonoultramicroscopicsilicovolcanoconiosis'.upper(), style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))

    y -= bh-by+M/2
    
    coverTitleStyle = dict(font=robotoLight.path, fontSize=100, textFill=c1)
    bs = context.newString('INTERMIXED', style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))

    y -= bh-by+2*M

    # Title of cover, make it fit in with and add shadow
    coverTitleStyle = dict(font=robotoMedium.path, fontSize=100, textFill=c2)
    bs = context.newString('MATTHEW', style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))

    y -= bh-by+M/2
    
    # Title of cover, make it fit in with and add shadow
    coverTitleStyle = dict(font=robotoBold.path, fontSize=100, textFill=c2)
    bs = context.newString('DOW', style=coverTitleStyle, w=w-2*M)  
    bx, by, bw, bh = bs.bounds()
    context.text(bs, (w/2-bx-bw/2, y-bh+by))

def buildCoverPages2(w, h, v):
    
    M = 30
    for pn in range(v): 
        # Page 66
        context.newPage(w, h) 
    
        context.fill(0.1)
        context.rect(0, 0, w, h)
    
        c1 = (0.2, 0.7, 1)
        c2 = 0.8
    
        y = h-M
    
    
        # Title of cover, make it fit in with and add shadow
        coverTitleStyle = dict(font=robotoRegular.path, fontSize=100, textFill=1, rTracking=0.2, openTypeFeatures=dict(smcp=True) )
        bs = context.newString('One Lightyear Equals', style=coverTitleStyle, w=w-2*M)  
        bx, by, bw, bh = bs.bounds()
        context.text(bs, (w/2-(bw+bx)/2, y-bh+by))

        y -= 100
   
        styleColors = (robotoLight, robotoLightItalic, robotoRegular, robotoRegularItalic, robotoMedium, robotoMediumItalic,
            obotoLight, robotoLightItalic, robotoThin, robotoThinItalic)
 
        if v == 1:
            R = 20
        else:
            R = math.sin(math.radians(pn*360/v))*16    
        for index, font in enumerate(styleColors):
            coverTitleStyle = dict(font=font.path, textFill=list(c1)+[index/len(styleColors)], rTracking=0.2, rLeading=0.85, )
            bs = context.newString('9460\n7304\n7258\n0800\n512', style=coverTitleStyle, w=w-2.5*M)  
            bx, by, bw, bh = bs.bounds()
            #print bx, by, bw, bh, w, w/2, w/2-bw/2+(random()*R-R/2)
            context.text(bs, (M*0.9 + (random()*R-R/2), -by+1.4*M+(random()*R-R/2)))
    
        coverTitleStyle = dict(font=robotoThin.path, fontSize=100, textFill=c1, rTracking=0.05, rLeading=0.9)
        bs = context.newString('mm', style=coverTitleStyle, w=w/5.5)    
        bx, by, bw, bh = bs.bounds()
        context.text(bs, (w*4/6+M+bx, -by+3.2*M))
    
        coverTitleStyle = dict(font=robotoRegular.path, fontSize=100, textFill=c2, rTracking=0.2, rLeading=1.2, openTypeFeatures=dict(smcp=True) )
        bs = context.newString('Design\nDesign\nSpace', style=coverTitleStyle, w=w/5)    
        bx, by, bw, bh = bs.bounds()
        context.text(bs, (w*4/6+M+bx, -by+0.75*M))
    
    

IMAGES = (
    ('_export/bookCoverPages1.pdf', W, H, None, buildCoverPages1),    ('_export/bookCoverPages1.png', W, H, None, buildCoverPages1),    ('_export/bookCoverPages2.pdf', W, H, 1, buildCoverPages2),    ('_export/bookCoverPages2.gif', W, H, 40, buildCoverPages2),)        
      
for path, w, h, v, m in IMAGES:
    newDrawing()
    m(w, h, v)
    saveImage(path, multipage=True)
    print path
    