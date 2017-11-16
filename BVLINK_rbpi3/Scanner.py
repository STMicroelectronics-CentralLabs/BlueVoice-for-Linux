from bluepy.btle import DefaultDelegate
import os


if os.getenv('C', '1') == '0':
    ANSI_RED = ''
    ANSI_GREEN = ''
    ANSI_YELLOW = ''
    ANSI_CYAN = ''
    ANSI_WHITE = ''
    ANSI_OFF = ''
else:
    ANSI_CSI = "\033["
    ANSI_RED = ANSI_CSI + '31m'
    ANSI_GREEN = ANSI_CSI + '32m'
    ANSI_YELLOW = ANSI_CSI + '33m'
    ANSI_CYAN = ANSI_CSI + '36m'
    ANSI_WHITE = ANSI_CSI + '37m'
    ANSI_OFF = ANSI_CSI + '0m'
    
class ScanPrint(DefaultDelegate):

	def __init__(self, opts=0):
		DefaultDelegate.__init__(self)
		self.opts = opts
		self.index=0
		self.listDev=[]
		
	def getListDev(self):
		return self.listDev

	def handleDiscovery(self, dev, isNewDev, isNewData):
		
		dict_dev={}
		if dev.rssi < -128:
			return
			
		if not dev.connectable:
			return
		
		for (sdid, desc, val) in dev.getScanData():
			
			if sdid in [8, 9]:
				self.index=self.index+1
				print(str(self.index) +') ' + str(ANSI_CYAN + val + ANSI_OFF) + ' --> ['+ ANSI_WHITE + dev.addr + ANSI_OFF + ']' + '(' + dev.addrType +') rssi: '+ str(dev.rssi) )
				dict_dev['index']= self.index
				dict_dev['name']= val
				dict_dev['addr']= dev.addr
				dict_dev['type_addr']= dev.addrType
				self.listDev.append(dict_dev)
		if not dev.scanData:
			print ('\t(no data)')
  
