import random

answer = 0
guess = 0
count = 0
try1 = 9
difi = random.randint(0, 10)
difi2 = random.randint(0, 25)
difi3 = random.randint(0, 50)
difi4 = random.randint(0, 75)
difi5 = random.randint(0, 100)

print ("Chose you difficulty ")
print("1 - Easy      🥴")
print("2 - Medium    😟")
print("3 - difficult 😫")
print("4 - Angel     🤯 ")
dif = int(input("5 - God Like  😵 \n"))


if dif == 1:
  while count != 10:
    answer = difi
    guess = int(input("Guess the number 0 to 10 (You have 10 tries): "))
    count = count + 1
    print ("You have more ", try1, " tries")
    try1 = try1 - 1
    if guess == difi :
      print("You got it!")
      break
    elif count == 10:
      print("⚠️ You failed ⚠️")

elif dif == 2:
  while count != 10:
    answer = difi2
    guess = int(input("Guess the number 0 to 25 (You have 10 tries): "))
    count = count + 1
    print ("You have more ", try1, " tries")
    try1 = try1 - 1
    if guess == difi2:
      print("You got it!")
      break
    elif count == 10 :
      print("⚠️ You failed ⚠️")


elif dif == 3:
  while count != 10:
    answer = difi3
    guess = int(input("Guess the number 0 to 50 (You have 10 tries): "))
    count = count + 1
    print ("You have more ", try1, " tries")
    try1 = try1 - 1
    if guess == difi3 :
      print("You got it!")
      break
    else:
      print("⚠️ You failed ⚠️")


elif dif == 4:
  while count != 10:
    answer = difi4
    guess = int(input("Guess the number 0 to 75 (You have 10 tries): "))
    count = count + 1
    print ("You have more ", try1, " tries")
    try1 = try1 - 1
    if guess == difi4 :
      print("You got it!")
      break
    elif count == 10:
      print("⚠️ You failed ⚠️")

elif dif == 5:
  while count != 10:
    answer = difi5
    guess = int(input("Guess the number 0 to 100 (You have 10 tries): "))
    count = count + 1
    print ("You have more ", try1, " tries")
    try1 = try1 - 1
    if guess == difi5:
      print("You got it!")
      break
    elif count == 10:
      print("⚠️ You failed ⚠️")
else:
  print("Wrong number")
print ("The answer was : ", answer)
