from datetime import datetime
timestamps = [1706784000, 1706870400, 1706956800]
dates = list(map(lambda ts: datetime.fromtimestamp(ts).date(), timestamps))
print(dates)

names = ["  Alice  ", "BOB", "cHaRlIe"]
normalized = list(map(lambda x: x.strip().title(), names))
print(normalized)

emails = [
"user@gmail.com",
"invalid_email",
"admin@yahoo.com",
"test.com"
]
valid_emails=list(filter(lambda x: "@" in x,emails))
print(valid_emails)

numbers = [-10, 5, 0, 8, -3, 12]
positive = list(filter(lambda x: x > 0, numbers))
print(positive)

n=int(input())
arr=list(map(int,input().split()))
squares=list(map(lambda x:x*x, arr))
print(sum(squares))

n=int(input())
arr=list(map(int,input().split()))
squares=list(filter(lambda x:x%2==0, arr))
cnt=0
for n in squares:
    cnt+=1
print(cnt)