import pacmanserver.server
import pacmanclient.pacman_client
import random
address = input("Server address (host:port) = ")
host, port = address.split(':')
port = int(port)

SERVER_ADDRESS = (host, port)

def main():
	#Randomly generate the address for this client
	local_address = ('localhost', random.randint(10000, 20000))

	server_handler = pacmanclient.pacman_client.ServerHandler(local_address,
														SERVER_ADDRESS
														)
	server_handler.start()

	while True:
		print("game begins")

	return

if __name__ == '__main__':
	main()