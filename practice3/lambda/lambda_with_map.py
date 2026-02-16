nums=[1,2,3,4]
result=list(map(lambda x:x+10,nums))
print(result)


nums=[2,4,6]
result=list(map(lambda x:x//2,nums))
print(result)


words=["a","bb","ccc"]
result=list(map(lambda x:len(x),words))
print(result)


temps=[0,10,20]
result=list(map(lambda x:x*9/5+32,temps))
print(result)


strings=["1","2","3"]
result=list(map(lambda x:int(x)*2,strings))
print(result)
