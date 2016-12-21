# -*- c oding: UTF-8 -*-

try:
    from filibuster.blurb import Blurb
except ImportError:
    from blurb import Blurb
    
import codecs
import os

# see if we can generate all of them
w = Blurb()
names = w.getBlurbTypes()

dst = os.path.join(os.getcwd(), "test")
if not os.path.exists(dst):
	os.makedirs(dst)

maxTests = 10
for name in names:
	print "trying",name
	namePath = os.path.join(dst, "%s.txt"%name)
	nameTagPath = os.path.join(dst, "%s_trying.txt"%name)
	if os.path.exists(namePath):
		print "name with dupe file %s, skipping"%(name)
		continue
	t = codecs.open(nameTagPath, 'w', 'utf-8')
	t.write("a")

	success = False
	for i in range(maxTests):
		f = codecs.open(namePath, 'a', 'utf-8')
		result = w.getBlurb(name)
		print name, result
		try:
			f.write(u"\n\n"+result)
			success = True
		except:
			print "UnicodeDecodeError"
		finally:
			f.close()

	if success:
		t.close()
		os.remove(nameTagPath)