#!/usr/bin/env python
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
from pagebot.contexts.platform import getContext
from pagebot.toolbox.color import blackColor, color
from pagebot import getResourcesPath
from pagebot.toolbox.units import pt
import os, os.path

WIDTH = 400
HEIGHT = 200
FONTSIZE = 80
LEADING = 96
FONTNAME = 'BungeeHairline-Regular'

def testFlat():
	context = getContext('Flat')
	pagebotFont = findFont(FONTNAME)
	flatFont = font.open(pagebotFont.path)
        fillColorTuple = (180, 0, 125)
        strokeColorTuple = (100, 180, 0)
	fillColor = rgb(*fillColorTuple)
	strokeColor = rgb(*strokeColorTuple)
        strokeWidth = 2.5

	''' Creates a document. '''

        # Flat.
	doc = document(WIDTH, HEIGHT, 'mm')
	p = doc.addpage()

        # Pagebot.
	context.newDocument(WIDTH, HEIGHT)
	context.newPage()

        ''' Draws a figure. '''

        # Flat.
	figure = shape().fill(fillColor).stroke(strokeColor).width(strokeWidth)
	r = figure.rectangle(50, 50, 20, 20)
	p.place(r)

        # Pagebot.
	context.fill(fillColorTuple)
	context.stroke(strokeColorTuple)
	context.strokeWidth(strokeWidth)
	context.rect(50, 50, 20, 20)

	#print(p.items[0].item.style.width)
	#print(context.pages[0].items[0].item.style.width)
	s = context.pages[0].items[0]
	#print(s.item.style.fill)
	#print(s.item.style.stroke)
	#print(s.item.style.join)
        #print(s.item.style.limit)

        ''' Draws text. '''

        # Flat.
	headline = strike(flatFont).color(strokeColor).size(FONTSIZE, LEADING)
	t = headline.text('Hello world!')
	entity = p.place(t)
	entity.frame(10, 10, 380, 80)

        # Pagebot.
        style = dict(font=pagebotFont, fontSize=FONTSIZE,
                color=rgb(*strokeColorTuple), leading=LEADING)
	bs = context.newString('Hello world!', style=style)
	context.text(bs, (10, 10))

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
