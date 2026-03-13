def my_func(name):
    print(name+ " Kelvin")

my_func("Emil")
my_func("Tobias")
my_func("Michael")

def my_function(name): # name is a parameter
  print("Hello", name)

my_function("Emil") # Emil is an argument

def avvalue_all(integer1,integer2,integer3):
    sum=integer1+integer2+integer3
    avvalue=sum/3
    print(int(avvalue))
    print(float(avvalue))
integer1=int(input())
integer2=int(input())
integer3=int(input())
avvalue_all(integer1,integer2,integer3)

def my_func(integer):
    for i in range(0,integer):
        print(i)
        
x=int(input())
my_func(x)


def my_function(person):
  print("Name:", person["name"])
  print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)
