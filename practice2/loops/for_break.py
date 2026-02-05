for i in range(1,11):
    if i == 5:
        break
    print(i)


arr = [3,7,2,9,5]
for x in arr:
    if x == 9:
        print("Found")
        break


for _ in range(1000):   #max range
    s = input()
    if s == "stop":
        break
    print(s)


n = int(input())
for i in range(2,n):
    if n % i == 0:
        print("Not prime")
        break
else:
    print("Prime")



arr = [1,3,7,8,10]
for x in arr:
    if x % 2 == 0:
        print(x)
        break

