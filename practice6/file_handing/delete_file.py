import re
import os

if os.path.exists("answer.txt"):
  os.remove("answer.txt")
else:
  print("The file does not exist")

try:
    os.rmdir("test")
except:
    print("File does not exist")

with open("sample.txt","r",encoding="utf-8") as f:
    text=f.read()


