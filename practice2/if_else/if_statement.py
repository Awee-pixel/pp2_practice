#Python supports the usual logical conditions from mathematics:

#Equals: a == b
#Not Equals: a != b
#Less than: a < b
#Less than or equal to: a <= b
#Greater than: a > b
#Greater than or equal to: a >= b

#These conditions can be used in several ways, most commonly in "if statements" and loops.
 #for example 'if statement'

a = 33
b = 200
if b > a:
  print("b is greater than a") 
#In this example we use two variables, a and b, which are used as part of the if statement to test whether b is greater than a.
#As a is 33, and b is 200, we know that 200 is greater than 33, and so we print to screen that "b is greater than a".

#The if statement evaluates a condition (an expression that results in True or False). If the condition is true, the code block inside the if statement is executed. If the condition is false, the code block is skipped.
#for example,checking if a numbers is positive:
number = 15
if number > 0:
  print("The number is positive")

age = 20
if age >= 18:
  print("You are an adult")
  print("You can vote")
  print("You have full legal rights")  #you can have multiple statements inside an if block


#we can also use variables in conditions
is_logged_in = True
if is_logged_in:
  print("Welcome back!")

    #There are some examples

# 1. AND
age = 20
if age >= 18 and age <= 25:
    print("You are between 18 and 25")

# 2. OR
temperature = 35
if temperature < 0 or temperature > 30:
    print("Extreme temperature")

# 3. NOT
is_raining = False
if not is_raining:
    print("You can go for a walk")

# 4. AND + OR together
score = 85
if score >= 90 or (score >= 80 and score < 90):
    print("Good or excellent score")

# 5. Simple comparison
password = "1234"
if password == "1234":
    print("Access granted")
