import json
x =  '{ "name":"John", "age":30, "city":"New York"}'
#json string we converts into python dictionary
y = json.loads(x)

print(y["age"])

x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}
#but here we turned python dict into json string by command dumps
y = json.dumps(x)

print(y)
#You can convert Python objects of the following types, into JSON strings:
#dict
#list
#tuple
#string
#int
#float
#True
#False
#None

import json

print(json.dumps({"name": "John", "age": 30}))
print(json.dumps(["apple", "bananas"]))
print(json.dumps(("apple", "bananas")))
print(json.dumps("hello"))
print(json.dumps(42))
print(json.dumps(31.76))
print(json.dumps(True))
print(json.dumps(False))
print(json.dumps(None))

import json

x = {
  "name": "John",
  "age": 30,
  "married": True,
  "divorced": False,
  "children": ("Ann","Billy"),
  "pets": None,
  "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
  ]
}

print(json.dumps(x))
print(json.dumps(x, indent=4))
print(json.dumps(x, indent=4, separators=(". ", " = ")))
print(json.dumps(x, indent=4, sort_keys=True))