# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     BitcountReference.py
#
#     This script the PDF document with Bitcount refernce information.
#
import pagebot
from pagebot import newFS
from pagebot.fonttoolbox.objects.family import getFamilyFontPaths
from pagebot.contributions.filibuster.blurb import blurb

if __name__ == '__main__':
	#for k in getFamilyFontPaths('Bitpath'):
	#    print k

	F = 50

	s = blurb.getBlurb('article_content', noTags=True)
	fs = newFS(s, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(1, 0, 0), rLeading=0.5))
	textBox(fs, (20, 20, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = newFS(s, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(0, 1, 0), rLeading=0.5))
	textBox(fs, (20+7, 20+7, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = newFS(s, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(0, 1, 1), rLeading=0.5))
	textBox(fs, (20, 20+7, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = newFS(s, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(1, 1, 0), rLeading=0.5))
	textBox(fs, (20+7, 20, 1000, 900))

	s = blurb.getBlurb('article_content', noTags=True)
	fs = newFS(s, None, dict(font='BitpathGridDouble-RegularLineSquare', fontSize=F, textFill=(0, 0, 0), rLeading=0.5))
	textBox(fs, (20, 20, 1000, 900))