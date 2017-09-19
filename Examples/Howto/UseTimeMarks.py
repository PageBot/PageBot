# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens & Font Bureau
#     www.pagebot.io
#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     AlignElements.py
#
import pagebot
import pagebot.toolbox
import pagebot.toolbox.timemark

from pagebot.toolbox.timemark import TimeMark

def run():
	tms = [TimeMark(0, 'aaaa'), TimeMark(10000, 'vvv')]

	tms.append(TimeMark(4, 'TimeMark@4'))
	tms.append(TimeMark(100, 'TimeMark@100'))
	print 'Unsorted after append', tms
	tms.sort()
	print 'Sorted TimeMark list', tms
	print

	def findTimeMarks(t, tms):
	    for index, tm in enumerate(tms):
	        if tm.t > t:
	            return tms[index-1], tm
	    return None

	# Search what is valid in t=5
	t = 102
	print findTimeMarks(t, tms)

if __name__ == '__main__':
	run()