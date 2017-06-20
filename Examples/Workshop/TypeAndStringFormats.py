# Identifier

a = 12 # Start with [abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_] (not the hyphen), followed by a-zA-Z0-9_ (not the hyphen)
a123 = 12
_a12 = 12
#3a = 12
#in = 1234

a = 12
aa = 12.0
b = 12.9534
c = [21,23,23,23]
d = 'This is a string'

#print d + a
print a + aa, int(a + aa)
print a + b, int(a + b), round(a+b), int(round(a+b)), round(int(a+b))
print d + ' ' + str(a)

print c
print str(a) + str(b) + str(c) + str(d)

# https://www.learnpython.org/en/String_Formatting
print '%c %% %06d This is a float %0.3f with a list %s behind and a string: %s' % ('%', a, b, c, d)

print '%d %s %d %s %d %s' % (a, b, a, c, a, d)
print '%(abc)d %(thisb)s %(abc)d %(thisc)s %(abc)d %(mystring)s' % {'abc':a, 'thisb':b, 'thisc':c, 'mystring':d} 

myValues = {'in': 1234, 'abc':a, 'thisb':b, 'thisc':c, 'mystring':d, 'aaaa': 1234, 'bbbb': 2345}
myValues = dict(abc=a, thisb=b, thisc=c, mystring=d, aaaa=1234, bbbb=2345)


print '%(abc)d %(thisb)s %(abc)d %(thisc)s %(abc)d %(mystring)s' % myValues 

