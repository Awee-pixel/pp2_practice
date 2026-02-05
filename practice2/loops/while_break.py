i = 0
while True:
    print(i)
    if i == 5:
        break
    i += 1

i = 1
while i <= 10:
    if i == 7:
        print("Found 7")
        break
    i += 1

while True:
    password = input("Enter password: ")
    if password == "1234":
        print("Access granted")
        break
    print("Wrong password")

total = 0
while True:
    x = int(input())
    if x == 0:
        break
    total += x

print(total)


n = int(input())
i = 2
is_prime = True

while i * i <= n:
    if n % i == 0:
        is_prime = False
        break
    i += 1

print("Prime" if is_prime and n > 1 else "Not prime")
