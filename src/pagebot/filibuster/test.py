# -----------------------------------------------------------------------------
#     Contributed by Erik van Blokland and Jonathan Hoefler#     Original from filibuster.#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------

from blurb import Blurb

w = Blurb()
print w.getBlurb('name')
print w.getBlurb('article_writer')
print w.getBlurb('article_start')
print w.getBlurb('article_pullquote')
print w.getBlurb('aerospace_headline')
print w.getBlurb('aerospace_headline', 10)

print 'TYPES OF BLURBS'
print w.getBlurbTypes()
