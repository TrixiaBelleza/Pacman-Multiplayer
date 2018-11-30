import pacmanserver.server
import pacmanclient.pacman_client
import random
from pygame.locals import *
import pygame
import pong.pacman_entities
import tkinter
from tkinter import *

pygame.init()
address = input("Server address (host:port) = ")
host, port = address.split(':')
port = int(port)

SERVER_ADDRESS = (host, port)
# SCREEN_SIZE = (pong.pacman_entities.World.WIDTH, pong.pacman_entities.World.HEIGHT)

def main():


	#Randomly generate the address for this client
	local_address = ('localhost', random.randint(10000, 20000))

	server_handler = pacmanclient.pacman_client.ServerHandler(local_address,
														SERVER_ADDRESS
														)
	server_handler.start()
	

	world = pong.pacman_entities.World("map1.txt")
	window = world.pacman_window()
	window.resizable(width=FALSE, height=FALSE)
	pacman = pong.pacman_entities.Pacman("yellow", "player", world)
	window.mainloop()
		

	return

if __name__ == '__main__':
	main()