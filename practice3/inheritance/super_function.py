class Person:
    def __init__(self,name):
        self.name=name

class Student(Person):
    def __init__(self,name,grade):
        super().__init__(name)
        self.grade=grade

s=Student("Ali","A")
print(s.name,s.grade)


class Vehicle:
    def start(self):
        return "Vehicle starting"

class Car(Vehicle):
    def start(self):
        return super().start()+" as Car"

c=Car()
print(c.start())


class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return super().speak()+" Woof"

d=Dog()
print(d.speak())


class Rectangle:
    def __init__(self,width,height):
        self.width=width
        self.height=height

class Square(Rectangle):
    def __init__(self,side):
        super().__init__(side,side)

sq=Square(4)
print(sq.width,sq.height)


class Logger:
    def log(self,message):
        return f"Log: {message}"

class FileLogger(Logger):
    def log(self,message):
        return super().log(message)+" saved to file"

fl=FileLogger()
print(fl.log("Error occurred"))
