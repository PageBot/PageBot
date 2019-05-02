#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     mining/filibuster/samplecontent.py
#
#     To be developed here: functions that do data mining from external sources.
#
from pagebot import getResourcesPath
from pagebot.contributions.filibuster.blurb import Blurb

class SampleContent:
	"""Answer a container with sample content.

	>>> sc = SampleContent()
	>>> sc.imagePaths[0].endswith('/cookbot1.jpg')
	True
	>>> len(sc.articles[0]) > 100
	True
	>>> len(sc.shortHeadlines) == len(sc.MAX_ARTICLE_LENGTHS)
	True
	>>> sc.imagePaths[0].endswith('.jpg')
	True
	"""
	MAX_ARTICLE_LENGTHS = (100, 200, 500, 1000, 2000, 5000, 10000)

	def __init__(self, topic=None):
		resourcesPath = getResourcesPath()
		self.imagePaths = (
        	resourcesPath + '/images/cookbot1.jpg',
        	resourcesPath + '/images/cookbot10.jpg',
        	resourcesPath + '/images/peppertom_lowres_398x530.png',
		)
		self.longTitles = []
		self.titles = []
		self.shortTitles = []
		self.newspaperNames = []
		self.headlines = []
		self.shortHeadlines = []
		self.credits = []
		self.ankeilers = []
		self.authors = []
		self.bylines = []
		self.captions = []
		self.summaries = []
		self.decks = []
		self.articles = []
		for cnt in self.MAX_ARTICLE_LENGTHS:
			self.longTitles.append(self.getBlurb('design_headline', 20, addPeriod=False))
			self.titles.append(self.getBlurb('design_article_title', 10, addPeriod=False))
			self.shortTitles.append(self.getBlurb('design_theory', 2, addPeriod=False))
			self.newspaperNames.append(self.getBlurb('news_newspapername', cnt, addPeriod=False))
			self.credits.append(self.getBlurb('credits', cnt))
			self.headlines.append(self.getBlurb('design_headline', cnt, addPeriod=False))
			self.shortHeadlines.append(self.getBlurb('design_theory', 4, addPeriod=False))
			self.ankeilers.append(self.getBlurb('ankeilers', cnt))
			self.bylines.append(self.getBlurb('design_article_byline', cnt))
			self.authors.append(self.getBlurb('design_article_author', cnt=cnt, addPeriod=False))
			self.captions.append(self.getBlurb('captions', cnt))
			self.summaries.append(self.getBlurb('summaries', cnt))
			self.decks.append(self.getBlurb('decks', cnt))
			self.articles.append(self.getBlurb('article', cnt))

	def _get_info(self):
		"""Answer a list of attribute names that are available."""
		attrNames = []
		for attrName, value in self.__dict__.items():
			if isinstance(value, (list, tuple)):
				attrNames.append(attrName)
		return attrNames
	info = property(_get_info)

	def getBlurb(self, topic, cnt=None, addPeriod=True):
		"""Answer a generated article text with the estimated cnt length."""
		txt = Blurb().getBlurb(topic, cnt=cnt)
		while txt and txt[-1] in ',:;-':
			txt = txt[:-1]
		if addPeriod and not txt.endswith('.'):
			txt += '.'
		elif txt.endswith('.'):
			txt = txt[:-1]
		#txt = txt.capitalize()
		return txt

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
