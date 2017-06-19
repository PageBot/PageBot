# Factory
class Car():
    
    MaxSpeed = 180 # Class variable
    Colors = []
    
    def __init__(self, color):
        assert color in self.Colors, 'Please select another color, e.g. %s' % self.Colors
        self.color = color
        self._capacity = 20
        
    def drive(self, speed):
        print 'I am a', self.color, self.__class__.__name__ + ', driving',
        print min(speed, self.MaxSpeed), 'km/h'

    def __add__(self, anotherCar):
        print 'BOOOOM'
        
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

car + myFerrari

