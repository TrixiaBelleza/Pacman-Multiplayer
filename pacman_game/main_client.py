import client

name = input("Enter your name: ")
ptype = input("Enter your type: ")
port = int(input("Enter port: "))
c = client.Client(name, ptype)

hostname = '127.0.0.1'
# port = 10950

c.hostname = hostname
c.port = port


c.connect()

if c.player.player_type == "HOST" :
	c.create_room()
else :
	lobby_id = input("Enter lobby_id: ")
	c.join(lobby_id)

while True:
	pass