import re


with open("sample.txt","r",encoding="utf-8") as f:
    text=f.read()
    print(f.readline())
print(text)

with open("sample.txt") as f:
    print(f.read(5))

pattern=r"[A-Z][a-z]+"
matches=re.findall(pattern,text)
print(matches)

