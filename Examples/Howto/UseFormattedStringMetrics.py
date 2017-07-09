# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UseFormattedStringMetrics.py
#
#     It is possible to measure on the content of FormattedString instances.
#     These show examples how to do that.
#
from drawBot import newPage

def run():
	W, H = 1000, 400
	newPage(W, H)
	txt = "Hellog World"
	x, y = 10, 100


	# set a font
	font("Verdana")
	# set a font size
	fontSize(300)
	# draw the text
	text(txt, (x, y))

	# calculate the size of the text
	textWidth, textHeight = textSize(txt)

	# set a red stroke color
	stroke(1, 0, 0)
	# loop over all font metrics
	for metric in (0, fontDescender(), fontAscender(), fontXHeight(), fontCapHeight()):
	    # draw a red line with the size of the drawn text
	    line((x, y+metric), (W-2*x, y+metric))

if __name__ == '__main__':
	run()
