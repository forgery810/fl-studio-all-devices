# name=No Default 
# Author: forgery810
# VERSION = '0.1.5'

import device
import channels
from midi import *
import midi
import mixer
import patterns
import channels
import transport
from leds import Leds
from process import Process, Dispatch, Main
from modes import Modes
from notes import Notes
import data as d
from config import Config
from config_layout3 import cl  
import plugindata as plg

def OnInit():
	"""Function called when script starts"""

	AssignLayoutData(cl["buttons"], cl["keyboard"], cl["sequencer"], cl["encoders"], cl["jog_wheel"], cl["defaults"], cl["performance"])
	AssignLeds(cl["leds"])
	Leds.led_setup()
	print(device.getName())
	
	if device.isAssigned():		
		# AssignLayoutData(cl["buttons"], cl["keyboard"], cl["sequencer"], cl["encoders"], cl["jog_wheel"], cl["defaults"])
		print("Assigned")
		print(f"Port Number: {device.getPortNumber()}")
	else:
		print("Not assigned. In the MIDI settings, set the Input and Output Ports to the same number for this device.")

def  OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""

	# print(scriptData)
	print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx, event.timestamp)

	p.event = event
	p.channel = channels.selectedChannel()
	p.track = mixer.trackNumber()
	p.pattern = patterns.patternNumber()
	p.d2 = event.data2
	p.triage()

def OnRefresh(event):
	# print(f"Refresh Event: {event}")
	if Leds.leds_assigned():
		Leds.check_event_leds(event)

p = Process()

def AssignLayoutData(bt, kb, sq, en, jw, df, pf):
	"""converts dict from config_layout to one that is easier for processing"""
	# d.buttonData = {
	#     v['channel']: {
	#         v['midi'][0]: {
	#             v['midi'][1]: {
	#                 'actions': v['actions'],
	#                 'channel': v['channel'],
	#                 'toggle': v['toggle'],
	#                 'release': v['midi'][3],
	#                 'track': v['track']
	#             }
	#         }
	#     }
	#     for k, v in bt.items()
	# }
	# d.buttonData = {
	# 	v['channel']: 
	# 		{v['midi'][0]: {
	# 		}
	# 	} for k, v, in bt.items()
	# }
	# for k, v in bt.items():
	# 	d.buttonData[v['channel']] = {}
	for k, v in bt.items():
		d.buttonData[v['channel']] = {}	
	for k, v in bt.items():
		d.buttonData[v['channel']][v['midi'][0]] = {

		}	
	for k, v in bt.items():
		d.buttonData[v['channel']][v['midi'][0]][v['midi'][1]] = {
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3],
			'track': v['track']
		}	
	print(d.buttonData)
	# for k, v in bt.items():
	# 	d.buttonData[v['channel']][v['midi'][0]] = {}
	# for k, v in bt.items():
	# 	d.buttonData[v['channel']][v['midi'][0]][v['midi'][1]] = {}
	# for k, v in bt.items():
	# 	d.buttonData[v['channel']][v['midi'][0]][v['midi'][1]] = { 
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		'release': v['midi'][3],
	# 		'track': v['track']
	# 		}
	d.keyboardData = {
		v['channel']: 
			{v['midi'][0]: {
			}
		} for k, v, in kb.items()
	}
	for k, v in kb.items():
		d.keyboardData[v['channel']][v['midi'][0]][v['midi'][1]] = {}
	# 	d.buttonData[v['midi'][0]] = {}
	# for k, v in bt.items():
	# 	d.buttonData[v['midi'][0]][v['midi'][1]] = { 
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		'release': v['midi'][3],
	# 		'track': v['track']
	# 		}
	# for v in kb.values():
	# 	d.keyboardData[v['midi'][0]] = {}
	# 	d.keyboardData[v['midi'][3]] = {}
	for k, v in sq.items():
		d.keyboardData[v['channel']][v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3],
			'track': v['track']
			}
		d.keyboardData[v['channel']][v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3],
			'track': v['track']
			}
	d.sequencerData = {
		v['channel']: 
			{v['midi'][0]: {
			}
		} for k, v, in bt.items()
	}
	for k, v in sq.items():
		d.sequencerData[v['channel']][v['midi'][0]][v['midi'][1]] = {}
	# for k, v in sq.items():
	# 	d.sequencerData[v['midi'][0]] = {}
	# 	d.sequencerData[v['midi'][3]] = {}
	for k, v in sq.items():
		d.sequencerData[v['channel']][v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3],
			'track': v['track']
			}
		d.sequencerData[v['channel']][v['midi'][3]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3],
			'track': v['track']
			}
	# for k, v in en.items():
	# 	d.encoderData[v['midi'][0]] = {}
	d.encoderData = {
		v['channel']: 
			{v['midi'][0]: {
			}
		} for k, v, in en.items()
	}
	for k, v in en.items():
		plg.knob_num.append(v['midi'][1])
		d.encoderData[v['channel']][v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3],
			'track': v['track']
			}
	# d.jogData = {
	# 	v['channel']: 
	# 		{v['midi'][0]: {
	# 		}
	# 	} for k, v, in jw.items()
	# }
	# # for k, v in jw.items():
	# # 	d.jogData[v['midi'][0]] = {}
	# # 	d.jogData[v['midi'][0]][v['midi'][1]] = {} 
	# for k, v in jw.items():
	# 	d.jogData[v['channel']][v['midi'][0]][v['midi'][1]][v['midi'][2]] = { 
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		'release': v['midi'][3],
	# 		'midi_2': v['midi'][2],
	# 		'track': v['track']
	# 		}
	if cl["defaults"]["Keyboard"]:
		Modes.remove_mode("Keyboard")
	if cl["defaults"]["Sequencer"]:
		Modes.remove_mode("Sequencer")	
	plg.knob_num = sorted(set(plg.knob_num))

	d.performanceData = {
		v['channel']: 
			{v['midi'][0]: {
			}
		} for k, v, in pf.items()
	}
	# for k, v in bt.items():
	# 	d.buttonData[v['channel']] = {}
	# for k, v in bt.items():
	# 	d.buttonData[v['channel']][v['midi'][0]] = {}
	for k, v in pf.items():
		d.performanceData[v['channel']][v['midi'][0]][v['midi'][1]] = {}
	for k, v in pf.items():
		d.performanceData[v['channel']][v['midi'][0]][v['midi'][1]] = { 
			'actions': v['actions'],
			'channel': v['channel'],
			'toggle': v['toggle'],
			'release': v['midi'][3],
			'track': v['track']
			}
	print(d.encoderData)
	print(d.sequencerData)
	print(d.keyboardData)
	print(d.performanceData)
	# print(d.defaults)
	print(d.buttonData)
	print(Modes.modes)


def AssignLeds(led):
	d.ledData = {
		v['actions'][0]: 
			[v['midi'][0], v['channel']- 1, v['midi'][1]
		] for k, v, in led.items()
	}
	
def OnDeInit():
	Leds.all_off()
