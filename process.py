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
from data import d
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
		self.midi_chan = self.event.midiChan + Config.CHANNEL_OFFSET
		midi_pair = [midi_id, data_1, self.midi_chan]
		print(midi_pair)
		if midi_pair in d["performanceData"]["midi_pairs"] and playlist.getPerformanceModeState() and ui.getFocused(midi.widPlaylist):
			print('performance') 
			if data_2 > 0:
				Action.performance_row = int(d["performanceData"][self.midi_chan][midi_id][data_1]["actions"][0])
				Main.set_track(d["performanceData"][self.midi_chan][midi_id][data_1])
				Action.trig_clip()
				self.event.handled = True
				# Main.transport_act(self, d.performanceData[self.midi_chan][midi_id][data_1]["actions"], Action.shift_status)
		elif midi_pair in d["keyboardData"]["midi_pairs"]and Modes.mode_active('Keyboard'):
			Keys.decide(self, d["keyboardData"][self.midi_chan][midi_id][data_1])
		elif midi_pair in d["sequencerData"]["midi_pairs"] and Modes.mode_active('Sequencer'):
			if d["sequencerData"][self.midi_chan][midi_id][data_1]["toggle"] or data_2 > 0:
				Sequencer.step_pressed(self, d["sequencerData"][self.midi_chan][midi_id][data_1])
		elif midi_pair in d["buttonData"]["midi_pairs"]:
			if (d["buttonData"][self.midi_chan][midi_id][data_1]["toggle"]) or data_2 > 0:
				Main.set_track(d["buttonData"][self.midi_chan][midi_id][data_1])
				Main.transport_act(self, d["buttonData"][self.midi_chan][midi_id][data_1]["actions"], Action.shift_status)
		elif midi_pair in d["encoderData"]["midi_pairs"]:
			Main.set_track(d["encoderData"][self.midi_chan][midi_id][data_1])
			Encoder.set(self, d["encoderData"][self.midi_chan][midi_id][data_1])
		elif midi_pair in d["jogData"]["midi_pairs"]:
			print('jog') 
			# data[self.midi_chan][self.event.data2]
			Encoder.jogWheel(self, d["jogData"][self.midi_chan][midi_id])
		else:
			self.event.handled = Config.PREVENT_PASSTHROUGH
			print('not set')

class Keys(Process):
	oct_iter = 2
	octave = [-36, -24, -12, 0, 12, 24, 36]
	def decide(self, data):
		print(f"keys d2: {self.event.midiId}")

		index = Notes.note_list.index(data["actions"][0])
		if Config.KEYBOARD_CHROMATIC:
			si =  Scales.scale_names.index("Chromatic")
			scale = Scales.scales[si]
			root = 0
		else:
			scale = Scales.scales[Scales.get_scale_choice()]
			root = Notes.get_root_note()
		note = scale[index] +  data["track"] * scale[12]  +  Action.get_octave() + 60 
		channels.midiNoteOn(self.channel, note, self.event.data2)
		# channels.midiNoteOn(channels.selectedChannel(), Notes.all_notes.index(act) + Action.get_octave() + 60, self.event.data2)
		# channels.midiNoteOn(channels.selectedChannel(), Notes.note_list.index(data["actions"][0]) + (data["track"] * 12) + Action.get_octave() + 60, self.event.data2)
		self.event.handled = True

	def play_note(self, data):
		channels.midiNoteOn(channels.selectedChannel(), Keys.notes.index(data) + 36, self.event.data2)

class Sequencer(Process):


	def step_pressed(self, data):
		act = data["actions"][Action.shift_status] 
		if act.isdigit():
			track = int(act) // cl["defaults"]["sequence_length"]
			print(f"track: {track}")
			print(int(act))
			step_num = Sequencer.get_step(int(act), cl["defaults"]["sequence_length"])
			chan = Sequencer.get_seq_channel(track, step_num)

			if channels.isGraphEditorVisible() and Config.SELECT_PARAM_STEP:
				Action.selected_step = step_num
				print('step_selected')
				self.event.handled = True
			else:
				Sequencer.set_step(self, step_num, chan) 
		else:
			track = data["track"]
			Main.set_track(data)
			Main.transport_act(self, data["actions"], Action.shift_status)

	def get_step(input, len):
		if input == 0:
			return 0
		else:
			return input % len
			
	def set_step(self, step, chan):
		# print(f"step: {step}")
		# print(f"chan: {chan}")
		if channels.getGridBit(chan, step) == 0:						
			channels.setGridBit(chan, step, 1)
			self.event.handled = True
		else:															
			channels.setGridBit(chan, step, 0)
			self.event.handled = True

	def get_seq_channel(track, step):
			# offset = int(step_num / cl["defaults"]["sequence_length"])
			# print(track)
			chan = channels.selectedChannel() + track
			return chan

	# def step_pressed(self, data):
	# 		print(data)
	# 		# seq_len = cl["defaults"]["sequence_length"]
	# 		s = int(data["actions"][0])
	# 		track = data["track"]
	# 		# step_num = (cl["defaults"]["sequence_length"] % s)
	# 		step_num = Sequencer.get_step(s, cl["defaults"]["sequence_length"])
	# 		# step_num = 0 if s == 0 else (cl["defaults"]["sequence_length"] % s)
	# 				# step_num = int(data["actions"][0]) - (cl["defaults"]["sequence_length"] * track)
	# 		print(step_num)
	# 		# if cl["defaults"]["seq_mult"]:
	# 		chan = Sequencer.get_seq_channel(track)
	# 		# else:
	# 		# 	chan = channels.selectedChannel()
	# 		if channels.isGraphEditorVisible() and Config.SELECT_PARAM_STEP:
	# 			Action.selected_step = step_num
	# 			self.event.handled = True
	# 		else:
	# 			# step = step_num % cl["defaults"]["sequence_multiple"][1]
	# 			Sequencer.set_step(self, step_num, chan) 

class Encoder(Process):

	def set(self, data):
		if ui.getFocused(5) and plugins.isValid(channels.channelNumber()) and cl["defaults"]["plugin_control"]:
			Encoder.control_plugin(self)
		else:		
			EncoderAction.call_func(data['actions'][Action.shift_status], self.event.data2)

	def set_data(d):
		if Config.FOLLOW_TRACK and mixer.trackNumber() != 0:
			track_offset = cl["defaults"]["mixer_tracks"] % mixer.trackNumber()
		else:
			track_offset = 0
		EncoderAction.track_number = d["track"] + track_offset

	def control_plugin(self):
		plugin = plugins.getPluginName(channels.selectedChannel())	
		param_count = plugins.getParamCount(channels.selectedChannel())
		if plugin in plg.plugin_dict:
			print('plugins')
			print(plg.knob_num)
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
		if data[self.event.data1].get(self.event.data2, {}):
			# print(data[self.event.data1][self.event.data2]['actions'])
			Main.transport_act(self, data[self.event.data1][self.event.data2]['actions'], Action.get_shift_status())
		# self.event.handled = True

		# if data[self.event.data1]['toggle']:
		# 	if self.event.data2 == data[self.event.data1]["midi_2"]:
		# 		Main.transport_act(self, data[self.event.data1]['actions'], Action.get_shift_status())
		# else:
		# 	Main.transport_act(self, data[self.event.data1]['actions'], Action.get_shift_status())
		# 	print('no track_offset')
		# if data.get(self.event.data2):
		# if Config.JOGWHEEL_USES_SAME_MIDI_CC:
		# 	print(data)
		# 	# Main.transport_act(self, data[self.event.data2][self.event.data1]['actions'], Action.get_shift_status())
		# 	Main.transport_act(self, data[self.event.data1][self.event.data2]['actions'], Action.get_shift_status())
		# else:
			# print(data[self.event.midiId][self.event.data1]['actions'])
		# Main.transport_act(self, data[self.event.midiId][self.event.data1]['actions'], Action.get_shift_status())

	def channel_link(cc):
		tracks = [i for i in range(0, 128)]
		if cc >= 65:
			if Encoder.link_chan > 0:
				Encoder.link_chan -= 1
		elif Encoder.link_chan < 127:
			Encoder.link_chan += 1
		return tracks[Encoder.link_chan]

class Main(Process):	

	def transport_act(self, offset_event, status):
		print(f"event: {offset_event[status]}")
		print(f"status: { Action.get_shift_status()}")
		Action.call_func(offset_event[status])
		if offset_event[status] != 'nothing':
			self.event.handled = True

	def set_track(data):
		# Action.track_number = data["track"]
		# if Config.FOLLOW_TRACK and mixer.trackNumber() != 0:
		# 	num_tracks = cl["defaults"]["mixer_tracks"]
		# 	n, d = divmod(mixer.trackNumber(), num_tracks)
		# 	if d == 0:
		# 		mult = (mixer.trackNumber() - 1) // num_tracks
		# 	else:
		# 		mult = mixer.trackNumber() // num_tracks

		# 	track_offset = mult * cl["defaults"]["mixer_tracks"]
		if Config.FOLLOW_TRACK and mixer.trackNumber() != 0:
			num_tracks = cl["defaults"]["mixer_tracks"]
			# this catches an issue when the selected track / mixer_tracks has 0 remainder
			mult = (mixer.trackNumber() - 1) // num_tracks if mixer.trackNumber() > 1 else 0
			track_offset = mult * num_tracks
		else:
			track_offset = 0
		Action.track_number = data["track"] + track_offset 
		Action.track_original = data["track"]
		# print(f"Action.track_original: {Action.track_original}")

