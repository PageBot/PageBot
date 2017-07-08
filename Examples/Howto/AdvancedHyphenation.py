"""
Hyphenation with head and tail
TODO: 
    - show hyphen if hyphenated...
    > make it work in drawBot, extra aguments in FormattedString (headHyphenation=4, tailHyphenation=3)
    >> then drawBot.context.baseContext.BaseContext.hyphenateAttributedString will take care if it (eventually)

"""
t = "programmatic"

fs = FormattedString(fontSize=70, language='en',)
fs.append(t)

softHyphen = unichr(0x00AD)

# set head and tail
head = 4
tail  = 4

print "lenght of string:", len(fs)

hyphenPositions=[]
for i in range(len(fs)):
    p = fs.getNSObject().lineBreakByHyphenatingBeforeIndex_withinRange_(i, (0, len(fs)))
    #print p
    if head <= p <= len(fs)-tail:
        hyphenPositions.append(p)

hyphenPositions=list(set(hyphenPositions))
hyphenPositions.sort()
print "Hyphenation indexes:", hyphenPositions

a=fs
b=fs

n=0
for p in hyphenPositions:
    a=a[:p+n] + "-" + a[p+n:] # hyphen, show hyphenation
    b=b[:p+n] + softHyphen + b[p+n:] # softHyphen here can the word hyphenate 
    
    n+=1 # hyphenationPositions are 0+n, where n = number of hyphenation positions that are already defined, because we add (soft)hyphens...

# the hard hyphens:
textBox(a,(20,500,900,500)) 

# the soft hyphens:    
w = 472 # change width to see hyphenations
textBox(b,(20,50,w,500))  
fill(None)
stroke(0)
rect(20,50,w,500)
        
        