# name=No Default 
# Author: forgery810
# VERSION = '0.1.8'

from config_layout import cl  
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
import plugindata as plg
# import time
from action import Action
import plugindata

def OnInit():
	"""Function called when script starts"""

	AssignLayoutData(cl["button"], cl["keyboard"], cl["sequencer"], cl["encoder"], cl["jogwheel"], cl["defaults"], cl["performance"])
	AssignLeds(cl["led"])
	Leds.led_setup()
	print(device.getName())
	
	if device.isAssigned():		
		print(f"Assigned. Layout: {cl['name']}")		
		print(f"Port Number: {device.getPortNumber()}")
	else:
		print("Not assigned. In the MIDI settings, set the Input and Output Ports to the same number for this device.")


if Config.PATTERN_CHANGE_WAIT:
	def OnUpdateBeatIndicator(e):
		if e == 1:
			if Config.PATTERN_CHANGE_WAIT and Action.change_pattern:
				patterns.jumpToPattern(Action.track_original)
				Action.change_pattern = False
 
def OnMidiMsg(event):
	"""Function called on every midi message sent by controller"""

	print(event.midiChan, event.midiId, event.data1, event.data2, event.midiChanEx, event.timestamp)

	p.event = event
	p.channel = channels.selectedChannel()
	p.track = mixer.trackNumber()
	p.pattern = patterns.patternNumber()
	p.d2 = event.data2
	p.triage()

# if Config.PITCH_BEND:
# 	def OnPitchBend(event):
# 		pass
		# EncoderAction.pitch_bend(event.data2)

def OnRefresh(event):
	# print(f"Refresh Event: {event}")
	if Leds.leds_assigned():
		Leds.check_event_leds(event)
	if event == 1024:
		Action.old_pattern_number = patterns.patternNumber()
	
p = Process()

def AssignLayoutData(bt, kb, sq, en, jw, df, pf):
	"""converts dict from config_layout to one that is easier for processing"""

	def process_data(data, key_name):
		for v in data.values():
			d[key_name][v['channel']] = {}	
			d[key_name][v['channel']] = {}	
		for v in data.values():
			d[key_name][v['channel']][v['midi'][0]] = {}	
		for v in data.values():
			d[key_name]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
			d[key_name][v['channel']][v['midi'][0]][v['midi'][1]] = {
				'actions': v['actions'],
				'channel': v['channel'],
				'midi_2': v['midi'][2],
				'toggle': v['toggle'],
				# 'release': v['midi'][3],
				'track': v['track']
			}
		if key_name == "jogData":
			for v in data.values():
				d[key_name][v['channel']][v['midi'][0]][v['midi'][1]] = {
					'midi_2': v['midi'][2]
				}
		d[key_name]['midi_pairs'].append(v['midi'])


	def process_jog_data(jw, jogData):
		for k, v in jw.items():
			d["jogData"][v["channel"]] = {}
		for k, v in jw.items():
			d["jogData"][v["channel"]][v['midi'][0]] = {}
			# d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]] = {} 
		for k, v in jw.items():
			d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]] = {} 
			d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]][v['midi'][2]] = {}
			# d["jogData"][v["channel"]]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
		for k, v in jw.items():
			d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]][v['midi'][2]] = { 
				'actions': v['actions'],
				'channel': v['channel'],
				'toggle': v['toggle'],
				'release': v['midi'][3],
				'midi_2': v['midi'][2]
				}
			d["jogData"]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
			# d["jogData"]['midi_pairs'].append([v['midi'][0:2], v['channel']])





	process_data(bt, 'buttonData')
	process_data(kb, 'keyboardData')
	process_data(sq, 'sequencerData')
	process_data(en, 'encoderData')
	process_data(pf, 'performanceData')
	process_jog_data(jw, 'jogData')
	# print(d["buttonData"]["midi_pairs"])



# 	# for k, v in jw.items():
# 	# 	d.jogData[v['midi'][0]] = {}
# 	# 	d.jogData[v['midi'][0]][v['midi'][1]] = {} 
# 	# for k, v in jw.items():
# 	# 	d.jogData[v['midi'][0]][v['midi'][1]][v['midi'][2]] = { 
# 	# 		'actions': v['actions'],
# 	# 		'channel': v['channel'],
# 	# 		'toggle': v['toggle'],
# 	# 		'release': v['midi'][3],
# 	# 		'midi_2': v['midi'][2]
# 	# 		}



# 	# print(d)
# 	# print(plugindata.knob_num)
# 	# print(d.encoderData)

# 	# print(d.sequencerData)
# 	# print(d.keyboardData)
# 	# print(d.performanceData)
# 	# print(d.defaults)
# 	# print(d.jogData)
# 	# print(Modes.modes)

transport_leds = ['shift', 'start', 'stop', 'record']

def AssignLeds(led):

	for v in cl["led"].values():
		Leds.active_leds.add(v["actions"][0])
		if v["actions"][0] in transport_leds:
			d["leds"]["transport_leds"][v["actions"][0]] = [v["midi"][0], v["channel"] - 1, v["midi"][1]]
			Modes.set_transport_leds(True)
			
		else:
			d["leds"]["seq_leds"][v["actions"][0]] = [v["midi"][0], v["channel"] - 1, v["midi"][1]]
			Modes.set_seq_leds(True)
			
			# d.leds["seq_leds"].append(v)
			# Leds.active_leds.append(k)
	# print(Leds.active_leds)
	print(Leds.active_leds)

	# if cl["leds"].get("transport_leds", {}):	
	# 	for k in cl["leds"]["transport_leds"]:
	# 		Leds.active_leds.append(k)
	# if cl["leds"].get('seq_leds'):
	# 	Leds.active_leds.append('seq_leds')

# 	if cl["leds"]["transport_leds"]:
# 		if Config.CHANNEL_OFFSET:
# 			for v in cl["leds"]["transport_leds"].values():
# 					v[1] -=  Config.CHANNEL_OFFSET;
# 		d["ledData"]["transport"] = cl["leds"]["transport_leds"]
# # 
# 	if cl["leds"]["seq_leds"]:
# 		if Config.CHANNEL_OFFSET:
# 			for v in cl["leds"]["seq_leds"].values():
# 					v[1] -= Config.CHANNEL_OFFSET;
# 		d["ledData"]["seq"] = cl["leds"]["seq_leds"]


# def OnDeInit():
# 	print('OnDeInit')
