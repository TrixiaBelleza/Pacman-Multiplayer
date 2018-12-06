import pacmanserver.server


def main():
    port = pacmanserver.server.PacmanServer.DEFAULT_PORT
    server = pacmanserver.server.PacmanServer(port)
    server.start()


if __name__ == '__main__':
    main()

