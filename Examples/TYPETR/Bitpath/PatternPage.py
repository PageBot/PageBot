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
#     BitcountReference.py
#
#     This script the PDF document with Bitcount refernce information.
#
import pagebot
from pagebot.contexts import defaultContext as context
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot.contributions.filibuster.blurb import blurb

if __name__ == '__main__':
	#for k in getFamilyFontPaths('Bitpath'):
	#    print k

	F = 50

	s = blurb.getBlurb('article_content', noTags=True)
	fs = context.newString(s, style=dict(font='BitpathGridDouble-RegularLineSquare',
                                             fontSize=F,
                                             textFill=(1, 0, 0),
                                             rLeading=0.5))
	textBox(fs, (20, 20, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = context.newString(s, style=dict(font='BitpathGridDouble-RegularLineSquare',
                                             fontSize=F,
                                             textFill=(0, 1, 0),
                                             rLeading=0.5))
	textBox(fs, (20+7, 20+7, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = context.newString(s, style=dict(font='BitpathGridDouble-RegularLineSquare',
                                             fontSize=F,
                                             textFill=(0, 1, 1),
                                             rLeading=0.5))
	textBox(fs, (20, 20+7, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = context.newString(s, style=dict(font='BitpathGridDouble-RegularLineSquare',
                                             fontSize=F,
                                             textFill=(1, 1, 0),
                                             rLeading=0.5))
	textBox(fs, (20+7, 20, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = context.newString(s, style=dict(font='BitpathGridDouble-RegularLineSquare',
                                             fontSize=F,
                                             textFill=(0, 0, 0),
                                             rLeading=0.5))
	textBox(fs, (20, 20, 1000, 900))
	
saveImage('_export/PatternPage1.pdf')
