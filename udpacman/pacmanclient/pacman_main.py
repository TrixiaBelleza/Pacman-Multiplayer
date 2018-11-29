import pacmanserver.server
import pacmanclient.pacman_client
import random
from pygame.locals import *
import pygame

address = input("Server address (host:port) = ")
host, port = address.split(':')
port = int(port)

SERVER_ADDRESS = (host, port)
SCREEN_SIZE = (300, 500)

def main():
	#Randomly generate the address for this client
	local_address = ('localhost', random.randint(10000, 20000))

	server_handler = pacmanclient.pacman_client.ServerHandler(local_address,
														SERVER_ADDRESS
														)
	server_handler.start()
	screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption('GUI Client')
	while True:
		for event in pygame.event.get():

			if event.type == KEYDOWN:
				print("down")
		
		#print("game begins")

	return

if __name__ == '__main__':
	main()