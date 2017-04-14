# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     UseContainerElements.py
#
#     Container element hold an ordered list of elements.
#     Each element knows its own position.
#
import os # Import module that communicates with the file system.

import pagebot.elements.container
reload(pagebot)
from pagebot.elements.container import Container

c = Container(name='myContainerElement')

print 'Container we made:', c 
print 'No elements yet:', c.elements # Currently no elements in the container 
print
child1 = Container(eId='myId1', name='Child1') # Make child containers with unique Id
c.append(child1)

child2 = Container(eId='myId2', name='Child2')
c.append(child2)

print '-- Now the container got 2 named child containers.'
print 'Elements:', c.elements # Currently no elements in the container 
print
print '-- None of the children are placed on default position (0, 0, 0)'
for e in c.elements:
    print e.name, e.x, e.y, e.z
print
print '-- Place the Child1 element on a fixed position (x,y), z is undefined/untouched'
child1.x = 20
child1.y = 30
print child1
print
print '-- Place the same Child2 element on another fixed position (x,y,z), a point tuple.'
child2.point = (120, 30, 20)
print child2
print
print '-- The container behaves as a dictionary of child elements with e.eId as key.'
print c['myId1']
print c['myId2']

