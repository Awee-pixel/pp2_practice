class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    pass

d=Dog()
print(d.speak())


class Vehicle:
    def wheels(self):
        return 4

class Bike(Vehicle):
    pass

b=Bike()
print(b.wheels())


class Person:
    def greet(self):
        return "Hello"

class Student(Person):
    pass

s=Student()
print(s.greet())


class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self,side):
        self.side=side
    def area(self):
        return self.side*self.side

sq=Square(5)
print(sq.area())


class Employee:
    def role(self):
        return "Staff"

class Manager(Employee):
    pass

m=Manager()
print(m.role())

class Mynumbers:
    def __iter__(self):
        self.a=1
        return self
    def __next__(self):
        if self.a<10:
            x=self.a
            self.a+=1
            return x
        else:
            raise StopIteration

myClass=Mynumbers()
myiter=iter(myClass)
for i in myiter:
    print(i)