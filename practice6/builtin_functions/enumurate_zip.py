users = ["Alice", "Bob", "Charlie"]
for user_id, name in enumerate(users, start=100):
    print(user_id, name)

numbers = [4, 7, 9, 15, 9]
positions = [i for i, v in enumerate(numbers) if v == 9]
print(positions)

posithions=[]
for i,v in enumerate(numbers):
    if v==9:
        posithions.append(i)

print(posithions)

n=int(input())
arr=input().split()
result=[]
for i,v in enumerate(arr):
    result.append(f"{i}:{v}")
print(*(result))

names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
result = dict(zip(names, scores))
print(result)

n = int(input())
arr1 = list(map(int, input().split()))
arr2 = list(map(int, input().split()))

dot_product = 0
for x, y in zip(arr1, arr2):
    dot_product += x * y

print(dot_product)
        

n=int(input())
arr=list(map(int,input().split()))
cnt=0
for i in arr:
    if i!=0:
        cnt+=1
print(cnt)


n=int(input())
arr1=list(input().split())
arr2=list(input().split())
key=input()
result=dict(zip(arr1,arr2))
if key in result:
    print(result[key])
else:
    print("Not found")

print(result)