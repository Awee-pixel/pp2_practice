for i in range(1,11):
    if i == 5:
        continue
    print(i)


for i in range(1,11):
    if i % 2 != 0:
        continue
    print(i)


text = input()
for ch in text:
    if ch == " ":
        continue
    print(ch, end="")

arr = [1,2,3,4,5]
for x in arr:
    if x < 0:
        continue
    print(x)


arr = [5,6,4,8,10]
total = 0

for x in arr:
    if x <= 10:
        continue
    total += x

print(total)
