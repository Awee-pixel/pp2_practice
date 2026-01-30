#BOOLEANS:

print(10>9)
print(10==9)
print(10<9)

#so. when i compare two values python returns me one of two following answers: True or False

print(bool("Hello"))
print(bool(15))
                #Any value is evaluated to True
x = "Hello"
y = 15
z=0

print(bool(x))  #any string is true
print(bool(y))  #any number is true
print(bool(z))  #any number is true,except zero

bool(["apple", "cherry", "banana"]) #list or tuple,set, and dictionary also true,except empty ones ofc

#So bool has two answers.true that equals to 1 or False that equals to 0

bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})  #any empty string or something else is False

#Functions can Return a Boolean
#You can create functions that returns a Boolean Value:

def myFunction() :
  return True       #return true

print(myFunction())

