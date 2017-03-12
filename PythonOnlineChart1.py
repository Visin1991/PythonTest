#!/user/bin/env python
'''
	cd Desktop\PythonPy\PythonTest
	Python PythonOnlineChart1.py
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

class ThreadedTCPRequestHandler(BaseRequestHandler):
	def handle(self):
		data = str(self.request.recv(1024),'ascii')
		cur_thread = threading.current_thread()
		response = bytes("{}:{}".format(cur_thread.name,data),'ascii')
		self.request.sendall(response)

class ThreadedTCPServer(ThreadingMixIn,TCPServer):
	pass

def client(ip,port,message):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((ip,port))
	try:
		sock.sendall(bytes(message,'ascii'))
		response = str(sock.recv(1024),'ascii')
		print("Receive:{}".format(response))
	finally:
		sock.close()

class CreateAChartWindow():
	def __init__(self):
		self.win = tk.Tk()
		self.win.title("Python GUI")
		self.createWidgets()
		self.CreateServer()
	
	def CreateServer(self):
		HOST, PORT = "localhost", 0
		server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
		ip, port = server.server_address
		server_thread = threading.Thread(target=server.serve_forever)
		server_thread.daemon = True
		server_thread.start()
		print("Server loop running in thread:", server_thread.name)
		client(ip, port, "Hello World 1")
		client(ip, port, "Hello World 2")
		client(ip, port, "Hello World 3")

		server.shutdown()
		server.server_close()
	
	def _SendMessage(self):
		print('{}. Ha ha'.format(self.name.get()))
		self.scr.configure(state='normal')
		self.scr.insert(tk.INSERT,self.name.get() + '\n')
		self.scr.configure(state='disabled')
		self.name.set('')
	
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
		
		
cw = CreateAChartWindow()
cw.win.mainloop()