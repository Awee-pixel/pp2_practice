def sqr(n):
    cnt=1
    while cnt<=n:
        yield cnt*cnt
        cnt+=1

sqrt=sqr(5)
for n in sqrt:
    print(n)

def even(n):
    cnt=0
    while cnt<=n:
        yield cnt
        cnt+=2

x=int(input())
evn=even(x)
first = True
for n in even(x):
    if not first:
        print(",", end="")
    print(n, end="")
    first = False

def div(n):
    cnt=0
    while cnt<=n:
        if cnt%3==0 and cnt%4==0:
            yield cnt
            cnt+=1
        else:
            cnt+=1

x=int(input())
Dyv=div(x)
for n in Dyv:
    print(n)


def sqr(n):
    cnt=1
    while cnt<=n:
        yield cnt*cnt
        cnt+=1

x=int(input())
for n in sqr(x):
    print(n)

def ret(n):
    cnt=0
    while cnt<=n:
        yield n
        n-=1
x=int(input())
for n in ret(x):
    print(n)