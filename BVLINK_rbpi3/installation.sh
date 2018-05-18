#!/bin/bash

#install dependencies
sudo apt-get update;
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-cffi libglib2.0-dev;

sudo pip3 install sounddevice;
sudo pip3 install bluepy;

#load kernel module and let them permanent
sudo modprobe snd-aloop ; 
sudo bash -c "echo snd-aloop >> /etc/modules"




#prevent audio out garbling because of audio out peripheral of raspberry
sudo bash -c "echo disable_audio_dither=1 >> /boot/config.txt"
sudo bash -c "echo audio_pwm_mode=2 >> /boot/config.txt"


echo BVLINK_rbpi3 installation complete;
