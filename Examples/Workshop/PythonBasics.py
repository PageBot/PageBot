if 0:
    # Integer
    print 12,23,34,5,56,67
    print 2323 * 2322 * 213862137623876321786123786123786123123867
    print 2 + 8 * 2, (2 + 8) * 2
    print isinstance(123, (int, long))
if 0:
    # Float
    print 1212.0 * 1223
    print 10/5
if 0:
    # String
    print 'This is a string'
    print "This is a 'quoted' string"
    print """This 'is' a "quoted" string"""
    print '''This 'is' a "quoted" """string"""'''
    print 'abc' + 'def' * 10
    print ('abc' + 'def') * 10
# List
if 0:
    print [12, 23, 'AAAA', 45, 56] + [55,55]*3
    aa = [44,55,66,99,100,22, 33, 44]
    aa.append(77)
    print aa
    print aa[1], len(aa), aa[2:5], aa[-2], aa[1:-3]
    hugeList = []
    for n in range(10000):
        hugeList.append(n)
    print hugeList[233:-600]
# Tuple
if 0:
    print (12, 23, 'AAAA', 45, 56) + (55,55)*3
    aa = (44,55,66,99,100,22, 33, 44)
    #aa.append(77)
    print aa
    print aa[1], len(aa), aa[2:5], aa[-2], aa[1:-3]
    bb = list(aa)
    bb.append(77)
    print bb
# Dictionary
if 0:
    d = {'ccc': 666, 'aaa': 123, 'bbb': 345}
    print d
    print d['aaa']
    print d.keys()
    print d.values()
    for key, value in sorted(d.items()):
        print key, '-->', value
# Set
if 0:
    s = set([34,34,34,34,34,34,34,34,34,34,34,45,45,45])
    print s

    print d.items()

    a = (23,34,45,65)
    print a
    qq,ww,ee,rr = a
    print qq,ww,ee,rr

    a = 10
    b = 20
    #c = a
    #a = b
    #b = c

    a, b = b, a
    print a, b

# Loops  
if 1:  
    # Processing: for (int i=0; i<10; i++){ ... }
    for n in range(10):
        print n
