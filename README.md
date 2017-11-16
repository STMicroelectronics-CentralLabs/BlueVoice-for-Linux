# BlueVoice Linux Receiver - BVLINK_rbpi3

This repository contains the ST BVLINK_rbpi3 app source code for Linux OS. The application has been tested on Raspberry Pi 3 Model B but could be easily ported to other Linux platform provided that they support [ALSA drivers](https://www.alsa-project.org/main/index.php/Main_Page) and [BlueZ](www.bluez.org/).

The BVLINK_rbpi3 application can receive an audio stream over Bluetooth Low Energy link using the "BlueVoice" vendor-specific profile. The received audio stream is then exported as a it was a standard microphone peripheral taking advantage of the [ALSA aloop device](https://www.alsa-project.org/main/index.php/Matrix:Module-aloop).

# BlueVoice transmitting device
The transmitter (or BLE microphone) can be any ST platform that supports the BlueVoice protocol.
The following table states the list of compatible firmware and the supported hardware platform that can be programmed as "BlueVoice" transmitting device.

Firmware Name			|	Supported hardware platforms
----------------------- | -------------------------------------------------
FP-AUD-BVLINK1 			|	SensorTile, BlueCoin or Nucleo+X-Nucleo
FP-SNS-ALLMEMS1 		|	SensorTile, BlueCoin or Nucleo+X-Nucleo
STSW-BLUEMIC-1			|	STEVAL-BlueMic-1

SensorTile Development kit --> www.st.com/sensortile  
BlueCoin Starter Kit  --> www.st.com/bluecoin  
STEVAL-BLUEMIC-1    --> www.st.com/en/evaluation-tools/steval-bluemic-1.html  

FP-AUD-BVLINK1 		-->	www.st.com/en/embedded-software/fp-aud-bvlink1.html  
FP-SNS-ALLMEMS1 	--> www.st.com/en/embedded-software/fp-sns-allmems1.html  
STSW-BLUEMIC-1		--> www.st.com/en/embedded-software/stsw-bluemic-1.html  

The chosen firmware must be configured to stream BlueVoice at either 8KHz or 16KHz with a connection interval set to 8.
__FP-AUD-BVLINK1__ or __FP-SNS-ALLMEMS1__
```
BV_ADPCM_Config.sampling_frequency = FR_8000; /* FR_16000; */
```
```
#define AUDIO_IN_SAMPLING_FREQUENCY   FR_8000 /* FR_16000 */
```
```
aci_l2cap_connection_parameter_update_request(handle,
                                              8 /* interval_min*/,
                                              8 /* interval_max */,
                                              0   /* slave_latency */,
                                              400 /*timeout_multiplier*/);
```
__STSW-BLUEMIC-1__
```
#define AUDIO_SAMPLING_FREQUENCY     (uint16_t)(SAMPLING_FREQ_8000) /* SAMPLING_FREQ_16000 */ 
```
```
aci_l2cap_connection_parameter_update_request(handle,
                                              8   /* interval_min*/,
                                              8   /* interval_max */,
                                              0   /* slave_latency */,
                                              400 /*timeout_multiplier*/);
```
Once the firmware code has been modified according to the above hints it must be recompiled and flashed on the microcontroller, STM32 or BlueNRG-1 depending on the chosen platform.

# BVLINK_rbpi3 application
## Prerequisites

- Linux based system (Tested on Raspberry Pi 3 Model B)
- Linux OS (Tested on Raspbian)
- ALSA kernel drivers
- BlueZ kernel modules
- Python 3

## Installing procedure

Clone the repository
```
git clone 
```
Go to the proper directory
```
cd BVLINK_rbpi3/projects/BVLINK_rbpi3
```
If you want to use the step by step installation procedure jump to the Manual section, otherwise follow the Automatic one.

#### Automatic
Give the executable permissions to the installation script
```
chmod +x ./installation.sh 
```
Run the installation.sh script to install BVLINK_rbpi3:
```
sudo ./installation.sh 
```
 Now BVLINK_rbpi3 is installed. 
#### Manual 
Type the following commands to the console
```
 sudo apt-get update
 sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-cffi libglib2.0-dev
 sudo pip3 install sounddevice
 sudo pip3 install bluepy
 sudo modprobe snd-aloop ; sudo modprobe snd-pcm-oss ; sudo modprobe snd-mixer-oss ; sudo modprobe snd-seq-oss
 sudo bash -c "echo snd-aloop >> /etc/modules"
 sudo bash -c "echo snd-mixer-oss >> /etc/modules"
 sudo bash -c "echo snd-mixer-oss >> /etc/modules"
 sudo bash -c "echo snd-seq-oss >> /etc/modules"
```

## Running the application
```
 sudo python3 main.py [mode] [frequency]
```
- mode
    - __alsa_playback__: to playback directly the audio acquired from ST platform to the speaker
    - __stl_capture__: to create a standard microphone named STL_capture for audio acquisition by audacity or arecord
- frequency
    - __16000__: for a 16KHz audio frequency
    - __8000__: for a 8KHz audio frequency

Running example:
To create a 16KHz microphone peripheral named STL_capture.
```
 sudo python3 main.py stl_capture 16000
```

Acquisition example:
Create a 16Khz file audio called "record1.wav" by arecord.
```
 arecord -D STL_capture -f S16_LE -r 16000 -c 1 record1.wav
```

## Authors

* **Central Lab** - *STMicroelectronics* - 

## License

COPYRIGHT(c) 2017 STMicroelectronics

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of STMicroelectronics nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
