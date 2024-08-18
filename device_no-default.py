# name=No Default 
# Author: forgery810
VERSION = '0.8.1'

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
from process import Process,  Main
from modes import Modes
from notes import Notes, Scales
from data import d
from config import Config
import plugindata as plg
from action import Action, EncoderAction
import plugindata
import itertools

def OnInit():
	"""Function called when script starts"""

	AssignLayoutData(cl["button"], cl["keyboard"], cl["sequencer"], cl["encoder"], cl["jogwheel"], cl["defaults"], cl["performance"])
	AssignLeds(cl["led"])
	Leds.led_setup()
	print(device.getName())
	print(f"Script Version: {VERSION}")
	
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

if Config.PITCH_BEND:
	def OnPitchBend(event):
		EncoderAction.pitch_bend(event.data2)
		event.handled = True

def OnRefresh(event):
	# print(f"Refresh Event: {event}")
	if Leds.leds_assigned():
		Leds.check_event_leds(event)
	if event == 1024:
		Action.old_pattern_number = patterns.patternNumber()
	
p = Process()

def AssignLayoutData(bt, kb, sq, en, jw, df, pf):

	def process_data(data, key_name):
		"""converts dict from the the easier to edit config_layout to one that is designed for processing efficiently"""
		try:
			for v in data.values():
				d[key_name][v['channel']] = {}	
				d[key_name][v['channel']] = {}	
			for v in data.values():
				d[key_name][v['channel']][v['midi'][0]] = {}	
				d[key_name][v['channel']][v['midi'][3]] = {}	
			for v in data.values():
				d[key_name]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])	
				if key_name == 'keyboardData':
					d[key_name]['midi_pairs'].append([ v['midi'][3], v['midi'][1], v['channel'] ])	
	
				d[key_name][v['channel']][v['midi'][3]][v['midi'][1]] = {
					'actions': v['actions'],
					'channel': v['channel'],
					'midi_2': v['midi'][2],
					'toggle': v['toggle'],
					# 'release': v['midi'][3],
					'track': v['track']
				}
				d[key_name][v['channel']][v['midi'][0]][v['midi'][1]] = {
					'actions': v['actions'],
					'channel': v['channel'],
					'midi_2': v['midi'][2],
					'toggle': v['toggle'],
					# 'release': v['midi'][3],
					'track': v['track']
				}
		except (KeyError, TypeError, ValueError) as e:
			print(f"An error occured: {e}")

	

	def process_jog_data(jw, jogData):
		""" jog wheel must have its own function as it requires the midi_2 data to be a key"""
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

	def process_encoders_for_plugins(data):
		for v in data.values():
			plg.knob_num.append(v["midi"][1])

	def process_colors(color_list):
		if color_list:
			d["colors"] = itertools.cycle(color_list)

	process_data(bt, 'buttonData')
	process_data(kb, 'keyboardData')
	process_data(sq, 'sequencerData')
	process_data(en, 'encoderData')
	process_encoders_for_plugins(en)
	process_data(pf, 'performanceData')
	process_jog_data(jw, 'jogData')
	process_colors(cl["defaults"]["colors"])

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
