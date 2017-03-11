def writeToScrol(inst):
	print('hi from Queue',inst)
	for idx in range(10):
		inst.guiQueue.put('Message from a queue: '+str(idx))
	inst.createThread(6)
	