nums=[1,2,3,4,5]
result=list(filter(lambda x:x>3,nums))
print(result)


nums=[-2,-1,0,1,2]
result=list(filter(lambda x:x>=0,nums))
print(result)


words=["cat","python","hi","world"]
result=list(filter(lambda x:len(x)>3,words))
print(result)


nums=[10,15,20,25]
result=list(filter(lambda x:x%10==0,nums))
print(result)


nums=[3,6,9,12]
result=list(filter(lambda x:x%3==0 and x>5,nums))
print(result)

names=input().split()
result=list(filter(lambda s:s[0]=='S',names))
print(result)