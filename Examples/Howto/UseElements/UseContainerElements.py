# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     UseContainerElements.py
#
#     Container element hold an ordered list of elements.
#     Each element knows its own position.
#
from pagebot.elements import newRect

def run():
	c = newRect(name='myContainerElement')

	print('Container we made:'+str(c))
	print('No elements yet:'+str(c.elements)) # Currently no elements in the container
	child1 = newRect(parent=c, name='Child1') # Make child containers with unique Id
	child2 = newRect(parent=c, name='Child2')
	# Get unique element eIds
	eId1 = child1.eId
	eId2 = child2.eId
	print('-- Now the container got 2 named child containers.')
	print('Elements:'+str(c.elements)) # Currently no elements in the container
	print('-- None of the children are placed on default position (0, 0, 0)')
	for e in c.elements:
	    print(e.name, e.x, e.y, e.z)
	print('-- Place the Child1 element on a fixed position (x,y), z is undefined/untouched')
	child1.x = 20
	child1.y = 30
	child1.z = 100
	print(child1)
	print('-- Place the same Child2 element on another fixed position (x,y,z), a point tuple.')
	child2.point = (120, 30, 20)
	print(child2)
	print('-- The container behaves as a dictionary of child elements with e.eId as key.')
	print(c[eId1])
	print(c[eId2])

if __name__ == '__main__':
	run()
	print('Done')

