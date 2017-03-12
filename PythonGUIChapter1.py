'''
	cd Desktop\PythonPy\PythonTest
	Python PythonGUIChapter1.py
'''
import tkinter as tk
from tkinter import ttk,Spinbox
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import messagebox as mBox
from threading import Thread
from queue import Queue
import Wei_ToolTip
import Wei_Thread_Queues as WTQ
import shutil #for CopyFile
from tkinter import filedialog as fd
from os import path
from os import makedirs

#Module level GLOBALS
#fDir = path.dirname(__file__)
fDir = path.dirname('C:/Users/ZHU/Desktop/PythonPy/PythonTest/PythonTest')

netDir = fDir + '/Backup'
if not path.exists(netDir) :
	makedirs(netDir,exist_ok=True)
	
	
from socketserver import BaseRequestHandler, TCPServer
'''
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
'''
class RequestHandler(BaseRequestHandler):
	#override base class handle method
	def handle(self):
		print('Server connected to : ',self.client_address)
		while True:
			rsp = self.request.recv(512)
			if not rsp: break
			print("Server Send Data")
			self.request.send(b'Server received: '+rsp)
			
def startServer():
	serv = TCPServer(('',24000),RequestHandler) #empty single quotes are a short cut for passing in localhost, which is our own PC. This is the IP address of 127.0.0.1.
	serv.serve_forever()

class TkinterChapter1():
	 #Create a instance
	def __init__(self):
		self.win = tk.Tk() 
		self.win.title("Python GUI")
		self.win.resizable(0,0)                       #disable resize
		self.createWidgets()
		self.defaultFileEntries()
		svrT = Thread(target=startServer,daemon=True)
		svrT.start()
	
	def defaultFileEntries(self):
		self.fileEntry.delete(0,tk.END)
		self.fileEntry.insert(0,fDir)
		if len(fDir) > self.entryLen:
			self.fileEntry.config(width=len(fDir) +3)
			self.fileEntry.config(state='readonly')
		
		self.netwEntry.delete(0,tk.END)
		self.netwEntry.insert(0,netDir)
		if len(fDir) > self.entryLen:
			self.netwEntry.config(width=len(netDir)+3)
			
	
	
	def PrintQueues(self):
		while True:
			print(self.guiQueue.get() + ' PrintQueues Thread')
	
	def Thread_InsertNumberToMessageBox(self,numOfLoops=10,strTest = 'Haha'):
		print('Hi, how are you?')
		self.scr.insert(tk.INSERT, strTest + '\n')
		for idx in range(numOfLoops):
			self.scr.insert(tk.INSERT, str(idx) + '\n')
			print('Insert index '+str(idx))
		print('Thread_InsertNumberToMessageBox():', self.runT.isAlive())
	
	#By turnining the local variable inoto a member, We can then check if the thread is still running by calling isAlive on it form another method
	def createThread(self,num):
		self.runT = Thread(target=self.Thread_InsertNumberToMessageBox,args=[num,'This is Wei, Now you Create a new Thread'])
		self.runT.setDaemon(True) # turning the thread into a background daemon,we can exit our GUI cleanly. the thread will terminated when the main thread ends
		self.runT.start()
		print(self.runT)
		print('createThread():', self.runT.isAlive())
		#textBoxes are the Comsumers of Queue data
		self.writeT = Thread(target=self.PrintQueues,daemon=True)
		self.writeT.start()
	
	def ClickMe(self):
		self.buttonA.configure(text='Hello' + self.name.get())
		print(self)
		WTQ.writeToScrol(self) 
		
	#Create Spinbox
	def _spin(self):
		self.value = self.spin.get()
		self.scr.insert(tk.INSERT,self.value + '\n')
		
	def _spin2(self):
		self.value = self.spin2.get()
		self.scr.insert(tk.INSERT,self.value + '\n')
		
	def _radCall(self):
		self.radSel = self.radVar.get()
		if self.radSel == 0:
			print("WTF")
			self.monty2.configure(text=self.colors[0])
		elif self.radSel == 1:
			self.monty2.configure(text=self.colors[1])
		elif self.radSel == 2:
			self.monty2.configure(text=self.colors[2])
	
	def _showInfoBox(self):
		mBox.showinfo('This is Wei', 'A Python GUI created using tkinter:\nThe year is 2017.')

	def _showErrorBox(self):
		mBox.showwarning('This is Wei', 'A Python GUI created using tkinter:\nWarning: Wei haven\'t create any action for this UI Event.')

	def _quit(self):
		mBox.showerror('This is Wei', 'A Python GUI created using tkinter:\nError: Wei made a BUG in this script')
		self.win.quit()
		self.win.destroy()
		exit()
		
	def _getTureOrFalse(self):
			answer = mBox.askyesno("This is Wei ",self.strs[0])
			if answer == True:
				self._getTureOrFalse()
			else:
				self._getTureOrFalse()
	
	def createWidgets(self):
		# Tab Control introduced here --------------------------------
		#every thing with self will become to a mumber of the object
		tabControl = ttk.Notebook(self.win) # Create Tab Control
		tab1 = ttk.Frame(tabControl) # Create a tab
		tabControl.add(tab1, text='Tab 1') # Add the tab
		tab2 = ttk.Frame(tabControl) # Add a second tab
		tabControl.add(tab2, text='Tab 2') # Make second tab visible
		tab3 = ttk.Frame(tabControl) # Add a third tab
		tabControl.add(tab3, text='Tab 3') # Make second tab visible
		tabControl.pack(expand=1, fill="both") # Pack to make visible
		tabControl.select(1)
		#=======================
		#tab1 
		#=======================
		#We are creating a container frame to hold all other widgets
		monty = ttk.LabelFrame(tab1,text='Monty Python')   #set the frame to child of tab1 instead of win
		monty.grid(column=0,row=0,padx=8,pady=4)
		#Button	
		self.buttonA = ttk.Button(monty,text="Click me!",command=self.ClickMe)
		self.buttonA.grid(column=2,row=1)
		
		#Entery
		ttk.Label(monty,text="Enter a name:").grid(column=0,row=0,sticky='W')
		self.name = tk.StringVar()
		nameEntered = ttk.Entry(monty,width=30,textvariable=self.name)
		nameEntered.grid(column=0,row=1,stick=tk.W)
		nameEntered.focus()  #Place cursor into name Entry
		nameEntered.delete(0,tk.END)
		nameEntered.insert(0,'< default name >')
		
		#chose Number
		ttk.Label(monty,text="Choose a number:").grid(column=1,row=0)
		number = tk.StringVar()
		self.numberChosen = ttk.Combobox(monty,width=14,textvariable=number,state='readonly')
		self.numberChosen['values'] = (1,2,4,42,400)
		self.numberChosen.grid(column=1,row=1)
		self.numberChosen.current(0)
		
		#Add Spinbox
		#spin = Spinbox(monty,from_=0,to=10,width=5,bd=8,command=_spin).
		#spin = Spinbox(monty,values=(1,2,4,42,100),width=5,bd=8,command=_spin)
		self.spin = Spinbox(monty,width=5,bd=8,command=self._spin)
		self.spin['values'] = (1,2,4,42,100)
		self.spin2 = Spinbox(monty,values=(0,50,100),width=5,bd=20,command=self._spin2)
		self.spin.grid(column=0,row=2,stick = 'W')
		self.spin2.grid(column=1,row=2,stick = 'W')
		#Add a Tooltop
		Wei_ToolTip.createToolTip(self.spin,'Hi kid what are you wanna to do')
		strData = self.spin.get()
		print("Spinbox value: "+strData) # Spinbox value: 1
		#Create a scrolledtext	
		scrolW = 50
		scrolH = 10
		self.scr = scrolledtext.ScrolledText(monty,width=scrolW,height=scrolH,wrap=tk.WORD)
		#scr.grid(column=0,columnspan=3)
		self.scr.grid(column=0,row = 3,stick='WE',columnspan=3)
		#createToolTip(self.scr,"This is a ScrolledText widget. HaHa, I am so sad, Nothing in here, please enter something")
		self.guiQueue = Queue()
		#==========================
		#Add Tab2
		#==========================
		self.monty2 = ttk.LabelFrame(tab2,text=' The Snake ')
		self.monty2.grid(column=0,row=0,padx=8,pady=4)

		#Check Box
		self.chVarDis = tk.IntVar()
		check1 = tk.Checkbutton(self.monty2,text="Disabled", variable=self.chVarDis, state='disabled')
		check1.select()
		check1.grid(column=0, row=4, sticky=tk.W,columnspan=3)

		self.chVarUn = tk.IntVar()
		check2 = tk.Checkbutton(self.monty2,text="Uncheckde",variable=self.chVarUn)
		check2.deselect()
		check2.grid(column=1,row=4,sticky=tk.W)

		self.chVarEn = tk.IntVar()
		check3 = tk.Checkbutton(self.monty2,text="Enabled",variable=self.chVarEn)
		check3.select()
		check3.grid(column=2,row=4,sticky=tk.W)
		
		self.colors = ["Blue","Gold","Red"]
		
		#create three Radiobuttons
		self.radVar = tk.IntVar()
		self.radVar.set(-1)

		for col in range(3):
			self.curRad = 'rad' + str(col)
			self.curRad = tk.Radiobutton(self.monty2,text=self.colors[col],variable=self.radVar,value=col,command=self._radCall)
			self.curRad.grid(column=col,row=5,stick=tk.W,columnspan=3)

		#Create a container to hold labels
		self.labelsFrame = ttk.LabelFrame(self.monty2,text=' Labels in a Frame')
		#labelsFrame.grid(column=0,row=7)
		self.labelsFrame.grid(column=0,row=7,padx=5,pady=5)
		ttk.Label(self.labelsFrame,text="Label1").grid(column=0,row=0)
		ttk.Label(self.labelsFrame,text="Label2").grid(column=1,row=0)
		ttk.Label(self.labelsFrame,text="Label3").grid(column=2,row=0)

		#add space around the label
		for child in self.labelsFrame.winfo_children():
			child.grid_configure(padx=8,pady=4)
			
		#Create Manage Files Frame
		mngFilesFrame = ttk.LabelFrame(tab2,text=' Manage Files: ')
		mngFilesFrame.grid(column=0,row=1,sticky='WE',padx=10,pady=5)
		
		# Define a function any time
		def getFilePath():
			print('Hello from getFilePath')
			fName = fd.askopenfilename(parent=self.win,initialdir=fDir)
			filePath.set(fName)
	
		#Add Widgets to Manage Files Frame
		lb = ttk.Button(mngFilesFrame,text="Browse to File...",command=getFilePath)
		lb.grid(column=0,row=0,sticky='WE')
		
		filePath = tk.StringVar()
		self.entryLen = scrolW
		self.fileEntry = ttk.Entry(mngFilesFrame,width=self.entryLen,textvariable=filePath)
		self.fileEntry.grid(column=1,row=0,sticky='WE')
		
		logDir = tk.StringVar()
		self.netwEntry=ttk.Entry(mngFilesFrame,width=self.entryLen,textvariable=logDir)
		self.netwEntry.grid(column=1,row=1,sticky='WE')
		
		#define a Function inside a Function.......
		def copyFile():
			src = self.fileEntry.get()
			fileName = src.split('/')[-1]
			dst = self.netwEntry.get() + '/' + fileName
			try:
				shutil.copy(src,dst)
				mBox.showinfo("Copy File to Network",'SUccess: FIle copied.')
			except FileNotFoundError as err:
				print('FileNotFoundError')
				mBox.showerror('Copy File to Network','*** Failed to copy file! ***\n\n' + str(err))
			except Exception as ex:
				mBox.showerror('Copy File to Network','*** Failed to copy file! ***\n\n' + str(ex))

		cb = ttk.Button(mngFilesFrame,text="Copy File To : ",command=copyFile)
		cb.grid(column = 0,row =1,stick='WE')
		
		#Add some space around each label
		for child in mngFilesFrame.winfo_children():
			child.grid_configure(padx=6,pady=6)
		

		#==========================
		#Add Tab3
		#==========================
		tab3 = tk.Frame(tab3,bg='blue')
		tab3.pack()
		for orangeColor in range(2):
			canvas = tk.Canvas(tab3,width =150,height=80,highlightthickness=0,bg='orange')
			canvas.grid(row=orangeColor, column=orangeColor)
		
		self.strs = ["I told you dont touch it Now you need to shutdown you PC"]
		index = 0;

		#Add Menu	
		menuBar = Menu(self.win)
		self.win.config(menu=menuBar)

		fileMenu = Menu(menuBar,tearoff=0)  #By passing in the property tearoff to the constructor of the menu, we can remove the first dashed line that, by default, appears above the first MenuItem in a menu.
		fileMenu.add_command(label="New",command=self._showErrorBox)
		fileMenu.add_command(label="Exit",command=self._quit)
		menuBar.add_cascade(label="File",menu=fileMenu)

		helpMenu = Menu(menuBar,tearoff=0)
		helpMenu.add_command(label="About",command=self._showInfoBox)
		helpMenu.add_command(label="DontClickIt",command=self._getTureOrFalse)
		menuBar.add_cascade(label="Help",menu=helpMenu)

wg = TkinterChapter1()

'''
	cd Desktop\PythonPy\PythonGUI
	Python PythonGUIChapter1.py
'''
#win.iconbitmap(r'C:\Users\ZHU\Desktop\PythonPy\PythonGUI\trumpIcon.png')
wg.win.mainloop()