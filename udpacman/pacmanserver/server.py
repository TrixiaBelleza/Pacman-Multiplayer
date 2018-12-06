import threading
import socket


class PacmanServer(threading.Thread, socket.socket):
    BUFFER_SIZE = 4096
    DEFAULT_PORT = 10939
    COMMAND_CLIENT_CONNECT = 'pacman_connect'
    
    def __init__(self, port=None):
        #initialize thread
        threading.Thread.__init__(self, name='Server thread')
        #initialize socket for connections using UDP (SOCK_DGRAM)
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)

        self.port = self.DEFAULT_PORT if port is None else port
        # self.settimeout(self.TIMEOUT)
        # specifies that the socket is reachable by any address the machine happens to have.
        self.bind(('', self.port))
        self.clients = []
        self.player_addresses = dict()
        self._current_player_to_assign = 1 #initial player number
        self.client_handlers = []

        # self.pong_world = pong.game.Pong()

    def run(self):
        print('Hosting at:', self.getsockname())
        print('Starting server.')

        for i in range(3):
            player_number = i + 1

            print('Waiting for client #{}'.format(player_number))
            c = self.wait_client()
            self.clients.append(c)

            print('Sending player number {} to {}'.format(player_number, c))
            self.send_player_number(c, player_number)

        print('Starting game.')

        while True:
            pass
            # print("on going")
       
        return

    def wait_client(self, return_queue=None):
        """Step 1: Wait for a client to connect."""
        data, address_info = self.recvfrom(self.BUFFER_SIZE)
        print('data:', data, 'address_info:', address_info)

        if data:
            decoded = data.decode('utf-8')
            if decoded != self.COMMAND_CLIENT_CONNECT:
                raise ValueError('Expecting "{}", but got "{}"'.format(self.COMMAND_CLIENT_CONNECT, decoded))
            if return_queue is not None:
                return_queue['client_address'] = address_info
            # print('Client address found:', address_info)
            return address_info

    def send_player_number(self, client_address, player_number):
        """Step 2: Create a client handler object to send the player number to the connected client"""
        ch = ClientHandler(self.port + self._current_player_to_assign, client_address, player_number, self)
        self.client_handlers.append(ch)
        self._current_player_to_assign += 1
        ch.start()    # Start happens later in another function...?

        self.player_addresses[player_number] = client_address

    def join(self, timeout=None):
        super().join()
        self.close()


class ClientHandler(threading.Thread, socket.socket):
    def __init__(self, port, client_address, player_number, server):
        socket.socket.__init__(self, type=socket.SOCK_DGRAM)
        threading.Thread.__init__(self, name='ClientHandler')
        self.settimeout(2)
        self.bind(('localhost', port))
        self.setDaemon(True)
        self.player_number = player_number
        self.client_address = client_address
        self.server = server

        self.send_player_number()

    def send_player_number(self):
        self.sendto(str(self.player_number).encode('utf-8'), self.client_address)

    # def send_game_update(self):
    #     self.sendto(self.server.pong_world.locations_json().encode('utf-8'), self.client_address)

    # def receive_client_command(self, retd=None):
    #     data, address_info = self.recvfrom(pong.common.BUFFER_SIZE)
    #     if data:
    #         decoded = data.decode('utf-8')
    #         try:
    #             cc = json.loads(decoded, object_hook=pong.common.from_json)
    #         except ValueError as err:
    #             print(err)
    #             raise ValueError('Expecting a JSON string from client, but got something else:', decoded)
    #         if retd is not None and isinstance(retd, dict):
    #             retd['client_command'] = cc
    #         return cc

    def run(self):
        #while True:
        pass  
            # print("ch on going")

    # def update_player_with_client_command(self, cc):
    #     player = None
    #     if self.player_number == 1:
    #         player = self.server.pong_world.player1
    #     elif self.player_number == 2:
    #         player = self.server.pong_world.player2
    #     player.heading = cc.heading()

    def join(self, timeout=None):
        super().join(timeout=2)
        self.close()
