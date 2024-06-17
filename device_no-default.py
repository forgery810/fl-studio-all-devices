# name=No Default 
# Author: forgery810
VERSION = '0.8.0'

import device
import channels
from midi import *
import midi
import mixer
import patterns
import channels
from process import Process
from notes import Notes
import config_layout as cl
# from data import MC
from config import Config
# from process import Update

def OnInit():
	"""Function called when script starts"""
	if device.isAssigned():		
		AssignLayoutData(cl.buttons, cl.keyboard, cl.sequencer, cl.encoders, cl.jog_wheel);
		print(device.getName())
		print(f"Port Number: {device.getPortNumber()}")

	else:
		print("Not assigned")

def  OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""

	# print(scriptData)
	print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx, event.timestamp)



	p.event = event
	p.channel = channels.selectedChannel()
	p.track = mixer.trackNumber()
	p.pattern = patterns.patternNumber()
	p.random_offset = 63
	p.triage()

# def OnRefresh(event):
# 	# print(event)
# 	Update.light_control(event)

p = Process()



def AssignLayoutData(bt, kb, sq, en, jw):
	# print(kb)
	for k, v in bt.items():
		cl.buttonData[v['midi'][0]] = {}
		# cl.buttonData[v['midi'][3]] = {}

		# cl.buttonData[v[1][0]] = {}
	for k, v in bt.items():
		cl.buttonData[v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3]
			}

		# layout[str(v[1][0])][str(v[1][1])] = v[2]
		# layout[str(v[1][0])][str(v[1][1])] = v[2] 

		# layout[v[1][0]][v[1][1]] = v[2]
	for k, v in kb.items():
		cl.keyboardData[v['midi'][0]] = {}
		cl.keyboardData[v['midi'][3]] = {}
	for k, v in kb.items():
		cl.keyboardData[v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3]
			}
		cl.keyboardData[v['midi'][3]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3]
			}
	for k, v in sq.items():
		cl.sequencerData[v['midi'][0]] = {}
		cl.sequencerData[v['midi'][3]] = {}
	for k, v in sq.items():
		cl.sequencerData[v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3]
			}
		cl.sequencerData[v['midi'][3]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3]
			}
	# for k, v in kb.items():
	# 	cl.keyboardData[v[1][0]] = {}
	# for k, v in kb.items():
	# 	cl.keyboardData[v[1][0]][v[1][1]] = v[2]
	# for k, v in sq.items():
	# 	cl.sequencerData[v[1][0]] = {}
	# for k, v in sq.items():
	# 	cl.sequencerData[v[1][0]][v[1][1]] = v[2]
	# for k, v in en.items():
	# 	cl.encoderData[v[1][0]] = {}
	# for k, v in en.items():
	# 	cl.encoderData[v[1][0]][v[1][1]] = v[2]
	# for k, v in jw.items():
	# 	cl.jogData[v[1][0]] = {}
	# for k, v in jw.items():
	# 	cl.jogData[v[1][0]][v[1][1]] = {}
	# for k, v in jw.items():
	# 	cl.jogData[v[1][0]][v[1][1]][v[1][2]] = v[2]
	# print(cl.buttonData)
	# print(cl.sequencerData)
	print(cl.keyboardData)
	# print(cl.jogData)
