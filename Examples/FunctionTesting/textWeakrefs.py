# Showing weakrefs (as used in Element-parent relations.

a = [123,342,34,324,234]

b = a
c = a
a = 123

print b

class A(object):
    pass
    
a = A()
b = A()

a.bref = b
b.aref = a

print a.bref
print b.aref

import weakref

a = A()
b = A()

a.bref = weakref.ref(b)
b.aref = a

print a.bref()
print b.aref

b = 123
print a.bref
print a.bref()