


from blurb import Blurb

# Show the list of all possible entries.
SHOW_ALL_TYPES = False

# see if we can generate all of them
blurb = Blurb()

# General aricle new headline
print(blurb.getBlurb('name_german_male'))
print(blurb.getBlurb('name_japanese'))

# General book title and author name
print(blurb.getBlurb('book_title'))

# Scientific book title
print(blurb.getBlurb('book_pseudoscientific'))

# Philosphy book title
print(blurb.getBlurb('book_phylosophy_title'))

# Neutral airport new headline
print(blurb.getBlurb('air_news_neutral'))

# General aricle new headline
print(blurb.getBlurb('_headline'))



# Show the list of all possible entries.
if SHOW_ALL_TYPES:
	names = blurb.getBlurbTypes()
	print(', '.join(names))

print('done')
