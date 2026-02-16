def add(a, b):
    return a + b

def greet(name):
    return "Hello " + name


def is_even(x):
    if x % 2 == 0:
        return True
    return False

def calc(a, b):
    return a + b, a - b

def check(num):
    if num > 0:
        return "Positive"
    else:
        return "Negative"


print(add(2, 3))
print(greet("Arkhat"))
print(is_even(4))

s, d = calc(10, 5)
print(s, d)

print(check(-2))
