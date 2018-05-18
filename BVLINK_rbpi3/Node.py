#!/usr/bin/env python
from bluepy.btle import UUID, Peripheral, DefaultDelegate, AssignedNumbers
import math
import FeatureAudioADPCM_Module as fAudio
import FeatureAudioADPCMSync_Module as fSycAudio
from collections import deque
import json

class Node(Peripheral):
	
	def __init__(self, addr, addr_type):
		if addr_type == 'random':
			Peripheral.__init__(self,addr,"random")
		else:
			Peripheral.__init__(self,addr)
		
		# Reading data back
		with open('data_config.json', 'r') as f:
			 data = json.load(f)
		f.close()
		
		#prequel of data characteristics
		self.serviceuuid= "%08X-"+data['data_service']
		print("initBoard ")
		
		self.mAudio = fAudio.FeatureAudioADPCM(self)
		self.syncAudio = fSycAudio.FeatureAudioADPCMSync(self)

		self.delegate =  STLDelegate(self)
		self.setDelegate(self.delegate)
		
		svcs = self.discoverServices()

        
	def extracData(self, handle, data):
		if self.mAudio.getHandle() == handle:
			self.mAudio.extractData(data)
		elif self.syncAudio.getHandle() == handle:
			self.syncAudio.extractData(data)
			

class STLDelegate(DefaultDelegate):

	def __init__(self,periph):
		DefaultDelegate.__init__(self)
		self.stl=periph
		print("initDelegate ")
		
	def handleNotification(self, hnd, data):
            self.stl.extracData(hnd,data)
		

 
