from pagebot.contributions.filibuster.blurb import Blurb

NO_TAGS = True # Flag to show/hide HTML tags in output

w = Blurb()

print w.getBlurb('article_ankeiler', noTags=NO_TAGS)
print
print w.getBlurb('article_summary', noTags=NO_TAGS)
print
print w.getBlurb('article', noTags=NO_TAGS)
