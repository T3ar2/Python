import random

guess = 0
count = 0
try1 = 9
answer = random.randint(0,10)

while count != 10:
  guess = int(input("Guess the number (You have 10 tries): "))
  count = count + 1
  print ("You have more ", try1, " tries")
  try1 = try1 - 1
  if guess == answer :
    print("You got it!")
    break

print ("⚠️ You failed ⚠️")
print ("The answer was : ", answer)
