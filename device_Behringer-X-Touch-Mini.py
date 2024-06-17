# name=Behringer X-Touch Mini
# Author: ts-forgery
# Version 0.91

import device
import channels
from midi import *
import midi
import mixer
import patterns
import channels
from process import Process, Mode
from leds import Leds
from data import MC
from config import Config
from process import Update

def OnInit():
	"""Function called when script starts"""
	if device.isAssigned():		
		print(device.getName())
		print(f"Port Number: {device.getPortNumber()}")
		# MC.init_leds(Config.INIT_MODE)
		MC.init_leds(6)

	else:
		print("Not assigned")

def  OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""

	print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx, event.timestamp)

	p.event = event
	p.channel = channels.selectedChannel()
	p.track = mixer.trackNumber()
	p.pattern = patterns.patternNumber()
	p.random_offset = 63
	p.triage()

def OnRefresh(event):
	# print(event)
	Update.light_control(event)

p = Process()