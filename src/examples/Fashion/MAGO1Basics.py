# Basic classes, primitives
print (1234 + 34) * 2 # Integer = whole  number
print 1234 + 34 * 2 # Multiplication has preference
print 5/7, 10/2, int(10/2) # Float
print 'This is a string ' + 'and a word' # Add together
print 'Many words. ' * 3 # Multiple of the same string

a = [12,23,'A word',43,45] # List
print a, a[0] # Print the list, and the first element
b = a + [44,55,66] # Add one list to another
print b # Show combined lists
print b[2:5], b[-2] # Slice, index from right

d = {'word': 'This is the meaning of word',
    'dutch': 'Dutch is a language'}
print d['word']