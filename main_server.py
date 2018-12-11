import server

port = 10939
server = server.Server('0.0.0.0',port)
# server = server.Server('10.11.158.171',port)
# server = server.Server('10.11.150.50',port)
server.run()
