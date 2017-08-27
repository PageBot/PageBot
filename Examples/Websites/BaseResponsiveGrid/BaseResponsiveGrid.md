# Using CSS Grid

This website generates the basic responsive CSS Grid
as defined in [here](https://gridbyexample.com/patterns/header-twocol-footer-responsive/)

~~~Python
cid = 'Website'

# Import the Document-Website class.
# No need to add any templates, they are already defined in Website
from pagebot.publications import Website

W, H = 1000, 600 # Default size of the website pages for preview

padding = 36
# Define the grid values for left and right pages

title = 'Using CSS Grid'

# The Website instance is stored as “doc”, so typesetter can find it.
# Use the predefined dynamic templates inside inside Website.
# No automatic pages, all are created by content in this file.

doc = Website(w=W, h=H, autoPages=1

~~~

This is content of the site.