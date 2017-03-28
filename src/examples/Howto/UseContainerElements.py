# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     ScalingAnImage.py
#
#     How to scale an image (without being an element) in plain DrawBot?
#
import os # Import module that communicates with the file system.

import pagebot.elements.container
reload(pagebot)
from pagebot.elements.container import Container

c = Container()

print 'Container we made:', c 
print 'No elements yet:', c.getElements() # Currently no elements in the container 
print
child1 = Container(eId='Child1') # Make child containers with unique Id
c.append(child1)

child2 = Container(eId='Child2') 
c.append(child2)

print '-- Now the container got 2 named child containers.'
print 'Elements:', c.getElements() # Currently no elements in the container 
print
print '-- None of the children are placed on a fixed position at this time.'
print c.getPositions()
print
print '-- Place the Child1 element on a fixed position (x,y), z is undefined'
c.place(child1, (20,30))
print c.getElementsPosition()
print
print '-- Place the same Child2 element on another fixed position (x,y,z)'
c.place(child2, (120,30, 20))
print c.getElementsPosition()
print
print '-- Now the children are placed on a fixed position.'
print c.getPositions()
print
print '-- The container behaves as a dictionary of child elements with e.eId as key.'
print c['Child1'], c['Child2']