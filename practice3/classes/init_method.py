class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age

p=Person("Arhat",19)
print(p.name,p.age)


class Car:
    def __init__(self,brand,year):
        self.brand=brand
        self.year=year

c=Car("Toyota",2020)
print(c.brand,c.year)


class Student:
    def __init__(self,name,grade="A"):
        self.name=name
        self.grade=grade

s=Student("Dana")
print(s.name,s.grade)


class Rectangle:
    def __init__(self,width,height):
        self.width=width
        self.height=height
    def area(self):
        return self.width*self.height

r=Rectangle(5,4)
print(r.area())


class BankAccount:
    def __init__(self,owner,balance=0):
        self.owner=owner
        self.balance=balance
    def deposit(self,amount):
        self.balance+=amount

acc=BankAccount("Ali",100)
acc.deposit(50)
print(acc.balance)
    