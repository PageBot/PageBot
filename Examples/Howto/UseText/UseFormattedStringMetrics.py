#!/usr/bin/env python
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
#     UseFormattedStringMetrics.py
#
#     It is possible to measure on the content of FormattedString instances.
#     These show examples how to do that.
#
from pagebot.contexts.platform import getContext

context = getContext()

def run():
	W, H = 1000, 400
	context.newPage(W, H)
	txt = "Hello World"
	x, y = 10, 100

	bs = context.newString(txt, style=dict(fontSize=300,
                                         font="Verdana"))
	# draw the text
	context.text(bs, (x, y))

	# calculate the size of the text
	textWidth, textHeight = context.textSize(bs)

	# set a red stroke color
	context.stroke(1, 0, 0)
	# loop over all font metrics
	for metric in (0, bs.fontDescender(), bs.fontAscender(), bs.fontXHeight(), bs.fontCapHeight()):
	    # draw a red line with the size of the drawn text
	    context.line((x, y+metric), (W-2*x, y+metric))

if __name__ == '__main__':
	run()
