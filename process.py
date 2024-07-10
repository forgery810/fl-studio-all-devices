from action import Action, EncoderAction
import transport
import channels
import ui 
import device
import mixer 
import channels 
import playlist
import plugins
import patterns
from utility import Utility
import midi
import data as d
from config import Config
from config_layout import cl
import plugindata as plg
from notes import Notes, Scales
from modes import Modes

class Dispatch:
	def __init__(self):
		self.chan_ex = 0
		self.channel = channels.selectedChannel()
		self.pattern = patterns.patternNumber()
		self.random_offset = 63

class Process(Dispatch):

	def triage(self):
		midi_id = self.event.midiId
		data_1 = self.event.data1
		data_2 = self.event.data2
		if d.keyboardData.get(midi_id, {}).get(data_1) and Modes.mode_active('Keyboard'):
				Keys.decide(self, d.keyboardData[midi_id][data_1])
		elif d.sequencerData.get(midi_id, {}).get(data_1) and Modes.mode_active('Sequencer'):
			if data_2 > 0 or d.sequencerData.get(midi_id, {}).get(data_1)["toggle"]:
				Sequencer.step_pressed(self, d.sequencerData[midi_id][data_1])
		elif d.buttonData.get(midi_id, {}).get(data_1):	
			if data_2 > 0:
				Main.set_track(d.buttonData[midi_id][data_1])
				Main.transport_act(self, d.buttonData[midi_id][data_1]["actions"], Action.shift_status)
		elif d.encoderData.get(midi_id, {}).get(data_1):
			Encoder.set_data(d.encoderData[midi_id][data_1])
			Encoder.set(self, d.encoderData[midi_id][data_1])
		elif d.jogData.get(midi_id, {}.get(data_1)):
			if (d.jogData[midi_id].get(data_1)):
				Encoder.jogWheel(self, d.jogData[midi_id].get(data_1))
		else:
			self.event.handled = True
			print('not set')

class Keys(Process):

	oct_iter = 2
	octave = [-36, -24, -12, 0, 12, 24, 36]
	notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
	def decide(self, data):
		# channels.midiNoteOn(channels.selectedChannel(), Notes.all_notes.index(act) + Action.get_octave() + 60, self.event.data2)
		channels.midiNoteOn(channels.selectedChannel(), Notes.note_list.index(data["actions"][0]) + (data["track"] * 12) + Action.get_octave() + 60, self.event.data2)
		self.event.handled = True
		# channels.midiNoteOn(channels.selectedChannel(), Keys.notes.index(data) + Action.get_octave() + 60, 127)

	def play_note(self, data):
		channels.midiNoteOn(channels.selectedChannel(), Keys.notes.index(data) + 36, self.event.data2)

class Sequencer(Process):

	def step_pressed(self, data):
		print(data)
		# seq_len = cl["defaults"]["sequence_length"]
		s = int(data["actions"][0])
		track = data["track"]
		# step_num = (cl["defaults"]["sequence_length"] % s)
		step_num = Sequencer.get_step(s, cl["defaults"]["sequence_length"])
		# step_num = 0 if s == 0 else (cl["defaults"]["sequence_length"] % s)
				# step_num = int(data["actions"][0]) - (cl["defaults"]["sequence_length"] * track)
		print(step_num)
		# if cl["defaults"]["seq_mult"]:
		chan = Sequencer.get_seq_channel(track)
		# else:
		# 	chan = channels.selectedChannel()
		if channels.isGraphEditorVisible() and Config.SELECT_PARAM_STEP:
			Action.selected_step = step_num
			self.event.handled = True
		else:
			# step = step_num % cl["defaults"]["sequence_multiple"][1]
			Sequencer.set_step(self, step_num, chan) 

	def get_step(input, len):
		if input == 0:
			return 0
		else:
			return input % len


	def set_step(self, step, chan):
		if channels.getGridBit(chan, step) == 0:						
			channels.setGridBit(chan, step, 1)
			self.event.handled = True
		else:															
			channels.setGridBit(chan, step, 0)
			self.event.handled = True

	def get_seq_channel(track):
			# offset = int(step_num / cl["defaults"]["sequence_length"])
			chan = channels.selectedChannel() + track
			return chan

class Encoder(Process):

	def set(self, data):
		if ui.getFocused(5) and plugins.isValid(channels.channelNumber()) and cl["defaults"]["plugin_control"]:
			Encoder.control_plugin(self)

		elif data['actions'][Action.shift_status][0:12] == 'mixer_level(':
			track = int(data['actions'][Action.shift_status][12:15])
			Encoder.mixer_level(self.event.data2, track)
 
		elif data['actions'][Action.shift_status][0:10] == 'mixer_pan(':
			track = int(data['actions'][Action.shift_status][10:13])
			Encoder.mixer_panning(self.event.data2, track)
		else:			
			EncoderAction.call_func(data['actions'][Action.shift_status], self.event.data2)

	def set_data(d):
		EncoderAction.track_number = d["track"] 

	def control_plugin(self):
		plugin = plugins.getPluginName(channels.selectedChannel())	
		param_count = plugins.getParamCount(channels.selectedChannel())
		if plugin in plg.plugin_dict:
			param = plg.plugin_dict[plugin][plg.knob_num.index(self.event.data1)]
			param_value =  self.event.data2/127 #Utility.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()), .025)		                                                                           																		
			plugins.setParamValue(param_value, param, channels.selectedChannel())
			self.event.handled = True
	
		else:	
			param = self.event.data1 - 15
			# param_value =  Utility.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()), .025)	
			plugins.setParamValue(self.event.data2/127, param, self.channel)
			self.event.handled = True

	def jogWheel(self, data):
		if data.get(self.event.data2):
			Main.transport_act(self, data[self.event.data2]['actions'], 0, 0)


	def channel_link(cc):
		print(cc)
		tracks = [i for i in range(0, 128)]
		if cc >= 65:
			if Encoder.link_chan > 0:
				Encoder.link_chan -= 1
		elif Encoder.link_chan < 127:
			Encoder.link_chan += 1
		return tracks[Encoder.link_chan]

class Main(Process):	

	def transport_act(self, offset_event, status):
		print(f"event: {offset_event[0]}")
		# print(offset_event[0] in Notes.all_notes)
		# if offset_event[0] in Notes.all_notes:
			# Keys.decide(self, offset_event[0], data)
		# else:
			# Action.call_func(offset_event[status])
		Action.call_func(offset_event[status])
		self.event.handled = True

	def set_track(data):
		Action.track_number = data["track"]


