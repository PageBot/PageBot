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
from pagebot.contexts import defaultContext as c

def run():
	W, H = 1000, 400
	c.newPage(W, H)
	txt = "Hello World"
	x, y = 10, 100

        fs = c.newString(txt, style=dict(fontSize=300,
                                         font="Verdana"))
	# draw the text
	c.text(fs, (x, y))

	# calculate the size of the text
	textWidth, textHeight = c.textSize(txt)

	# set a red stroke color
	c.stroke(1, 0, 0)
	# loop over all font metrics
	for metric in (0, fs.fontDescender(), fs.fontAscender(), fs.fontXHeight(), fs.fontCapHeight()):
	    # draw a red line with the size of the drawn text
	    c.line((x, y+metric), (W-2*x, y+metric))

if __name__ == '__main__':
	run()
