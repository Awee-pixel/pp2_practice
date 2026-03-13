
age = 16
if age >= 18 and age <= 25:
    print("You are between 18 and 25")
else:
    print("You are not in this age range")


temperature = 20
if temperature < 0 or temperature > 30:
    print("Extreme temperature")
else:
    print("Normal temperature")


is_raining = True
if not is_raining:
    print("You can go for a walk")
else:
    print("Take an umbrella")


score = 75
if score >= 90 or (score >= 80 and score < 90):
    print("Good or excellent score")
else:
    print("Needs improvement")


password = "0000"
if password == "1234":
    print("Access granted")
else:
    print("Access denied")
