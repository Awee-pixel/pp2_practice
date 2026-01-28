a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''  #ican assign a multiline string to a variable by using three quotes
print(a)


a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

a=("hello")
print(a[1]) #work with index
print(len(a)) #length of a string

for x in "banana": #interesting loop
  print(x)

txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")
#or
txt = "The best things in life are free!"
print("free" in txt)

txt = "The best things in life are free!"
print("expensive" not in txt)


h=("Hellooo")
print(h[2:5])
print(h[:5])
print(h[5:])
print(h[-5:-2])  #Use negative indexes to start the slice from the end of the string


#modify strings
o="Hello Git"
print(o.upper())
print(o.lower())
print(o.replace("H", "h"))

age = 36
txt = f"My name is John, I am {age}"
print(txt)

txt = "We are the so-called \n \"Vikings\" from the north." #\n=endline
print(txt)


test="Hello \bWorld" #b=backspace 
print(test)