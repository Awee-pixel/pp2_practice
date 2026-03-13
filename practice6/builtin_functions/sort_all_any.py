n=int(input())
arr=list(map(int,input().split()))
result=set(arr)
final=sorted(result)
for i in final:
    print(i,end=" ")

n=input().lower()
vowels=["a", "e", "i", "o", "u"]
if any(char in n for char in vowels):
    print("Yes")
else:
    print("No")

n = input().lower()
vowels = set("aeiou")
if vowels.intersection(n):
    print("Yes")
else:
    print("No")

n=int(input())
arr=list(map(int,input().split()))
if all(i>=0 for i in arr):
    print("Yes")
else:
    print("No")

n=int(input())
arr=input().split()
longest=max(arr,key=len)
print(longest)