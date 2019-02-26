# -----------------------------------------------------------------------------
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
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
#     UseTimeMarks.py
#
from pagebot.toolbox.timemark import TimeMark

def run():
	"""TimeMarks are use to control the change of element values over time.
	This way movement can be defined in time based documents, such as animations.
	But also support for the generation of specific document content and appearance,
	based on a time or date, can be defined this way."""

	tms = [TimeMark(0, 'aaaa'), TimeMark(10000, 'vvv')]

	tms.append(TimeMark(4, 'TimeMark@4'))
	tms.append(TimeMark(100, 'TimeMark@100'))
	print('Unsorted after append', tms)
	tms.sort()
	print('Sorted TimeMark list', tms)
	print()

	def findTimeMarks(t, tms):
	    for index, tm in enumerate(tms):
	        if tm.t > t:
	            return tms[index-1], tm
	    return None

	# Search what is valid in t=5
	t = 5
	print(findTimeMarks(t, tms))


if __name__ == '__main__':
    run()
