class Student:
    university="NU"
    def __init__(self,name):
        self.name=name
    @classmethod
    def change_university(cls,new_name):
        cls.university=new_name

Student.change_university("KBTU")
print(Student.university)


class Product:
    discount=0.1
    @classmethod
    def set_discount(cls,value):
        cls.discount=value

Product.set_discount(0.2)
print(Product.discount)


class User:
    total_users=0
    def __init__(self,name):
        self.name=name
        User.total_users+=1
    @classmethod
    def get_total_users(cls):
        return cls.total_users

u1=User("Ali")
u2=User("Dana")
print(User.get_total_users())


class Company:
    name="TechCorp"
    @classmethod
    def rename(cls,new_name):
        cls.name=new_name

Company.rename("FutureTech")
print(Company.name)


class Temperature:
    @classmethod
    def celsius_to_fahrenheit(cls,c):
        return c*9/5+32

print(Temperature.celsius_to_fahrenheit(25))
