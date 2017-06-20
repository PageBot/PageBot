# Factory
class Car():
    
    MaxSpeed = 180 # Class variable
    Colors = []
    
    def __init__(self, color):
        assert color in self.Colors, 'Please select another color, e.g. %s' % self.Colors
        self.color = color
        self._capacity = 20
        
    def drive(self, speed):
        print str(self) + ', driving',
        print min(speed, self.MaxSpeed), 'km/h'

    def __add__(self, anotherCar):
        print 'BOOOOM'
    
    def __repr__(self): # Create represenation string from self
       return 'I am a ' + self.color + ' ' + self.__class__.__name__ 
           
class Mercedes(Car): # Class inheritance
    Colors = ['black', 'blue', 'gray']
    
class Ferrari(Car):
    Colors = ['red', 'yellow']
    MaxSpeed = 300 # Class variable
    
    
# -----------------------------------------------
     
# Create instance (or object)
car = Mercedes('blue')
# Drive the car
car.drive(80)
car.drive(179)
car.drive(1000080)
print car._capacity

myFerrari = Ferrari('yellow')
myFerrari.drive(1000080)

car + myFerrari # Is converted by preprocessor into:
car.__add__(myFerrari) # Is was is actually executed.

# This is printing the car as string. All are equivalent.
print car
print str(car)
print `car`
