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
				Keys.decide(self, d.keyboardData[midi_id][data_1]["actions"][0])
		elif d.sequencerData.get(midi_id, {}).get(data_1) and Modes.mode_active('Sequencer'):
			if data_2 > 0 or d.sequencerData.get(midi_id, {}).get(data_1)["toggle"]:
				Sequencer.step_pressed(self, d.sequencerData[midi_id][data_1]["actions"][0])
		elif d.buttonData.get(midi_id, {}).get(data_1):	
			if data_2 > 0:
				Main.transport_act(self, d.buttonData[midi_id][data_1]["actions"], Action.shift_status, d.buttonData[midi_id][data_1])
		elif d.encoderData.get(midi_id, {}).get(data_1):
			Encoder.set(self, d.encoderData[midi_id][data_1]);
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
	def decide(self, act):
		# if Mode.get_layer() == 0:
		# Keys.play_note(act)
		# # print(f"data: {data}")
		# if self.event.data2 == 0:
		# 	# print(f"act: {act}") 
		# 	# print(f"notes.index: {Notes.all_notes.index(act)}") 
		# 	channels.midiNoteOn(channels.selectedChannel(), 
								#Notes.all_notes.index(act) + Action.get_octave() + 60, 0)
		# else:
		# 	# print(Keys.notes.index(act) + Action.get_octave() + 60)
		channels.midiNoteOn(	channels.selectedChannel(), 
								Notes.all_notes.index(act) + Action.get_octave() + 60, 
								self.event.data2)
		self.event.handled = True
		# channels.midiNoteOn(channels.selectedChannel(), Keys.notes.index(data) + Action.get_octave() + 60, 127)


		# 	if str(self.event.data1) in self.xt.key_dict.keys():
		# 		Keys.play_note(self)
		# 		self.event.handled = True

		# 	elif self.event.data2 > 0:
		# 		if self.event.data1 == self.xt.lower_octave  and self.event.midiId == 144:
		# 			Keys.oct_iter -= 1
		# 			if Keys.oct_iter < 0:
		# 				Keys.oct_iter = len(Keys.octave) - 1
		# 			self.event.handled = True

		# 		elif self.event.data1 == self.xt.raise_octave and self.event.midiId == 144:
		# 			Keys.oct_iter += 1
		# 			if Keys.oct_iter == len(Keys.octave):
		# 				Keys.oct_iter = 0
		# 			self.event.handled = True

		# 		elif self.event.data1 == self.xt.key_blank and self.event.midiId == 144:
		# 			Action.record()
		# 			self.event.handled = True

		# elif Mode.get_layer() == 1:
		# 	channels.midiNoteOn(channels.selectedChannel(), Scales.scales[Scales.get_scale_choice()][self.xt.buttons.index(self.event.data1) + 24 + Notes.get_root_note()], self.event.data2)
		# 	self.event.handled = True

	def play_note(self, data):
		# channels.midiNoteOn(channels.selectedChannel(), self.xt.key_dict[str(self.event.data1)] + Keys.octave[Keys.oct_iter], self.event.data2)
		channels.midiNoteOn(channels.selectedChannel(), Keys.notes.index(data) + 36, self.event.data2)

class Sequencer(Process):

	def step_pressed(self, data):
		step_num = int(data)
		if cl["defaults"]["sequence_multiple"][0]:
			chan = Sequencer.get_seq_channel(step_num)
		else:
			chan = channels.selectedChannel()
		if channels.isGraphEditorVisible() and Config.SELECT_PARAM_STEP:
			Action.selected_step = step_num
			self.event.handled = True
		else:
			step = step_num % cl["defaults"]["sequence_multiple"][1] 
			Sequencer.set_step(self, step, chan) 

	def set_step(self, step, chan):
		if channels.getGridBit(chan, step) == 0:						
			channels.setGridBit(chan, step, 1)
			self.event.handled = True
		else:															
			channels.setGridBit(chan, step, 0)
			self.event.handled = True

	def get_seq_channel(step_num):
			offset = int(step_num / cl["defaults"]["sequence_multiple"][1])
			chan = channels.selectedChannel() + offset
			return chan

class Encoder(Process):

	def mixer_level(d2, track):
		mixer.setTrackVolume(track, d2/127, True)

	def mixer_panning(d2, track):
		mixer.setTrackPan(track, Utility.mapvalues(d2, -1, 1, 0, 127), True)

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
		# if data['actions'][Action.shift_status] == 'set_parameter_value':
		# 	Action.set_parameter_value(self.event.data2)


		# elif data['actions'][Action.shift_status] == 'set_random_min_octave':
		# 	Action.set_random_min_octave(self.event.data2)

		# elif data['actions'][Action.shift_status] == 'set_random_max_octave':
		# 	Action.set_random_max_octave(self.event.data2)

		# elif data['actions'][Action.shift_status] == 'set_step_parameter':
		# 	print('step param')
		# 	Action.set_step_parameter(self.event.data2)

		# elif data['actions'][Action.shift_status] == 'set_random_offset':
		# 	print('step param')
		# 	Action.set_random_offset(self.event.data2)

		# elif data['actions'][Action.shift_status] == 'selected_level':
		# 	if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
		# 		Action.set_parameter_value(self.event.data2)
		# 		# channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), Action.selected_step, Action.parameter_index, self.event.data2, 1) # int(Utility.level_adjust(self.event.data2, param_value, 1)),
		# 		# channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())
		# 	elif ui.getFocused(midi.widMixer):
		# 		mixer.setTrackVolume(mixer.trackNumber(), self.event.data2/127, True)
		# 	elif ui.getFocused(midi.widChannelRack):
		# 		channels.setChannelVolume(self.channel, self.event.data2/127, True)

		# elif (data['actions'][Action.shift_status] == 'selected_pan'):
		# 	if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
		# 		Action.set_step_parameter(self.event.data2)
		# 		# Action.parameter_index = Encoder.get_param_from_range(self.event.data2)
		# 		# channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())
		# 	if ui.getFocused(midi.widMixer):
		# 		mixer.setTrackPan(mixer.trackNumber(), Utility.mapvalues(self.event.data2, -1, 1, 0, 127), True)
		# 	elif ui.getFocused(midi.widChannelRack):
		# 		channels.setChannelPan(self.channel, Utility.mapvalues(self.event.data2, -1, 1, 0, 127), True)
		# 		# if channels.isGraphEditorVisible():
		# 		# else:

		# elif data['actions'][0] == 'master_mixer_level':
		# 	mixer.setTrackVolume(0, self.event.data2/127, True)

		# elif data['actions'][0] == 'set_efx_track':
		# 	if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
		# 		Action.selected_step = Encoder.set_step(self.event.data2)
		# 	else:
		# 		channels.setTargetFxTrack(channels.selectedChannel(), self.event.data2)

		# elif data['actions'][0] == 'scroll':
		# 	if ui.getFocused(0):
		# 		mixer.setTrackNumber(int(Utility.mapvalues(self.event.data2, 0, 64, 0, 127)))
		# 		ui.scrollWindow(midi.widMixer, mixer.trackNumber())
		# 		self.event.handled = True
	
		# 	elif ui.getFocused(1):
		# 		channels.selectOneChannel(int(round(Utility.mapvalues(self.event.data2, channels.channelCount()-1, 0, 0, 127), 0)))			
		# 		self.event.handled = True

		# 	elif ui.getFocused(2):
		# 		playlist.deselectAll()
		# 		playlist.selectTrack(int(Utility.mapvalues(self.event.data2, 1, 30, 0, 127)))
		# 		self.event.handled = True	

		# 	elif ui.getFocused(4):
		# 		ui.navigateBrowser(midi.FPT_Down, 41)

		# elif data['actions'][0] == 'jog_wheel_up' and data['actions'][1] == 'jog_wheel_up':
		# 	Action.jog_wheel_up()

		# elif data['actions'][0] == 'jog_wheel_down':
		# 	Action.jog_wheel_down()

	# def acts(self):

	def jogWheel(self, data):
		if data.get(self.event.data2):
			Main.transport_act(self, data[self.event.data2]['actions'], 0, 0)
		
		# if data[self.event.data1][self.event.data2] == self.event.data2:
			# Main.transport_act(self, data["actions"], Action.shift_status, 3)


	def channel_link(cc):
		print(cc)
		tracks = [i for i in range(0, 128)]
		if cc >= 65:
			if Encoder.link_chan > 0:
				Encoder.link_chan -= 1
		elif Encoder.link_chan < 127:
			Encoder.link_chan += 1
		return tracks[Encoder.link_chan]



		


		# elif self.event.data1 == self.xt.knobs[3] and Mode.get_mode() != 7:
		# 	shift = Shifter()
		# 	if self.event.data2 == 65:
		# 		shift.back()
		# 	elif self.event.data2 == 1:
		# 		shift.forward()

		# elif Mode.get_mode() == 7 and self.event.data1 < 23:  		# < 23 ignores shift and lets knob 8 adjust random offset

		# 	if Mode.get_layer() == 0 and self.event.data1 == self.xt.knobs[3]:
		# 		shift = Shifter()
		# 		if self.event.data2 == 65:
		# 			shift.back()
		# 		elif self.event.data2 == 1:
		# 			shift.forward()			 
		# 	elif Mode.get_layer() == 1:
		# 		Encoder.edit_parameter(self)

		# 	elif Mode.get_layer() == 2:
		# 		Encoder.set_random(self) 



		# elif Mode.get_mode() == 6 and Mode.get_layer() == 1:
		# 	if self.event.data1 == self.xt.knobs[0] or self.event.data1 == self.xt.knobs[1]:
		# 		Encoder.set_random(self)

				# ui.setHintMsg(f"Route Current Track to Track {link}")


		# elif self.event.data1 == self.xt.knobs[7]:
		# 	Action.set_random_offset(Utility.level_adjust(self.event.data2, Action.get_random_offset(), 5))
		# 	if Action.get_random_offset() < 0:
		# 		Action.set_random_offset(0)
		# 	elif Action.get_random_offset() > 127:
		# 		Action.set_random_offset(127)
		# 	ui.setHintMsg(f'Random Offset: {Action.get_random_offset()}')



class Main(Process):	

	def transport_act(self, offset_event, status, data):
		print(data)
		print(f"event: {offset_event[0]}")
		# print(offset_event[0] in Notes.all_notes)
		# if offset_event[0] in Notes.all_notes:
			# Keys.decide(self, offset_event[0], data)
		# else:
			# Action.call_func(offset_event[status])
		Action.call_func(offset_event[status], data)
		# print(Action.shift_status)
		# if Action.shift_status:
		# else:
			# Action.call_func(offset_event[0])
		self.event.handled = True

