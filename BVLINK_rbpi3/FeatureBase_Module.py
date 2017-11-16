from bluepy.btle import UUID, Peripheral, DefaultDelegate, AssignedNumbers
import struct
import json


class FeatureBase(object):
	sensorOn  = struct.pack("B", 0x01)
	sensorOff = struct.pack("B", 0x00)
	
	def __init__(self, periph):
		self.periph = periph
		self.characteristic = None
		
	def enable(self):
		if self.characteristic is None:
			self.characteristic = self.periph.getCharacteristics(1, 0xffff,  self.charUUID) [0]          
			
		if self.sensorOn is not None:
			self.characteristic.write(self.sensorOn,withResponse=False)

	def read(self):
		return self.characteristic.read()

	def disable(self):
		if self.characteristic is not None:
			self.characteristic.write(self.sensorOff)
			
	def enableNotification(self):
		ccc_desc=self.characteristic.getDescriptors()[0]
		ccc_desc.write(b"\x01")
		
	def disableNotification(self):
		ccc_desc=self.characteristic.getDescriptors()[0]
		ccc_desc.write(b"\x00")

	def extractData(self, data):
		raise NotImplementedError("Please implement this method")
		
