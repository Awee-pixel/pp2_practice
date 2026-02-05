 #There are some examples


 # 1. AND
age = 16
if age >= 18 and age <= 25:
    print("You are between 18 and 25")
else:
    print("You are not in this age range")

# 2. OR
temperature = 20
if temperature < 0 or temperature > 30:
    print("Extreme temperature")
else:
    print("Normal temperature")

# 3. NOT
is_raining = True
if not is_raining:
    print("You can go for a walk")
else:
    print("Take an umbrella")

# 4. AND + OR
score = 75
if score >= 90 or (score >= 80 and score < 90):
    print("Good or excellent score")
else:
    print("Needs improvement")

# 5. Simple equality check
password = "0000"
if password == "1234":
    print("Access granted")
else:
    print("Access denied")
