class Car:
    wheels=4
    def __init__(self,brand):
        self.brand=brand

c1=Car("Toyota")
c2=Car("BMW")
print(c1.wheels,c2.wheels)


class Student:
    university="NU"
    def __init__(self,name):
        self.name=name

s1=Student("Ali")
s2=Student("Dana")
print(s1.university,s2.university)


class Counter:
    total=0
    def __init__(self):
        Counter.total+=1

a=Counter()
b=Counter()
c=Counter()
print(Counter.total)


class Product:
    tax=0.12
    def __init__(self,price):
        self.price=price
    def final_price(self):
        return self.price+self.price*Product.tax

p=Product(100)
print(p.final_price())


class Game:
    difficulty="Normal"
    def __init__(self,player):
        self.player=player

g1=Game("Arhat")
Game.difficulty="Hard"
g2=Game("Dana")
print(g1.difficulty,g2.difficulty)
