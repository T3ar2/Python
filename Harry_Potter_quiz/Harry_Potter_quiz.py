# Write code below 💖

gry = 0
rav = 0
sly = 0
huf = 0

print("Q1) Do you like Dawn or Dusk?")
print ("1) Dawn")
q1 = int(input("2) Dusk \n"))
if (q1 == 1):
  gry = gry + 1
elif (q1 == 2):
  huf = huf + 1
else: 
  print ("Wrong input")


print ("Q2) When I’m dead, I want people to remember me as:")
print ( "1) The Good")
print ( "2) The Great")
print ( "3) The Wise")
q2 = int(input("4) The Bold\n"))


if q2 == 1:
  huff = huff + 2
elif q2 == 2:
  sly = sly + 2
elif q2 == 3:
  rav = rav + 2
elif q2 == 4:
  gry = gry + 2
else:
  print ("Wrong input")



print ("Q3) Which kind of instrument most pleases your ear?")
print ( "1) The violin")
print ( "2) The trumpet")
print ( "3) The piano")
q3 = int(input("4) The drum\n"))


if q3 == 1:
  sly = sly + 4
elif q3 == 2:
  huff = huff + 4
elif q3 == 3:
  rav = rav + 4
elif q3 == 4:
  gry = gry + 4
else:
  print ("Wrong input")

print ("Score: ")
print ("Slytherin    : ", sly)
print ("Hufflepuff   : ", huf)
print (" Ravenclaw   : ", rav)
print (" Gryffindor  : ", gry)
