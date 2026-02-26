def fun(max):
    cnt = 1
    while cnt <= max:
        yield cnt
        cnt += 1

ctr = fun(5)
for n in ctr:
    print(n)

def fun(str):
    cnt=1
    while cnt<len(str):
        yield cnt
        cnt+=1

ctr = fun("apple")
for n in ctr:
    print(n)

def fun():
    yield 1            
    yield 2            
    yield 3            
 
for val in fun(): 
    print(val)