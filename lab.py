import re

s = input()
substring = input()
if re.search(substring, s):
    print("Yes")
else:
    print("No")