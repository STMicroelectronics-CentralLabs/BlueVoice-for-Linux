import sounddevice as sd
import Node as stl
import Scanner as scr
from bluepy.btle import UUID, Scanner, BTLEException
import struct
import sys
import getopt
import math
import random
from collections import deque
from threading import Thread
import os
import argparse
from argparse import ArgumentParser
from subprocess import call
import signal

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


queue_audio=deque()

def init_audio(d_out):
	global stream
	sd.default.channels=1
	devIndex =-1
	devices= sd.query_devices()
	devF=-1
	for d in devices:
		if d_out == "stl_capture":
			
			if d["name"] == "STL_playback":
				devIndex=devices.index(d)
				devF= int(d["default_samplerate"])
				print("DEVICE: %s  INDEX:  %s  RATE:  %s " %  (d["name"],devIndex, devF))
			if d["name"] == "STL_capture":
				print(ANSI_CYAN + "MIC DEVICE: %s  INDEX:  %s  RATE:  %s CH: %s" %  
				(d["name"],devices.index(d),  int(d["default_samplerate"]), sd.default.channels[0])+ ANSI_OFF)
				
		if d_out == "alsa_playback":
			if d["name"] == "alsa_playback":
				devIndex=devices.index(d)
				devF= int(d["default_samplerate"])
				print("DEVICE: %s  INDEX:  %s  RATE:  %s " %  (d["name"],devIndex, devF))
			
	sd.default.device=devIndex		
	sd.default.dtype='int16'
	stream = sd.RawOutputStream(samplerate=devF)
			
def audio_player():
	global stream
	while True:
		if len(queue_audio) >= 20:
			play= b''.join(queue_audio)
			queue_audio.clear()
			stream.write(play)
		
def audio_getter():
	global brd
	while True:
		brd.mAudio.audio_stream(queue_audio)

def signal_handler(signal, frame):
	print('You have pressed Ctrl+C!')
	call(["mv", "/home/pi/.asoundrc_bkp", "/home/pi/.asoundrc"])
	call(["scp",  "/etc/asound_bkp.conf", "/etc/asound.conf"])
	call(["rm",  "/etc/asound_bkp.conf"])
	sys.exit()

def main():
	global brd
	global stream
	timeout_sc=2
	n_dev=-1
	
	# Instantiate the parser
	parser = argparse.ArgumentParser(description='BV_Link_rbpi3 application')
	# Required positional argument
	parser.add_argument('output_config', type=str, help='[alsa_playback] to playback directly to the speaker. [stl_capture] to create a virtual microphone')
	parser.add_argument('freq_config', type=int, help='[16000] to set 16KHz frequency.[8000] to set 8KHz frequency')

	args = parser.parse_args()
	if args.output_config != "alsa_playback" and args.output_config != "stl_capture":
		parser.error("output_config required, type -h to get more information") 
	
	if args.freq_config != 16000 and args.freq_config != 8000:
		parser.error("freq_config required, type -h to get more information") 
	
	#make a backup of orginal configuration files
	call(["cp", "/home/pi/.asoundrc", "/home/pi/.asoundrc_bkp"])
	call(["scp",  "/etc/asound.conf", "/etc/asound_bkp.conf"])
	if args.freq_config == 16000:
		call(["cp", "./asoundrc_template_16KHz", "/home/pi/.asoundrc"])
		call(["scp", "./asoundrc_template_16KHz", "/etc/asound.conf"])
	else:
		call(["cp", "./asoundrc_template_8KHz", "/home/pi/.asoundrc"])
		call(["scp", "./asoundrc_template_8KHz", "/etc/asound.conf"])
	
	#scanning phase
	sc=scr.ScanPrint()
	print (ANSI_RED + "Scanning for devices..." + ANSI_OFF)
	try:
		hci0=0
		scanner = Scanner(hci0).withDelegate(sc).scan(timeout_sc)
	except BTLEException:
		hci0=1
		scanner = Scanner(hci0).withDelegate(sc).scan(timeout_sc)
	devices= sc.getListDev()
	
	if len(devices) > 0:
		print("Type the index of device to connect (eg. " + str(devices[0].get('index')) + 
		" for " + devices[0].get('name') + " device)...")
	else:
		print("no device found")
		exit()
	try:
		n_dev=int(input('Input:'))
	except ValueError:
		print (" Not a number")
		exit()
	
	if (n_dev in range(1,len(devices)+1)) and n_dev > 0:
		print("Valid device")
	else:
		print (" Not valid device")
		exit()
	
	#connection
	for d in devices:
		if d.get('index') == n_dev:
			print(	'Connecting to ' + d.get('name') + "...")
			brd = stl.Node(d.get('addr'),d.get('type_addr'))
	
	print("Connected")
	brd.syncAudio.enable()
	brd.syncAudio.enableNotification()

	brd.mAudio.enable()
	brd.mAudio.setSyncManager(brd.syncAudio)	
	brd.mAudio.enableNotification()
	 
	init_audio(args.output_config)
	
	getter = Thread(target=audio_getter)
	getter.start()
	player = Thread(target=audio_player)
	player.start()
	print(	'double tap on SensorTile device (for BVLINK1 FW only) ' )
	print(	'push SW2 button on BlueCoin device (for BVLINK1 FW only) ' )
	print(	'Start_stream... ' )
	signal.signal(signal.SIGINT, signal_handler)
	print('Press Ctrl+C to exit')
	signal.pause()
	stream.start()
	
	while True:
		brd.waitForNotifications(1.0)
				
	brd.disconnect()
	del brd


if __name__ == "__main__":
	main()
