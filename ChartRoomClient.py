#!/user/bin/env python
'''
	cd Desktop\PythonPy\PythonTest
	Python ChartRoomClient.py
'''

import tkinter as tk
from tkinter import ttk,Spinbox
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
import socketserver

import sys,socket,threading

import threading
import socket
import tincanchat
import queue

HOST = tincanchat.HOST
PORT = tincanchat.PORT

send_queues = {}
lock = threading.Lock()


class CreateAChartWindow():
	def __init__(self):
		self.win = tk.Tk()
		self.win.title("Client GUI")
		self.createWidgets()
		self.CreateClient()
	
	def CreateClient(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.connect((HOST,PORT))
		recv_thread = threading.Thread(target = self.Handle_recv,args=[self.sock],daemon=True)
		recv_thread.start()
		print('Connected to {}:{}'.format(HOST,PORT))
		
	def Handle_recv(self,sock):
		''' Receive messages from client and broadcast them to
			other clients until client disconnects '''
		rest = bytes()
		while True:
			try:
				(msgs,rest) = tincanchat.recv_msgs(sock,rest)
			except(EOFError,ConnectionError):
				print('Error')
				break
			
			for msg in msgs:
					msg = '{}'.format(msg)
					self.scr.configure(state='normal')
					self.scr.insert(tk.INSERT,str(msg) + '\n')
					self.scr.configure(state='disabled')
					
	def _SendMessage(self):
		#print('{}. Ha ha'.format(self.name.get()))
		self.scr.configure(state='normal')
		msg = self.name.get()
		self.scr.insert(tk.INSERT,msg + '\n')
		self.scr.configure(state='disabled')
		self.name.set('')
		try:
			tincanchat.send_msg(self.sock,msg) #Blocks until sent
			print('Send message ' + msg)
		except(BrokenPipeError,ConnectionError):
			print("Error")
		
	
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