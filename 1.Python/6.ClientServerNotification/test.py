import socket

def get_hostname():
	return socket.getfqdn()


print(get_hostname())

