# Showing how weakrefs work (as used in Element-parent relations.

# Arbitrary object
a = [123,342,34,324,234]
# Make two indepdent references. This does not copy a into b and c.
b = a
c = a
# Make a refer to another object.
a = 123
# Check that b still refers to the content of a, although a lost reference to it.
# This is done by Python‘s reference count. As long as there is one or more refernces,
# an object stays alive.
print b

# Now we make a simple class.
class A(object):
    pass

# Create two instances of this class, which are different objects.   
a = A()
b = A()
# Make a cross reference. This is called a circular reference, which makes
# that reference counts don't get back to zero --> will not be erased from memory.
a.bref = b
b.aref = a
# This is a construcion to avoid. It happens if parent and child objects fully refer to each other.
print b, 'equal to', a.bref
print a, 'equal to', b.aref
print
# Circular references can be avoided by weakrefs.
import weakref
# Make two instances again.
a = A()
b = A()
# Now one of them is a weakref. It is a normal reference, but not counting as such.
a.bref = weakref.ref(b)
b.aref = a
# Weakrefs are functions to be executed.
print b, 'equal to', a.bref()
print a, 'equal to', b.aref
# If we delete b, the a.bref will become obsolete, showing as None
b = 123
print 'a.bref weakred exists', a.bref
print 'But the reference result is', a.bref()
# This construction will break the circular reference if one of the object disappears.
