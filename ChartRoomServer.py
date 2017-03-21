#!/user/bin/env python
'''
	cd Desktop\PythonPy\PythonTest
	Python ChartRoomServer.py
'''

import tkinter as tk
from tkinter import ttk,Spinbox
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
import socketserver
from socketserver import BaseRequestHandler,ThreadingMixIn,TCPServer
import threading
import socket
import tincanchat
import queue

HOST = tincanchat.HOST
PORT = tincanchat.PORT

send_queues = {}
lock = threading.Lock()


		
	

def broadcast_msg(msg):
	""" Add message to each connected client's send queue """
	with lock:
		for q in send_queues.values():
			q.put(msg)
			
def handle_client_send(sock,q,addr):
	""" Monitor queue for new messages, send them to client as they arrive """
	while True:
		msg = q.get()
		if msg == None : break
		try:
			tincanchat.send_msg(sock,msg)
		except(ConnectionError,BrokenPipe):
			handle_disconnect(sock,addr)
			break
			
def handle_disconnect(sock,addr):
	""" Ensure queue is cleaned up and socket closed when a client disconnects """
	fd = sock.fileno()
	with lock:
		#Get send queue for this client
		q = send_queues.get(fd,None)
	#If we find a queue then this disconnect has not yet been handled
	if q:
		q.put(None)
		del send_queues[fd]
		addr = sock.getpeername()
		print('Client {} disconnected'.format(addr))
		sock.close()

class CreateAChartWindow():
	def __init__(self):
		self.win = tk.Tk()
		self.win.title("Server GUI")
		self.createWidgets()
		self.CreateServer()
	
	def CreateServer(self):
		listen_sock = tincanchat.create_listen_socket(HOST,PORT)
		addr = listen_sock.getsockname()
		print("Listening on {}".format(addr))
		
		listen_thread = threading.Thread(target=self.handle_Server_Listen,args=[listen_sock],daemon=True)
		listen_thread.start()	
		
		
	def handle_Server_Listen(self,sock):
		while True:
			client_sock,addr = sock.accept()
			q = queue.Queue()
			with lock:
				send_queues[client_sock.fileno()]=q
			recv_thread = threading.Thread(target=self.handle_Client_recv,args=[client_sock,addr],daemon=True)
			send_thread = threading.Thread(target=handle_client_send,args=[client_sock,q,addr],daemon=True)
			recv_thread.start()
			send_thread.start()
			print('Connection from {}'.format(addr))
		
	def handle_Client_recv(self,sock,addr):
		''' Receive messages from client and broadcast them to
			other clients until client disconnects '''
		rest = bytes()
		while True:
			try:
				(msgs,rest) = tincanchat.recv_msgs(sock,rest)
			except(EOFError,ConnectionError):
				handle_disconnect(sock,addr)
				break
			
			for msg in msgs:
					msg = '{}: {}'.format(addr,msg)
					self.scr.configure(state='normal')
					self.scr.insert(tk.INSERT,str(msg) + '\n')
					self.scr.configure(state='disabled')
					broadcast_msg(msg)
						
	
	def _SendMessage(self):
		msg = self.name.get()
		print('{}. Ha ha'.format(msg))
		self.scr.configure(state='normal')
		self.scr.insert(tk.INSERT,str(msg) + '\n')
		self.scr.configure(state='disabled')
		self.name.set('')
		broadcast_msg(msg)
		
	
	def createWidgets(self):
		#every thing with self will become to a mumber of the object
		tabControl = ttk.Notebook(self.win) # Create Tab Control
		tab1 = ttk.Frame(tabControl) # Create a tab
		tabControl.add(tab1, text='Tab 1') # Add the tab
		tab2 = ttk.Frame(tabControl) # Add a second tab
		tabControl.add(tab2, text='Tab 2') # Make second tab visible
		tab3 = ttk.Frame(tabControl) # Add a third tab
		tabControl.add(tab3, text='Tab 3') # Make second tab visible
		tabControl.pack(expand=1, fill="both") # Pack to make visible
		#=======================
		#tab1 
		#=======================
		#We are creating a container frame to hold all other widgets
		chat = ttk.LabelFrame(tab1,text='main chat')   #set the frame to child of tab1 instead of win
		chat.grid(column=0,row=0,padx=8,pady=4)
		
		#Create a scrolledtext	
		scrolW = 60
		scrolH = 20
		self.scr = scrolledtext.ScrolledText(chat,width=scrolW,height=scrolH,wrap=tk.WORD)
		self.scr.config(state='disabled')
		#scr.grid(column=0,columnspan=3)
		self.scr.grid(column=0,row = 0,stick='WE',columnspan=3)
		
		#Button	
		self.buttonA = ttk.Button(chat,text="Send!",command=self._SendMessage)
		self.buttonA.grid(column=2,row=2)
		
		#Entery
		ttk.Label(chat,text="Enter a Massage:").grid(column=0,row=1,sticky='W')
		self.name = tk.StringVar()
		nameEntered = ttk.Entry(chat,width=40,textvariable=self.name)
		nameEntered.grid(column=0,row=2,stick=tk.W)
		nameEntered.focus()  #Place cursor into name Entry
		
		#=======================
		#tab1 					 Contain the Client Information
		#=======================
		
if __name__ == '__main__':	
	cw = CreateAChartWindow()
	cw.win.mainloop()