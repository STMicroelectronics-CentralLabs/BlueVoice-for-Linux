import speech_recognition as sr
import sounddevice as sd
import time 

#The following name is the name of the BVLINK_rbpi3 microphone
mic_name = "STL_capture"
#Sample rate is how often values are recorded
sample_rate = 16000
#Chunk is like a buffer. It stores 2048 samples (bytes of data) here. 
#It is advisable to use powers of 2 such as 1024 or 2048
chunk_size = 2048
#Initialize the recognizer
r = sr.Recognizer()
 
#Generate a list of all audio cards/microphones
devices= sd.query_devices()
for d in devices:
	if d["name"] == "STL_capture":
		device_id=devices.index(d)
 
print ("Welcome to Speech2Text demo powered by Google API and BVLINK_rbpi3\n")
while True:
	with sr.Microphone(device_index = device_id, sample_rate = sample_rate, 
							chunk_size = chunk_size) as source:
		print ("Google ambient noise reduction on.\n")
		#wait for a second to let the recognizer adjust the 
		#energy threshold based on the surrounding noise level
		r.adjust_for_ambient_noise(source)
		time.sleep(2) 
		print ("Say something...")

		#listens for the user's input
		audio = r.listen(source)
		
		"""
		Language supported:
		
		English(UK) en-GB
		English(US) en-US
		Italian it-IT
		Mandarin Chinese zh-CN
		
		all languages:
		https://cloud.google.com/speech/docs/languages
		""" 
		try:
			text = r.recognize_google(audio, language='en-US', show_all = True)
			if len(text) >0: 
				print ("You said: \"" + text["alternative"][0]["transcript"] + "\" with " + str(int(text["alternative"][0]["confidence"]*100)) + "% of confidence")
			else:
				print("No audio present, repeat please")
				pass
			
			print ("press ENTER to continue...")
			n_dev=input('')
			
		#error occurs when google could not understand what was said
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio")
		 
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))
