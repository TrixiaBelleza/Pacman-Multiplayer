import client

name = input("Enter your name: ")
ptype = input("Enter your type: ")
port = int(input("Enter port: "))
# hostname = input("Enter hostname: ")
c = client.Client(name, ptype)

hostname = '127.0.0.1'

c.hostname = hostname
c.port = port

c.connect()

if c.player.player_type == "HOST" :
	lobby_id = c.create_room()
else :
	lobby_id = input("Enter lobby_id: ")
	
if c.join(lobby_id) == True:
	while True:
		num_of_players = c.recvNumOfPlayers()
		print(num_of_players)
		if num_of_players == 3:
			game_state = c.startGame()
			break
