# name=No Default 
# Author: forgery810
# VERSION = '0.1.8'

import device
import channels
from midi import *
import midi
import mixer
import patterns
import channels
import ui
import transport
from leds import Leds
from process import Process, Dispatch, Main
from modes import Modes
from notes import Notes, Scales
from data import d
from config import Config
from config_layout import cl  
import plugindata as plg
import time
from action import Action
import plugindata

def OnInit():
	"""Function called when script starts"""

	AssignLayoutData(cl["buttons"], cl["keyboard"], cl["sequencer"], cl["encoders"], cl["jog_wheel"], cl["defaults"], cl["performance"])
	AssignLeds(cl["leds"])
	Leds.led_setup()
	print(device.getName())
	
	if device.isAssigned():		
		print(f"Layout: {cl['name']}")		
		print("Assigned")
		print(f"Port Number: {device.getPortNumber()}")
	else:
		print("Not assigned. In the MIDI settings, set the Input and Output Ports to the same number for this device.")


if Config.PATTERN_CHANGE_WAIT:
	def OnUpdateBeatIndicator(e):
		if e == 1:
			if patterns.patternNumber() != Action.new_pattern_number:
				patterns.jumpToPattern(Action.track_original)
				Action.new_pattern_number = patterns.patternNumber()

def OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""

	print(event.midiId, event.data1, event.data2, event.midiChan, event.midiChanEx, event.timestamp)

	p.event = event
	p.channel = channels.selectedChannel()
	p.track = mixer.trackNumber()
	p.pattern = patterns.patternNumber()
	p.d2 = event.data2
	p.triage()

def OnRefresh(event):
	# print(f"Refresh Event: {event}")
	print(Leds.leds_assigned())
	if Leds.leds_assigned():
		Leds.check_event_leds(event)
	
p = Process()

def AssignLayoutData(bt, kb, sq, en, jw, df, pf):
	"""converts dict from config_layout to one that is easier for processing"""


	# def process_data(data, key_prefix):
	# 	d[key_prefix] = {}
	# 	for v in data.values():
	# 		print(v)
	# 		d[key_prefix][v['channel']] = {}
	# 		d[key_prefix][v['channel']][v['midi'][0]] = {}
	# 		d[key_prefix][v['channel']][v['midi'][0]][v['midi'][1]] = {
	# 			'actions': v['actions'],
	# 			'channel': v['channel'],
	# 			'toggle': v['toggle'],
	# 			'track': v['track'],}

	#         # d[key_prefix]['midi_pairs'].append(v['midi'])
	# process_data(bt, 'buttonData')
	# process_data(kb, 'keyboardData')
	# process_data(sq, 'sequencerData')
	# process_data(en, 'encoderData')
	# process_data(pf, 'performanceData')
	# process_data(jw, 'jogData')

	def process_data(data, key_name):
		for v in data.values():
			d[key_name][v['channel']] = {}	
		for v in data.values():
			d[key_name][v['channel']][v['midi'][0]] = {}	
		for v in data.values():
			d[key_name]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
			d[key_name][v['channel']][v['midi'][0]][v['midi'][1]] = {
				'actions': v['actions'],
				'channel': v['channel'],
				'toggle': v['toggle'],
				'release': v['midi'][3],
				'track': v['track']
			}
			d[key_name]['midi_pairs'].append(v['midi'])


	process_data(bt, 'buttonData')
	process_data(kb, 'keyboardData')
	process_data(sq, 'sequencerData')
	process_data(en, 'encoderData')
	process_data(pf, 'performanceData')
	process_data(jw, 'jogData')

	print(d)
	# for v in bt.values():
	# 	d.buttonData[v['channel']] = {}	
	# for v in bt.values():
	# 	d.buttonData[v['channel']][v['midi'][0]] = {}	
	# for v in bt.values():
	# 	d.buttonData['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
	# 	d.buttonData[v['channel']][v['midi'][0]][v['midi'][1]] = {
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		'release': v['midi'][3],
	# 		'track': v['track']
	# 	}
	# print(d)
	# for v in kb.values():
	# 	d.keyboardData[v['channel']] = {}	
	# for v in kb.values():
	# 	d.keyboardData[v['channel']][v['midi'][0]] = {}	
	# 	d.keyboardData[v['channel']][v['midi'][3]] = {}	
	# for v in kb.values():
	# 	d.keyboardData['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
	# 	d.keyboardData[v['channel']][v['midi'][0]][v['midi'][1]] = {
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		'release': v['midi'][3],
	# 		'track': v['track']
	# 	}
	# for v in kb.values():
	# 	d.keyboardData['midi_pairs'].append([ v['midi'][3], v['midi'][1], v['channel'] ])	
	# 	d.keyboardData[v['channel']][v['midi'][3]][v['midi'][1]] = {
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		'release': v['midi'][3],
	# 		'track': v['track']
	# 	}

	# for v in sq.values():
	# 	d.sequencerData[v['channel']] = {}	
	# for v in sq.values():
	# 	d.sequencerData[v['channel']][v['midi'][0]] = {}	
	# for v in sq.values():
	# 	d.sequencerData['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
	# 	d.sequencerData[v['channel']][v['midi'][0]][v['midi'][1]] = {
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		'release': v['midi'][3],
	# 		'track': v['track']
	# 	}

	# for v in en.values():
	# 	d.encoderData[v['channel']] = {}	
	# for v in en.values():
	# 	d.encoderData[v['channel']][v['midi'][0]] = {}	
	# 	plugindata.knob_num.append(v['midi'][1])
	# for v in en.values():
	# 	d.encoderData['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
	# 	d.encoderData[v['channel']][v['midi'][0]][v['midi'][1]] = {
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		# 'release': v['midi'][3],
	# 		'track': v['track']
	# 	}


	# for v in pf.values():
	# 	d.performanceData[v['channel']] = {}	
	# for v in pf.values():
	# 	d.performanceData[v['channel']][v['midi'][0]] = {}	
	# for v in pf.values():
	# 	d.performanceData['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
	# 	d.performanceData[v['channel']][v['midi'][0]][v['midi'][1]] = {
	# 		'actions': v['actions'],
	# 		'channel': v['channel'],
	# 		'toggle': v['toggle'],
	# 		# 'release': v['midi'][3],
	# 		'track': v['track']
	# 	}

	# for v in jw.values():
	# 	d.jogData[v['channel']] = {}	
	# for v in jw.values():
	# 	if Config.JOGWHEEL_USES_SAME_MIDI_CC:
	# 		d.jogData[v['channel']][v['midi'][2]] = {}	
	# 	else:
	# 		d.jogData[v['channel']][v['midi'][0]] = {}	
	# for v in jw.values():
	# 	d.jogData['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])
	# 	if Config.JOGWHEEL_USES_SAME_MIDI_CC:
	# 		d.jogData[v['channel']][v['midi'][2]][v['midi'][1]] = {
	# 			'actions': v['actions'],
	# 			'channel': v['channel'],
	# 			'toggle': v['toggle'],
	# 			'release': v['midi'][3],
	# 			'track': v['track']
	# 		}
	# 	else:	
	# 		d.jogData[v['channel']][v['midi'][0]][v['midi'][1]] = {
	# 			'actions': v['actions'],
	# 			'channel': v['channel'],
	# 			'toggle': v['toggle'],
	# 			'release': v['midi'][3],
	# 			'track': v['track']
	# 		}

	# if cl["defaults"]["Keyboard"]:
	# 	Modes.remove_mode("Keyboard")
	# if cl["defaults"]["Sequencer"]:
	# 	Modes.remove_mode("Sequencer")	
	# plg.knob_num = sorted(set(plg.knob_num))
	# Scales.set_scale_by_name(cl["defaults"]["scale"])

	# print(plugindata.knob_num)
	# print(d.encoderData)

	# print(d.sequencerData)
	# print(d.keyboardData)
	# print(d.performanceData)
	# print(d.defaults)
	# print(d.jogData)
	# print(Modes.modes)

def AssignLeds(led):

	if cl["leds"]["transport_leds"]:
		Modes.set_transport_leds(True)
		if Config.CHANNEL_OFFSET:
			for v in cl["leds"]["transport_leds"].values():
					v[1] -=  Config.CHANNEL_OFFSET;
		d["ledData"]["transport"] = cl["leds"]["transport_leds"]
# 
	if cl["leds"]["seq_leds"]:
		if Config.CHANNEL_OFFSET:
			for v in cl["leds"]["seq_leds"].values():
					v[1] -= Config.CHANNEL_OFFSET;
		Modes.set_seq_leds(True)
		d["ledData"]["seq"] = cl["leds"]["seq_leds"]
	
def OnDeInit():
	print('OnDeInit')
	# Leds.all_off()
