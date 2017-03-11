from socket import socket, AF_INET,SOCK_STREAM

def writeToScrol(inst):
	print('hi from Queue',inst)
	sock = socket(AF_INET,SOCK_STREAM) #AF_INET is Socket family, SOCK_STREAM : sock type
	sock.connect(('localhost',24000))
	for idx in range(10):
		sock.send(b'Message from a queue : ' + bytes(str(idx).encode()))
		recv = sock.recv(8192).decode()
		print("Client Resive : " + recv)
		inst.guiQueue.put(recv)
	inst.createThread(6)
	