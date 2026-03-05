import re
text= "The rain in Almaty is ai generated"
result=re.search("rain", text)
if result:
    print("Pattern found at position:",result.start() )

result=re.match("The", text) #match for only start
if result:
    print("Match found at the beginning!")

matches=re.findall("ai", text)
print("All matches: ",matches)
cnt=0
if matches:
    cnt+=1
print(cnt)


repl_text=re.sub("Almaty","Astana",text)
print(repl_text)

import re
texs="Sample 123 for st"
pattern="\\d+"
print(re.findall(pattern,texs))

import re
find=r"a.c"
test="abc aac atc"
print(re.findall(find,test))