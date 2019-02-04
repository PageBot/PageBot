#!/usr/bin/env python3
# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     testBabelStrings.py
#
# Compares pure Flat and FlatContext functionality.

 # Only runs under Flat
from flat import rgb, font, shape, strike, document
from pagebot.fonttoolbox.objects.font import findFont
from pagebot import getContext
from pagebot.toolbox.color import blackColor, color
from pagebot import getResourcesPath
from pagebot.toolbox.units import pt
import os, os.path

WIDTH = 400
HEIGHT = 200
FONTSIZE = 24
LEADING = 36
FONTNAME = 'BungeeHairline-Regular'

def testFlat():
    context = getContext('Flat')
    pagebotFont = findFont(FONTNAME)
    flatFont = font.open(pagebotFont.path)
    flatFill = rgb(180, 0, 125)
    pagebotFill = color((180.0 / 255, 0, 125.0 / 255))
    flatStroke = rgb(100, 180, 0)
    pagebotStroke = color(100.0 / 255, 180.0 / 255, 0)
    strokeWidth = 1

    ''' Creates a document. '''

    # Flat.
    doc = document(WIDTH, HEIGHT, 'pt')
    p = doc.addpage()

    # Pagebot.
    context.newDocument(WIDTH, HEIGHT)
    context.newPage()

    ''' Draws a figure. '''

    # Flat.
    figure = shape().fill(flatFill).stroke(flatStroke).width(strokeWidth)
    r = figure.rectangle(50, 50, 20, 20)
    p.place(r)

        # Pagebot.
    context.fill(pagebotFill)
    context.stroke(pagebotStroke)
    context.strokeWidth(strokeWidth)
    context.rect(50, 50, 20, 20)

    '''
    print(p.items[0].item.style.width)
    print(context.pages[0].items[0].item.style.width)
    '''

    s = context.pages[0].items[0]

    '''
    print(s.item.style.fill)
    print(s.item.style.stroke)
    print(s.item.style.join)
    print(s.item.style.limit)
    '''

    ''' Draws text. '''

    msg = 'Hello world!'

    # Flat.
    headline = strike(flatFont).color(flatStroke).size(FONTSIZE, LEADING, units='pt')
    t = headline.text(msg)
    entity = p.place(t)
    entity.frame(100, 100, 380, 80)

    # Pagebot.
    style = dict(font=pagebotFont, fontSize=FONTSIZE, textFill=pagebotStroke,
            leading=LEADING)
    bs = context.newString(msg, style=style)
    context.text('bla', (50, 100)) # TODO: also for native flat.
    context.text(bs, (100, 100))

    '''
    print(headline.style.size)
    print(headline.style.leading)
    print(headline.style.color.r)
    print(headline.style.color.g)
    print(headline.style.color.b)
    '''

    ''' Exports file. '''

    im = p.image(kind='rgb')
    #print(p.items)

    # TODO:
    #imagePath = getResourcesPath() + '/images/peppertom_lowres_398x530.png'
    #size = context.imageSize(imagePath)
    #print(size)

    if not os.path.exists('_export'):
        os.mkdir('_export')

    #print('Exporting native')
    doc.pdf('_export/native-flat.pdf')
    '''
    im.png('_export/native-flat.png')
    im.jpeg('_export/native-flat.jpg')
    p.svg('_export/native-flat.svg')
    '''
    print(context.doc)

    context.saveDocument('_export/pagebot-flat.pdf')
    #print('Exporting pagebot')
    #context.saveDocument('_export/pagebot-flat.png')
    #context.saveDocument('_export/pagebot-flat.jpg')
    #context.saveDocument('_export/pagebot-flat.svg')

testFlat()
