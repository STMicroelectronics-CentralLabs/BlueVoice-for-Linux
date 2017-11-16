from FeatureBase_Module import * 


def _ST_UUID(val):
		with open('data_config.json', 'r') as f:
			 data = json.load(f)
		f.close()
		return UUID(val % int(data['sync_characteristic'],16) )
   		
class FeatureAudioADPCMSync(FeatureBase):

	def __init__(self, periph):
		FeatureBase.__init__(self, periph)
		self.charUUID=_ST_UUID(periph.serviceuuid)
		self.handle= periph.getCharacteristics(uuid=self.charUUID)[0].getHandle()
		self.Index= struct.pack("h", 0)[0]
		self.PredSample= struct.pack("i", 0)[0]
		self.intra_flag=False
		print("initAudioADPCMSync ")
	
	def getHandle(self):
		return self.handle
		
	def extractData(self, data):
		if len(data) != 6:
			raise NameError('error')
		
		self.Index= struct.unpack("h", data[0:2])[0]
		self.PredSample= struct.unpack("i", data[2:6])[0]
		self.intra_flag=True
		
	def getAdpcm_index_in(self):
		return self.Index

	def getAdpcm_predsample_in(self):
		return self.PredSample

	def reinitResetFlag(self):
		self.intra_flag=False
