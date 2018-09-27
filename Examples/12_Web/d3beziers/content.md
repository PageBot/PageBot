~~~Python
cid = 'D3 Beziers'


doc.lib['footer'] = "Footer. How do you change a plan into a planning and mistakes into treasures? Where can you find the design space to develop?"

doc.title = doc.name = 'D3%nbsp;Beziers'
page = doc[1]
box = page.deepFind('Logo')
~~~
# D3 Beziers


~~~Python
box = page.select('Content')
~~~

# The Bezier Game

For a second-order (quadratic) Bézier curve, first we find two intermediate points that are t along the lines between the three control points. Then we perform the same interpolation step again and find another point that is t along the line between those two intermediate points. Plotting this last point yields a quadratic Bézier curve. The same steps can be repeated for higher orders.

~~~Python
box = page.select('Content2')
~~~

## Repeat to improve again

DesignDesign.Space




~~~Python
box = page.select('ColoredSectionHeader')
~~~

~~~Python
box = page.select('ColoredSection0')
~~~

![pagebot_macbookpro.jpg](images/pagebot_macbookpro.jpg)

Now more than ever, people buy brands not products. They react to beautiful delightful experiences. Beauty and elegance are core to our strategy and purposeful in our design.

~~~Python
box = page.select('ColoredSection1')
~~~

![pagebot_smartphone_with_hand.jpg](images/pagebot_smartphone_with_hand.jpg)

Now more than ever, people buy brands not products. They react to beautiful delightful experiences. Beauty and elegance are core to our strategy and purposeful in our design.

~~~Python
box = page.select('ColoredSection2')
~~~

![pagebot_tablet.jpg](images/pagebot_tablet.jpg)

Now more than ever, people buy brands not products. They react to beautiful delightful experiences. Beauty and elegance are core to our strategy and purposeful in our design.

~~~Python
box = page.select('Footer').append(doc.lib['footer'])
~~~
 

