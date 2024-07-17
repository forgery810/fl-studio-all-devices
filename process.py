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
		midi_chan = self.event.midiChan + Config.CHANNEL_OFFSET
		if playlist.getPerformanceModeState() and d.performanceData.get(midi_chan, {}).get(midi_id).get(data_1) and ui.getFocused(widPlaylist):
			print('performance')
			if data_2 > 0:
				Action.performance_row = int(d.performanceData[midi_chan][midi_id][data_1]["actions"][0])
				Main.set_track(d.performanceData[midi_chan][midi_id][data_1])
				Action.trig_clip()
				# Main.transport_act(self, d.performanceData[midi_chan][midi_id][data_1]["actions"], Action.shift_status)
		elif d.keyboardData.get(midi_id, {}).get(data_1) and Modes.mode_active('Keyboard'):
				Keys.decide(self, d.keyboardData[midi_id][data_1])
		elif d.sequencerData.get(midi_id, {}).get(data_1) and Modes.mode_active('Sequencer'):
			if data_2 > 0 or d.sequencerData.get(midi_id, {}).get(data_1)["toggle"]:
				Sequencer.step_pressed(self, d.sequencerData[midi_id][data_1])
		elif d.buttonData.get(midi_chan, {}).get(midi_id).get(data_1):	
				Main.set_track(d.buttonData[midi_chan][midi_id][data_1])
				Main.transport_act(self, d.buttonData[midi_chan][midi_id][data_1]["actions"], Action.shift_status)
		elif d.encoderData.get(midi_chan, {}).get(midi_id).get(data_1):
			Main.set_track(d.encoderData[midi_chan][midi_id][data_1])
			Encoder.set(self, d.encoderData[midi_chan][midi_id][data_1])
		elif d.jogData.get(midi_chan, {}).get(midi_id).get(data_1):
			if (d.jogData[midi_id].get(data_1)):
				Encoder.jogWheel(self, d.jogData[midi_chan][midi_id].get(data_1))
		else:

			self.event.handled = Config.PREVENT_PASSTHROUGH
			print('not set')

class Keys(Process):

	oct_iter = 2
	octave = [-36, -24, -12, 0, 12, 24, 36]
	def decide(self, data):
		index = Notes.note_list.index(data["actions"][0])
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
		else:			
			EncoderAction.call_func(data['actions'][Action.shift_status], self.event.data2)

	def set_data(d):
		if Config.FOLLOW_TRACK and  mixer.trackNumber() != 0:
			track_offset = cl["defaults"]["mixer_tracks"] % mixer.trackNumber()
		else:
			track_offset = 0
		EncoderAction.track_number = d["track"] + track_offset

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
		Action.call_func(offset_event[status])
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
		# print(f"Action.track_num: {Action.track_number}")

