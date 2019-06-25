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
#     mining/wikipedia/wikicontent.py
#
#     TODO: Make this work, answering a Wikipadia content page from a topic or word.
#
import urllib

class WikiContent:
	"""Answer a container with content json from Wikipedia pages.

	wiki = WikiContent()
	"""
	URL = 'https://en.wikipedia.org/w/api.php?'

	def __init__(self, topic=None):
		url = self.URL
		# https://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=info&format=json
		url += 'action=query&prop=extracts&format=json&exintro=&titles=%s' % (topic or 'bees')
		response = urllib.request.urlopen(url) # TODO @@@@@ Error in urllib.request attribute
		html = response.read()
		print(html)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
