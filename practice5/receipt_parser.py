import re
import os
print("CURRENT DIR: ",os.getcwd())

with open("raw.txt", "r", encoding="utf-8") as f:
    text=f.read()

pattern=r"ab*"
test=re.findall(pattern,text)  #first
if test:
    print(test)
else:
    print(0)

pattern = r"ab{2,3}"

if re.search(pattern, text):  #second
    print("Match found")
else:
    print("No match")

pattern = r"[a-z]+_[a-z]+"

if re.search(pattern, text):  #third
    print("Match found")
else:
    print("No match")


pattern= r"[A-Z][a-z]+"

matches=re.findall(pattern, text) #four

print(matches)

pattern= r"a.*b"
matches=re.findall(pattern, text)
print(matches)

x=re.sub(r"[ ,.]",":",text)
print(x)

camel= re.sub(r"_([a-z])", lambda x: x.group(1).upper(), text)
print(camel)


result = re.split(r"(?=[A-Z])", text)
print(result)

result = re.sub(r'([A-Z])', r' \1', text)
print(result.strip())

snake = re.sub(r'([A-Z])', r'_\1', text).lower()
print(snake)
