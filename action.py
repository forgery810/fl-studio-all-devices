import _random 
import itertools
from midi import *
import midi  
import arrangement 
import channels 
import general
import device 
import mixer 
import patterns
import playlist 
import plugins  
import transport 
import ui 
from shifter import Shifter
import config_layout as cl
# import data 
# from config import Config 
from utility import Utility
from notes import Notes, Scales 

class Action():

	
	octave_index = 3
	current_mode = 0
	# color_num = 0
	parameter_index = 0
	mixer_num = 0
	mixer_send = 0 
	c = itertools.cycle(cl.defaults["colors"])
	random_offset = 63
	rotate_set_count = 0
	shift_status = False
	selected_step = 0
	# offset_iter = 0
	# pitch_value = 0

	def call_func(f):
		print(f)
		method = getattr(Action, f)
		return method()

	def shift_pattern_right():
		shift = Shifter()
		shift.forward()	

	def shift_pattern_left():
		shift = Shifter()
		shift.back()

	def change_mode():
		Action.current_mode += 1
		if (Action.current_mode >= len(cl.modes)):
			Action.current_mode = 0
		ui.setHintMsg(cl.modes[Action.current_mode])

	def get_mode():
		return cl.modes[Action.current_mode]

	def standard_mode():
		device.midiOutMsg(0xB0, 0x00, 0x7F, 0x00)

	def channel_mixer():
		if ui.getFocused(midi.widMixer):
			Action.focus_channels()
		elif ui.getFocused(midi.widChannelRack):
			Action.focus_mixer()
		else:
			Action.focus_channels()

	def octave_up():
		Action.octave_index += 1
		if (Action.octave_index >= len(cl.octaves)):
			Action.octave_index = 0
		print(Action.get_octave())

	def octave_down():
		Action.octave_index -= 1
		if (Action.octave_index < 0):
			Action.octave_index = len(cl.octaves) - 1

	def get_octave():
		return cl.octaves[Action.octave_index]

	def set_mixer_route(track):
		Action.mixer_send = track 

	def get_mixer_route():
		return Action.mixer_send

	def mixer_route():
		mixer.setRouteTo(mixer.trackNumber(), Action.get_mixer_route(), 1)

	def start():
		return transport.start()	

	def step_parameters():
		if channels.isGraphEditorVisible():
			ui.escape()
		else:
			channels.showGraphEditor(True, 0, 0, channels.selectedChannel())

	def stop():
		return transport.stop()

	# def setPosition(position = 0):
	# 	return transport.setSongPos(position)

	def record():
		# Utility.define_message('Record')
		return transport.record()

	def song_pat():
		return transport.setLoopMode()

	def step_rec():
		transport.globalTransport(midi.FPT_StepEdit, 114)		

	def overdub():
		return transport.globalTransport(midi.FPT_Overdub, 112)

	def metronome():
		return transport.globalTransport(midi.FPT_Metronome, 110)

	def loop_record():
		return transport.globalTransport(midi.FPT_LoopRecord, 113)

	def pattern_down():
		return transport.globalTransport(midi.FPT_PatternJog, -1)

	def pattern_up():
		return transport.globalTransport(midi.FPT_PatternJog, 1)

	def jog_wheel_up():
		print('jog_wheel_up')
		return ui.jog(1)

	def jog_wheel_down():
		return ui.jog(-1)

	def mute():
		if ui.getFocused(0):
			return mixer.muteTrack(mixer.trackNumber())
		elif ui.getFocused(1):
			return channels.muteChannel(channels.channelNumber())
		# elif ui.getFocused(2):
		# 	playlist.muteTrack(ModWheel.get_pl_mod_value())

	def open_channel():
		return channels.showCSForm(channels.channelNumber(), -1)

	def up():
		return ui.up()

	def down():
		return ui.down()

	def left():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.previous()
		elif ui.getFocused(widPlaylist):
			arrangement.jumpToMarker(0, 1)
		else:
			return ui.left()

	def right():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.next()
		elif ui.getFocused(widPlaylist):
			arrangement.jumpToMarker(1, 1)
		else:
			return ui.right()

	def enter():
		if ui.getFocused(4):
			ui.selectBrowserMenuItem()		
		elif ui.getFocused(widPlaylist):
			arrangement.addAutoTimeMarker(arrangement.currentTime(1), str(arrangement.currentTime(1)))
		else:
			return ui.enter()

	def prev_pre_pat():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.previous()
		else:
			Action.pattern_down()

	def next_pre_pat():
		if ui.getFocused(5) and channels.getChannelType(channels.channelNumber()) != CT_Sampler:
			return ui.next()
		else:
			Action.pattern_up()		

	def b_down():
		ui.navigateBrowser(FPT_Down, 0)

	def b_right():
		ui.navigateBrowser(FPT_Right, 1)

	def b_left():
		ui.navigateBrowser(FPT_Left, 0)

	def b_select():
		ui.selectBrowserMenuItem()

	def undo():
		transport.globalTransport(midi.FPT_Undo, 20)
		device.midiOutMsg(144, 1, 63, 80)

	def focus_mixer():
		ui.showWindow(widMixer)

	def focus_channels():
		ui.showWindow(1)

	def focus_playlist():
		ui.showWindow(2)

	def focus_piano():
		ui.showWindow(3)

	def focus_browser():
		ui.showWindow(4)

	def set_root_note():
		Notes.root += 1
		if Notes.root >= len(Notes.note_list):
			Notes.root = 0
		ui.setHintMsg(Notes.root_name())

	def increment_scale():
		Scales.increment_scale()
		ui.setHintMsg(Scales.get_scale_name())

	def open_plugins():
		transport.globalTransport(midi.FPT_F8, 67)

	def cut():
		ui.cut()

	def copy():		
		ui.copy()

	def copy_all():
		channels.selectAll()
		ui.copy()

	def paste():
		ui.paste()

	def insert():
		ui.insert()

	def delete():
		ui.delete()

	def next():
		ui.next()

	def previous():
		print('adjkldjaklj')
		ui.previous()

	def escape():
		ui.escape()

	def next_preset():
		if plugins.isValid(channels.selectedChannel()):
			plugins.nextPreset(channels.selectedChannel())	

	def prev_preset():
		if plugins.isValid(channels.selectedChannel()):
			plugins.prevPreset(channels.selectedChannel())

	def arm_track():
		mixer.armTrack(mixer.trackNumber())

	def next():
		ui.next()

	def previous():
		ui.previous()

	def quantize():
		channels.quickQuantize(channels.channelNumber())

	def rotate_set_windows():
		Action.rotate_set_count += 1
		if Action.rotate_set_count >= len(cl.defaults['windows']):
			Action.rotate_set_count = 0
		ui.showWindow(cl.defaults['windows'][Action.rotate_set_count])

	def rotate_all():
		ui.nextWindow()

	def tap_tempo():
		transport.globalTransport(midi.FPT_TapTempo, 100)

	def wait_for_input():
		transport.globalTransport(midi.FPT_WaitForInput, 111)

	def item_menu():
		transport.globalTransport(midi.FPT_ItemMenu, 91)

	def menu():
		transport.globalTransport(midi.FPT_Menu, 90)

	def undo_up():
		transport.globalTransport(midi.FPT_UndoUp, 21)	

	def undo_down():
		general.undoDown()

	def countdown():
		transport.globalTransport(midi.FPT_CountDown, 115)
	
	def new_pattern():
		transport.globalTransport(midi.FPT_F4, 63)

	def save():
		transport.globalTransport(midi.FPT_Save, 92)

	def menu():
		transport.globalTransport(midi.FPT_Menu, 90)

	def snap_toggle():
		transport.globalTransport(midi.FPT_Snap, 48)

	def solo():
		if ui.getFocused(widMixer):
			mixer.soloTrack(mixer.trackNumber())
		elif ui.getFocused(widChannelRack):
			channels.soloChannel(channels.selectedChannel())
		# elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(ModWheel.get_pl_mod_value()):
		# 	playlist.soloTrack(ModWheel.get_pl_mod_value())	

	def link_mix():
		mixer.linkTrackToChannel(0)

	def item_menu():
		transport.globalTransport(FPT_ItemMenu, 91)

	def countdown():
		transport.globalTransport(FPT_CountDown, 115)

	def change_step_parameter():
		Action.parameter_index += 1
		if Action.parameter_index > 6:
			Action.parameter_index = 0
		ui.setHintMsg(f"{Action.parameter_index}")
		channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())

	def change_color():
		if ui.getFocused(widChannelRack):
			channels.setChannelColor(channels.selectedChannel(), next(Action.c))
		elif ui.getFocused(widMixer):
			mixer.setTrackColor(mixer.trackNumber(), next(Action.c))
		# elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(ModWheel.get_pl_mod_value()):

		# 	playlist.setTrackColor(ModWheel.get_pl_mod_value(), next(Action.c))

	# def trig_clip():
	# 	playlist.triggerLiveClip(1, 1, midi.TLC_MuteOthers | midi.TLC_Fill)
	# 	print(playlist.getLiveStatus(1))

	def rand_pat():
			"""Function clears pattern and for each step, generates a random number. The number is checked"""
			
			for i in range(patterns.getPatternLength(patterns.patternNumber())):
				channels.setGridBit(channels.channelNumber(), i, 0)
			for z in range (patterns.getPatternLength(patterns.patternNumber())):
				y = Utility.num_gen()
				if y > ( Action.random_offset * 516):
					channels.setGridBit(channels.channelNumber(), z, 1)
				else:
					pass

	def rand_notes():
		"""function sets random notes for selected pattern when called based on scale/root selected in switch along with Knob() class"""

		scale = Scales.get_scale_choice()
		root = Notes.get_root_note()
		upper = Notes.get_upper_limit()
		lower = Notes.get_lower_limit()
		for i in range(patterns.getPatternLength(patterns.patternNumber())):
			note = Scales.scales[scale][int(Utility.mapvalues(Utility.num_gen(), lower, len(Scales.scales[scale]) + upper, 0, 65535))]
			# print(note)
			channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, note + root, 1)		

	def shift():
		if Action.shift_status == False:
			Action.shift_status = True
			ui.setHintMsg('Shift Active')
		elif Action.shift_status == True:
			Action.shift_status = False
			ui.setHintMsg('Shift Disabled')

	def get_shift_status():
		return Action.shift_status

	# def set_random_offset(val):
	# 	Action.random_offset = val

	# def get_random_offset():
	# 	return Action.random_offset

	def get_step_param():
		return Action.parameter_index

	# def get_mixer_num():
	# 	return Action.mixer_num

	def nothing():
		pass

# class Shifter():

# 	def __init__(self):
# 		self.channel = channels.selectedChannel()
# 		self.pattern = []
# 		self.pat_num = patterns.patternNumber()
# 		self.pat_len = patterns.getPatternLength(self.pat_num)
# 		self.p_str = self.pattern_to_string() 	
# 		self.p_int = self.str_to_int(self.p_str)
# 		self.formatted = 0
# 		self.list_outgoing = []

# 	def back(self):
# 		self.formatted = format(self.shift_left(), self.get_format())	
# 		self.list_outgoing = self.str_to_list()
# 		if len(self.list_outgoing) > self.pat_len:
# 			self.list_outgoing.pop(0)
# 		self.write_to_pattern()

# 	def forward(self):
# 		self.formatted = format(self.shift_right(), self.get_format())	
# 		self.list_outgoing = self.str_to_list()
# 		if len(self.list_outgoing) > self.pat_len:
# 			self.list_outgoing.pop(0)
# 		self.write_to_pattern()

# 	def pattern_to_string(self):
# 		"""takes current pattern, appends to list, return string of list"""
# 		for bit in range(0, self.pat_len):
# 			self.pattern.append(str(channels.getGridBit(self.channel, bit)))
# 		return (''.join(self.pattern))

# 	def str_to_int(self, pattern):
# 		"""takes pattern as string of numbers and returns int"""

# 		return int(pattern, 2)	

# 	def get_format(self):
# 		"""gets patterns num and returns appropriate string to format in into bits"""

# 		length = patterns.getPatternLength(self.pat_num) + 2
# 		return f'#0{length}b'

# 	def shift_left(self):

# 		out = (self.p_int << 1) | (self.p_int >> (self.pat_len - 1))
# 		return out

# 	def shift_right(self):

# 		out = (self.p_int >> 1) | (self.p_int << (self.pat_len - 1)) & self.max_bits(self.pat_len)
# 		return out

# 	def str_to_list(self):
# 		"""takes string and returns list without first two characters'b0' """

# 		out_list = []
# 		for i in self.formatted[2:]:
# 			out_list.append(int(i))
# 		return out_list

# 	def write_to_pattern(self):
# 		"""writes bit shifted pattern to approriate channel"""

# 		inx = 0
# 		if patterns.patternNumber() == self.pat_num:
# 			for i in range(patterns.getPatternLength(self.pat_num)):    # clear pattern
# 				channels.setGridBit(self.channel, i, 0)
# 			for step in self.list_outgoing:
# 				channels.setGridBit(self.channel, inx, step)
# 				inx += 1

# 	def max_bits(self, num):
# 		"""returns the maximun integer based on num in bits"""

# 		max_num = (1 << num) - 1
# 		return max_num


