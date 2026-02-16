class Person:
    def greet(self):
        return "Hello"

class Worker:
    def work(self):
        return "Working"

class Employee(Person,Worker):
    pass

e=Employee()
print(e.greet(),e.work())


class A:
    def show(self):
        return "A"

class B:
    def show(self):
        return "B"

class C(A,B):
    def show(self):
        return super().show()+" and C"

c=C()
print(c.show())


class Flyer:
    def action(self):
        return "Flying"

class Swimmer:
    def action(self):
        return "Swimming"

class Duck(Flyer,Swimmer):
    def action(self):
        return super().action()+" and Quacking"

d=Duck()
print(d.action())


class Vehicle:
    def start(self):
        return "Vehicle started"

class Electric:
    def start(self):
        return "Electric system on"

class ElectricCar(Vehicle,Electric):
    def start(self):
        return super().start()+" with Electric power"

ec=ElectricCar()
print(ec.start())


class Logger:
    def log(self,message):
        return f"Log: {message}"

class FileLogger:
    def log(self,message):
        return f"FileLog: {message}"

class AppLogger(Logger,FileLogger):
    def log(self,message):
        return super().log(message)+" via App"

al=AppLogger()
print(al.log("Error occurred"))
