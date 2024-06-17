# import data as d
from action import Action
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
# from config_layout import layoutData, keyboardData
import config_layout as cl
# from leds import Leds
# from config import Config
# import itertools
# import plugindata as plg
from notes import Notes, Scales

class Dispatch:

	def __init__(self):
		self.chan_ex = 0
		self.channel = channels.selectedChannel()
		self.pattern = patterns.patternNumber()
		self.random_offset = 63
		self.seq_b_offset = 16

class Process(Dispatch):

	def triage(self):
		midi_id = self.event.midiId
		data_1 = self.event.data1
		data_2 = self.event.data2
		# print(layoutDataself.event.data1)
		# if self.event.midiId in keyboardData:
		# if self.event.midiId in cl.jogData and self.event.data1 in cl.jogData[self.event.midiId]:
		# 	# print(cl.jogData[self.event.midiId][self.event.data1][self.event.data2])
		# 	Main.transport_act(self, cl.jogData[self.event.midiId][self.event.data1][self.event.data2])
	
		# elif self.event.midiId in cl.sequencerData and Action.get_mode() == 'Sequencer':
		# 	if self.event.data1 in cl.sequencerData[self.event.midiId]:
		# 		print('50')
		# 		Sequencer.step_pressed(self, cl.sequencerData[self.event.midiId][self.event.data1])
		# if data_1 in cl.keyboardData[midi_id]:
		if cl.keyboardData.get(midi_id, {}).get(data_1) and Action.get_mode() == 'Keyboard':
			Keys.decide(self, cl.keyboardData[midi_id][data_1]["actions"][0])
		elif cl.sequencerData.get(midi_id, {}).get(data_1) and Action.get_mode() == 'Sequencer':
			if data_2 > 0 or cl.sequencerData.get(midi_id, {}).get(data_1)["toggle"]:
				Sequencer.step_pressed(self, cl.sequencerData[midi_id][data_1]["actions"][0])
		# elif data_2 > 0 or cl.buttonData[midi_id][data_1]["toggle"]:
		# elif midi_id in cl.buttonData:	
		elif cl.buttonData.get(midi_id, {}).get(data_1) and data_2 > 0:	
			Main.transport_act(self, cl.buttonData[midi_id][data_1]["actions"], Action.shift_status, cl.buttonData[midi_id][data_1])
		# if midi_id in cl.buttonData and data_1 in cl.buttonData[midi_id]:
			# if data_2 > 0 or cl.buttonData[midi_id][data_1]["toggle"]:
				# Main.transport_act(self, cl.buttonData[midi_id][data_1]["actions"])
		# elif midi_id in cl.keyboardData:
			# if data_1 in cl.keyboardData[midi_id] and Action.get_mode() == 'Keyboard':
				# Keys.decide(self, cl.keyboardData[midi_id][data_1])
				# self.event.handled = True
		# elif midi_id == 128 and Action.get_mode() == 'Keyboard' and data_1 in cl.keyboardData[144]:
			# Keys.decide(self, cl.keyboardData[144][data_1])
			# self.event.handled = True
		# elif midi_id in cl.encoderData and data_1 in cl.encoderData[midi_id]:
			# Encoder.set(self, cl.encoderData[midi_id][data_1]);
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
		print(act)
		# 	# print(f"act: {act}") 
		# 	# print(f"notes.index: {Notes.all_notes.index(act)}") 
		# 	channels.midiNoteOn(channels.selectedChannel(), Notes.all_notes.index(act) + Action.get_octave() + 60, 0)
		# else:
		# 	# print(Keys.notes.index(act) + Action.get_octave() + 60)
		channels.midiNoteOn(channels.selectedChannel(), Notes.all_notes.index(act) + Action.get_octave() + 60, self.event.data2)
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
		if channels.isGraphEditorVisible():
			Action.selected_step = int(data)
			self.event.handled = True
		else:
			Sequencer.set_step(self, data) 

	def set_step(self, data):
		if channels.getGridBit(channels.selectedChannel(), int(data)) == 0:						
			channels.setGridBit(channels.selectedChannel(), int(data), 1)
			# Mode.set_leds(self)
			self.event.handled = True
		else:															
			channels.setGridBit(channels.selectedChannel(), int(data), 0)
			# Mode.set_leds(self)
			self.event.handled = True

class Encoder(Process):
	link_chan = 0

	def get_param_from_range(cc):
		param = 0
		if cc < 19:
			param = 0
		elif cc < 37:
			param = 1
		elif cc < 56: 
			param = 2
		elif cc < 74:
			param = 3
		elif cc < 92:
			param = 4
		elif cc < 110:
			param = 5
		elif cc <= 127:
			param = 6
		return param

	def set(self, data):
		if (data == 'selected_level'):
			if ui.getFocused(midi.widMixer):
				mixer.setTrackVolume(mixer.trackNumber(), self.event.data2/127, True)
			elif ui.getFocused(midi.widChannelRack):
				if channels.isGraphEditorVisible():
					channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), Action.selected_step, Action.parameter_index, self.event.data2, 1) # int(Utility.level_adjust(self.event.data2, param_value, 1)),
					channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())
				else:
					channels.setChannelVolume(channels.selectedChannel(), self.event.data2/127, True)

		elif (data == 'selected_pan'):
			if ui.getFocused(midi.widMixer):
				mixer.setTrackPan(mixer.trackNumber(), Utility.mapvalues(self.event.data2, -1, 1, 0, 127), True)
			elif ui.getFocused(midi.widChannelRack):
				if channels.isGraphEditorVisible():
					Action.parameter_index = Encoder.get_param_from_range(self.event.data2)
					channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())
				else:
					channels.setChannelPan(channels.selectedChannel(), Utility.mapvalues(self.event.data2, -1, 1, 0, 127), True)

		elif data == 'master_mixer_level':
			mixer.setTrackVolume(0, self.event.data2/127, True)

		elif data == 'set_efx_track':
			channels.setTargetFxTrack(channels.selectedChannel(), self.event.data2)

		elif data == 'scroll':
			if ui.getFocused(0):
				mixer.setTrackNumber(int(Utility.mapvalues(self.event.data2, 0, 64, 0, 127)))
				ui.scrollWindow(midi.widMixer, mixer.trackNumber())
				self.event.handled = True
	
			elif ui.getFocused(1):
				channels.selectOneChannel(int(round(Utility.mapvalues(self.event.data2, channels.channelCount()-1, 0, 0, 127), 0)))			
				self.event.handled = True

			elif ui.getFocused(2):
				playlist.deselectAll()
				playlist.selectTrack(int(Utility.mapvalues(self.event.data2, 1, 30, 0, 127)))
				self.event.handled = True	

			elif ui.getFocused(4):
				ui.navigateBrowser(midi.FPT_Down, 41)

		elif data == 'jog_wheel_up':
			Action.jog_wheel_up()

		elif data == 'jog_wheel_down':
			Action.jog_wheel_down()

	def channel_link(cc):
		print(cc)
		tracks = [i for i in range(0, 128)]
		if cc >= 65:
			if Encoder.link_chan > 0:
				Encoder.link_chan -= 1
		elif Encoder.link_chan < 127:
			Encoder.link_chan += 1
		return tracks[Encoder.link_chan]



		# if ui.getFocused(5) and plugins.isValid(channels.channelNumber()): 

		# 	plugin = plugins.getPluginName(channels.selectedChannel())	
		# 	param_count = plugins.getParamCount(channels.selectedChannel())
		# 	if plugin in plg.plugin_dict:
		# 		param = plg.plugin_dict[plugin][self.xt.knobs.index(self.event.data1)]
		# 		param_value =  Utility.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()), .025)		                                                                           																		
		# 		plugins.setParamValue(param_value, param, channels.selectedChannel())
		# 		self.event.handled = True
		
		# 	else:	
		# 		param = self.event.data1 - 15
		# 		param_value =  Utility.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()), .025)	
		# 		plugins.setParamValue(param_value, param, self.channel)
		# 		self.event.handled = True

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



	def edit_parameter(self):
			param_knob = self.xt.knobs.index(self.event.data1)
			param_value = channels.getCurrentStepParam(self.channel, Buttons.step_to_edit, param_knob)
			channels.showGraphEditor(True, param_knob, Buttons.step_to_edit, channels.selectedChannel())
																						# bool temporary, long param, long step, long index, (long globalIndex* = 1)			
			if param_knob == midi.pModX or param_knob == midi.pModY: 					#long index, long patNum, long step, long param, long value, (long globalIndex = 0)
				channels.setStepParameterByIndex(self.channel, self.pattern, Buttons.step_to_edit, param_knob, int(Utility.level_adjust(self.event.data2, param_value,  1)), 1)

			elif param_knob == midi.pFinePitch:	
				channels.setStepParameterByIndex(self.channel, self.pattern, Buttons.step_to_edit, param_knob, int(Utility.level_adjust(self.event.data2, param_value,  1)), 1)

			else:
				channels.setStepParameterByIndex(self.channel, self.pattern, Buttons.step_to_edit, param_knob, int(Utility.level_adjust(self.event.data2, param_value, 1)), 1)


class Main(Process):	

	def transport_act(self, offset_event, status, data):
		print(f"event: {offset_event[0]}")
		print(f"data: {data}")
		# print(Notes.all_notes)
		# print(offset_event[0] in Notes.all_notes)
		# if offset_event[0] in Notes.all_notes:
			# Keys.decide(self, offset_event[0], data)
		# else:
			# Action.call_func(offset_event[status])
		Action.call_func(offset_event[status])
		# print(Action.shift_status)
		# if Action.shift_status:
		# else:
			# Action.call_func(offset_event[0])
		self.event.handled = True

# 	def set_random(self):
# 		if self.event.data1 == self.xt.knobs[0]:
# 			root = Utility.level_adjust(self.event.data2, Notes.get_root_note(), 1)
# 			if root < 0:
# 				root = 0
# 			if root > 11:
# 				root = 11
# 			Notes.set_root_note(root)	
# 			ui.setHintMsg(f'{Notes.root_name(Notes.get_root_note())} {Scales.scale_name(Scales.get_scale_choice())}')

# 		elif self.event.data1 == self.xt.knobs[1]:
# 			scale = Utility.level_adjust(self.event.data2, Scales.get_scale_choice(), 1)
# 			if scale < 0:
# 				scale = 0
# 			if scale >= len(Scales.scales):
# 				scale = len(Scales.scales) - 1
# 			Scales.set_scale(scale)
# 			ui.setHintMsg(f'{Notes.root_name(Notes.get_root_note())} {Scales.scale_name(Scales.get_scale_choice())}')

# 		elif self.event.data1 == self.xt.knobs[2]:
# 			lower = Utility.level_adjust(self.event.data2, Notes.get_lower_limit(), 1)
# 			if lower < 0:
# 				lower = 0
# 			elif lower > 50:
# 				lower = 50
# 			Notes.set_lower_limit(lower)
# 			ui.setHintMsg(f'Lower Limit: {Notes.get_lower_limit()}')
# 			self.event.handled = True

# 		elif self.event.data1 == self.xt.knobs[3]:
# 			upper = Utility.level_adjust(self.event.data2, Notes.get_upper_limit(), 1)
# 			if upper > 0:
# 				upper = 0
# 			elif upper < -50:
# 				upper = -50
# 			Notes.set_upper_limit(upper)
# 			ui.setHintMsg(f'Upper Limit: {Notes.get_upper_limit()}')
# 			self.event.handled = True



# class Mode(Process):

# 	current_mode = Config.INIT_MODE
# 	seq_modes = ['Pattern B', 'Pattern A']
# 	seq = itertools.cycle(seq_modes)
# 	seq_status = 'Pattern A'
# 	modes = ['Keyboard', 'Transport', 'Sequencer']
# 	layer_count = 0

# 	def set_layer(self, val):

# 		Mode.layer_count = Mode.layer_count + val
# 		if Mode.layer_count < 0:
# 			Mode.layer_count = 2
# 		elif Mode.layer_count > 2:
# 			Mode.layer_count = 0
# 		Mode.set_leds(self)

# 	def get_layer():
# 		return Mode.layer_count

# 	def set_mode_direct(mode):
# 		Mode.current_mode = mode

# 	def get_mode():
# 		return Mode.current_mode

# 	def set_pattern_range(self):
# 		"""rotates between pattern a and pattern b"""

# 		if Mode.get_layer() <= 1:
# 			Mode.seq_status = next(Mode.seq)
# 			ui.setHintMsg(f'Seq Mode: {Mode.seq_status}')

# 	def get_seq_status():
# 		return Mode.seq_status

# 	def set_leds(self):
# 		Leds.off(self.xt.all_button_leds)
# 		Leds.light_layer(Mode.get_layer())
# 		if Mode.get_layer() == 2 and Mode.get_mode() != 8:
# 			print('light_transport')
# 			Leds.light_transport()
# 		elif Mode.get_mode() == 6:
# 			if Mode.get_layer() == 0:
# 				Leds.light_keys(self.xt.keyboard_leds)
# 			elif Mode.get_layer() == 1:
# 				Leds.light_button_range(self.xt.all_button_leds)

# 		elif Mode.get_mode() == 7 and Mode.get_layer() != 2:
# 			Leds.knobs_off()
# 			if Mode.get_seq_status() == 'Pattern A':
# 				Leds.light_quarter_knob(54, 1)
# 			elif Mode.get_seq_status() == 'Pattern B':
# 				Leds.light_quarter_knob(54, 2)
# 			Leds.light_steps(Mode.get_seq_status())
# 		elif Mode.get_mode() == 8 and Mode.get_layer() == 0:
# 			Leds.light_transport()
# 		else:
# 			Leds.off(self.xt.all_button_leds)

# class Update():

# 	def light_control(event):
# 		if event and Mode.get_mode() == 7 and Mode.get_layer() != 2:
# 			Leds.light_steps(Mode.get_seq_status(), )
# 		elif event == 256 or event == 260:
# 			if Mode.get_mode() == 8 and Mode.get_layer() == 0:
# 				Leds.light_transport()
# 			elif Mode.get_layer() == 2 and Mode.get_mode() != 8:
# 				Leds.light_transport()

