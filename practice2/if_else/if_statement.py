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