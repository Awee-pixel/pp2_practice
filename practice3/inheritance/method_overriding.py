class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return "Woof"

d=Dog()
print(d.speak())


class Vehicle:
    def start(self):
        return "Vehicle starting"

class Car(Vehicle):
    def start(self):
        return "Car engine started"

c=Car()
print(c.start())


class Person:
    def greet(self):
        return "Hello"

class Student(Person):
    def greet(self):
        return "Hi, I'm a student"

s=Student()
print(s.greet())


class Shape:
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self,radius):
        self.radius=radius
    def area(self):
        import math
        return math.pi*self.radius*self.radius

circle=Circle(3)
print(circle.area())


class Logger:
    def log(self,message):
        return f"Log: {message}"

class FileLogger(Logger):
    def log(self,message):
        return f"FileLog: {message}"

fl=FileLogger()
print(fl.log("Error occurred"))
