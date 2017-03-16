'''
	cd Desktop\PythonPy\PythonTest
	multi_Thread_Client.py
'''
import sys,socket,threading
import tincanchat

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = tincanchat.PORT

def handle_input(sock):
	""" Prompt user for message and send it to server """
	print("Type message, enter to send. 'q' to quit")
	while True:
		msg = input() #Blocks
		if msg == 'q':
			print('Shut Down Client')
			sock.shutdown(socket.SHUT_RDWR)
			sock.close()
			break
		try:
			tincanchat.send_msg(sock,msg) #Blocks until sent
		except(BrokenPipeError,ConnectionError):
			break

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((HOST,PORT))
	print('Connected to {}:{}'.format(HOST,PORT))
	
	#Create thread for handling user input and message sending
	thread = threading.Thread(target = handle_input,args=[sock],daemon=True)
	thread.start()
	rest = bytes()
	addr = sock.getsockname()
	
	print('Connected to {}:{}'.format(HOST,PORT))
	#Loop indefinitely to receive message from server
	while True:
		try:
			#blocks
			(msgs,rest) = tincanchat.recv_msgs(sock,rest) #When we use Q to close the Client. we Get a error
			for msg in msgs:
				print(msg)
		except ConnectionError:
			print('Connection to server closed')
			sock.close()
			break