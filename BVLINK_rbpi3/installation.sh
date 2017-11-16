#!/bin/bash

#install dependencies
sudo apt-get update;
sudo apt-get install build-essential libssl-dev libffi-dev python-dev python-cffi libglib2.0-dev;

sudo pip3 install sounddevice;
sudo pip3 install bluepy;

#load kernel module and let them permanent
sudo modprobe snd-aloop ; sudo modprobe snd-pcm-oss ; sudo modprobe snd-mixer-oss ; sudo modprobe snd-seq-oss;
sudo bash -c "echo snd-aloop >> /etc/modules"
sudo bash -c "echo snd-mixer-oss >> /etc/modules"
sudo bash -c "echo snd-mixer-oss >> /etc/modules"
sudo bash -c "echo snd-seq-oss >> /etc/modules"


echo BVLINK_rbpi3 installation complete;
