import client


x = client.Client("0.0.0.0", 10939)

name = input("Enter your name: ")
ptype = input("Enter your type: ")

x.connect(name, ptype)
x.start_game("map1.txt")