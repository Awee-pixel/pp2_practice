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

try:
    os.rmdir("test.csv")
except:
    print("File does not exist")



