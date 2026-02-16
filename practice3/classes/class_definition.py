class Dog:
    def bark(self):
        return "Woof"

d=Dog()
print(d.bark())


class Car:
    def start(self):
        return "Engine started"

c=Car()
print(c.start())


class Book:
    def read(self):
        return "Reading book"

b=Book()
print(b.read())


class Light:
    def turn_on(self):
        return "Light is on"

l=Light()
print(l.turn_on())


class Phone:
    def call(self,number):
        return f"Calling {number}"

p=Phone()
print(p.call("87001234567"))
