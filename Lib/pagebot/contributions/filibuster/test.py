
from blurb import Blurb
from content import index

import codecs
import os

# see if we can generate all of them
w = Blurb()
names = w.getBlurbTypes()

dst = os.path.join(os.getcwd(), "_export") # Make output not write to Git.
if not os.path.exists(dst):
	os.makedirs(dst)

maxTests = 20
count = 0
for name in names:
	count += 1
	#print("trying",name)
	namePath = os.path.join(dst, "%s.txt"%name)
	nameTagPath = os.path.join(dst, "___%s_trying.txt"%name)
	t = codecs.open(nameTagPath, 'w', 'utf-8')
	t.write("a")

	success = False
	f = codecs.open(namePath, 'w', 'utf-8')
	f.write("Results for \"%s\""%name)
	definedIn, usedIn = index(name)
	usedMods = {}
	for a,b in usedIn:
		usedMods[a] = True

	f.write("\nDefined in module %s"%definedIn[0])
	if usedMods:
		k = usedMods.keys()
		k.sort()
		f.write("\nUsed in %s"%", ".join(k))
	f.close()
	for i in range(maxTests):
		f = codecs.open(namePath, 'a', 'utf-8')
		result = w.getBlurb(name)
		try:
			f.write(u"\n\n"+result)
			success = True
		except:
			print("UnicodeDecodeError", definedIn[0], name)
		finally:
			f.close()

	if success:
		t.close()
		os.remove(nameTagPath)

print('generated %d files'%count)
print('done')
