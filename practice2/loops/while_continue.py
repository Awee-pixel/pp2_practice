i = 0
while i < 10:
    i += 1
    if i == 5:
        continue
    print(i)

i = 0
while i < 10:
    i += 1
    if i % 2 != 0:
        continue            #in 2 words 'continue' is skip command
    print(i)

while True:
    x = int(input())
    if x < 0:
        continue    #if x is negative integer we just skip it and continue our loop
    if x == 0:
        break
    print(x)

n = int(input())
i = 1

while i <= n:
    i += 1
    if n % i != 0:
        continue
    print(i)

i = 0
while i < 6:
  i += 1
  if i == 3:
    continue
  print(i)