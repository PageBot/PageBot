~~~
doc.title = 'Nano-Test-Site'

# Page (Home)
#	Wrapper
#		Header 
#			Logo (+BurgerButton)
#			Navigation/TopMenu/MenuItem(s)
#  			Banner
#  			SlideShow (on Home)
#      		Slides
#      		SlideSide
#		Content
#			Section(s)
#				Introduction
#				Main
#				Side(s)
#		Footer
#
# ----------------------------------------
# index.html
# ----------------------------------------
page.name = 'Home'
page.url = 'index.html'
content = page.select('Content')
box = content.newBanner()
~~~
# Headline on home page
~~~
section = content.newSection()
box = section.newIntroduction()
~~~
## This is an introduction head

~~~
box = section.newMain()
~~~
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.

~~~
sides = section.newSides()
box = sides.newSide()
~~~
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.

~~~
box = sides.newSide()
~~~
This is a short side text.

~~~
box = sides.newSide()
~~~
This is a second short side text.

~~~
box = section.newMain()
~~~
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.

~~~
sides = section.newSides()
box = sides.newSide()
~~~
This is a short side text.

~~~
box = sides.newSide()
~~~
This is a second short side text.

~~~
box = sides.newSide()
~~~
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.

~~~
box = section.newIntroduction()
~~~
## This is an introduction head

~~~
box = section.newMain()
~~~
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.
This is main text.

~~~
sides = section.newSides()
box = sides.newSide()
~~~
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.
This is side text.

~~~
box = sides.newSide()
~~~
This is a short side text.

~~~
box = sides.newSide()
~~~
This is a second short side text.

