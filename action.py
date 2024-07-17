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
from config_layout import cl
import data 
from config import Config 
from utility import Utility
from notes import Notes, Scales 
from modes import Modes 

class Action():

	channel_name = ''

	random_max_octave = 3
	random_min_octave = 6
	octave_index = 3
	current_mode = 0
	# color_num = 0
	active_track = 0
	parameter_index = 0
	mixer_num = 0 
	mixer_send = 0 
	random_offset = 63
	rotate_set_count = 0
	shift_status = 0
	selected_step = 0
	track_number = -1
	performance_row = -1
	# offset_iter = 0
	# pitch_value = 0

	def call_func(f):
		method = getattr(Action, f)
		return method()

	def shift_pattern_right():
		shift = Shifter()
		return shift.forward()	

	def shift_pattern_left():
		shift = Shifter()
		return shift.back()

	def change_mode():
		Modes.current_mode += 1
		if (Modes.current_mode >= len(Modes.modes)):
			Modes.current_mode = 0
		ui.setHintMsg(Modes.modes[Modes.current_mode])

	def get_mode():
		return cl["default"]["modes"][Action.current_mode]

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
		if (Action.octave_index >= len(Notes.octaves)):
			Action.octave_index = 0
		ui.setHintMsg(f"Octave: {Action.get_octave()}")

	def octave_down():
		Action.octave_index -= 1
		if (Action.octave_index < 0):
			Action.octave_index = len(Notes.octaves) - 1
		ui.setHintMsg(f"Octave: {Action.get_octave()}")

	def get_octave():
		return Notes.octaves[Action.octave_index]

	def set_random_max_octave(data2):
		Action.random_max_octave = int(Utility.mapvalues(data2, 0, 10, 1, 127))
		ui.setHintMsg(f"Max Octave: {Action.random_max_octave}")
		return 

	def set_random_min_octave(data2):
		Action.random_min_octave = int(Utility.mapvalues(data2, 0, 10, 1, 127))
		ui.setHintMsg(f"Min Octave: {Action.random_min_octave}")
		return 

	def set_mixer_route(track):
		Action.mixer_send = track 

	def get_mixer_route():
		return Action.mixer_send

	def mixer_route():
		return mixer.setRouteTo(mixer.trackNumber(), Action.get_mixer_route(), 1)

	def start():
		return transport.start()	

	def step_parameters():
		if channels.isGraphEditorVisible():
			ui.escape()
			channels.setChannelName(channels.selectedChannel(), Action.channel_name)

		else:
			Action.channel_name = channels.getChannelName(channels.selectedChannel())
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
		return transport.globalTransport(midi.FPT_StepEdit, 114)		

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
		return ui.jog(1)

	def jog_wheel_down():
		return ui.jog(-1)

	def open_editor():
		channels.showEditor();

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
			return arrangement.jumpToMarker(0, 1)
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
			Action.focus_browser()
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

	def quantize():
		channels.quickQuantize(channels.channelNumber())

	def rotate_set_windows():
		Action.rotate_set_count += 1
		if Action.rotate_set_count >= len(cl["defaults"]['windows']):
			Action.rotate_set_count = 0
		ui.showWindow(cl["defaults"]['windows'][Action.rotate_set_count])

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
		elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(ModWheel.get_pl_mod_value()):
			playlist.setTrackColor(ModWheel.get_pl_mod_value(), next(Action.c))

	def trig_clip():
		print(f"row track: {Action.performance_row}, {Action.track_number}")
		# turn_off = [2, 4]
		if playlist.getLiveBlockStatus(Action.performance_row, Action.track_number, 2) == 2: 
			print('!=0')
			playlist.triggerLiveClip(Action.performance_row, -1, midi.TLC_MuteOthers | midi.TLC_Fill)
		else:
			print('-==')
			playlist.triggerLiveClip(Action.performance_row, Action.track_number, midi.TLC_MuteOthers | midi.TLC_Fill)
		# print(f"glbs: {playlist.getLiveBlockStatus(Action.performance_row, Action.track_number, 2)}")

	def rand_trigs():
			"""Function clears pattern and for each step, generates a random number. The number is checked"""
			
			for i in range(patterns.getPatternLength(patterns.patternNumber())): 
				channels.setGridBit(channels.channelNumber(), i, 0)
			for z in range (patterns.getPatternLength(patterns.patternNumber())):
				y = Utility.num_gen()
				if y < ( Action.random_offset * 516):
					channels.setGridBit(channels.channelNumber(), z, 1)
				else:
					pass

	def rand_notes():
		"""function sets random notes for selected pattern when called based on scale/root selected in switch along with Knob() class"""

		scale = Scales.get_scale_choice()
		root = Notes.get_root_note()
		# upper = Notes.get_upper_limit()
		# lower = Notes.get_lower_limit()
		upper = Action.random_max_octave
		lower = Action.random_min_octave
		for i in range(patterns.getPatternLength(patterns.patternNumber())):
			# note = Scales.scales[scale][int(Utility.mapvalues(Utility.num_gen(), lower, len(Scales.scales[scale]) + upper, 0, 65535))]
			interval = Scales.scales[scale][int(Utility.mapvalues(Utility.num_gen(), 0, len(Scales.scales[scale]), 0, 65535))]
			octave = int(Utility.mapvalues(Utility.num_gen(), lower, upper, 0, 65535)) * 12
			note = interval + octave
			channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, note + root, 1)		

	def rand_pattern():
		Action.rand_trigs()
		Action.rand_notes()

	def shift():
		if Action.shift_status == 0:
			Action.shift_status = 1
			ui.setHintMsg('Shift Active')
		elif Action.shift_status == 1:
			Action.shift_status = 0
			ui.setHintMsg('Shift Disabled')

	def get_shift_status():
		return Action.shift_status

	def set_random_offset(val):
		Action.random_offset = val
		ui.setHintMsg(f'Random: {int(val/127 * 100)}%')
	# def get_random_offset():
	# 	return Action.random_offset

	def get_step_param():
		return Action.parameter_index

	# def get_mixer_num():
	# 	return Action.mixer_num

	def nothing():
		pass

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

	def set_step_parameter(data2):
		Action.parameter_index = Action.get_param_from_range(data2)
		channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())

	def set_parameter_value(data2):

		c = channels.selectedChannel()
		p = patterns.patternNumber()
		s = Action.selected_step
		pi = Action.parameter_index
		if Action.parameter_index == midi.pModX or Action.parameter_index == midi.pModY: 					
						#long index, long patNum, long step, long param, long value, (long globalIndex = 0)
			channels.setStepParameterByIndex(c, p, s, pi, int(Utility.mapvalues(data2, 0 , 255, 0, 127)), 1)
		elif Action.parameter_index == midi.pFinePitch:	
			channels.setStepParameterByIndex(c, p, s, pi, int(Utility.mapvalues(data2, 0 , 240, 0, 127)), 1)
		else:
			channels.setStepParameterByIndex(c, p, s, pi, data2, 1)
		channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())

	def mixer_solo():
		mixer.soloTrack(Action.track_number)

	def mixer_record():
		mixer.armTrack(Action.track_number)

	def mixer_mute():
		mixer.muteTrack(Action.track_number)

class EncoderAction(Action):

	track_number = -1

	def call_func(f, d2):
		method = getattr(EncoderAction, f)
		return method(d2) 

	def set_parameter_value(d2):
		Action.set_parameter_value(d2)

	def set_random_min_octave(d2):
		Action.set_random_min_octave(d2)

	def set_random_max_octave(d2):
		Action.set_random_max_octave(d2)

	def set_step_parameter(d2):
		Action.set_step_parameter(d2)

	def set_random_offset(d2):
		Action.set_random_offset(d2)

	def selected_level(d2):
		if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
			Action.set_parameter_value(d2)
			# channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), Action.selected_step, Action.parameter_index, d2, 1) # int(Utility.level_adjust(d2, param_value, 1)),
			# channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())
		elif ui.getFocused(midi.widMixer):
			mixer.setTrackVolume(mixer.trackNumber(), d2/127, True)
		elif ui.getFocused(midi.widChannelRack):
			channels.setChannelVolume(channels.selectedChannel(), d2/127, True)

	def selected_pan(d2):
		if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
			Action.set_step_parameter(d2)
			# Action.parameter_index = Encoder.get_param_from_range(d2)
			# channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())
		if ui.getFocused(midi.widMixer):
			mixer.setTrackPan(mixer.trackNumber(), Utility.mapvalues(d2, -1, 1, 0, 127), True)
		elif ui.getFocused(midi.widChannelRack):
			channels.setChannelPan(channels.selectedChannel(), Utility.mapvalues(d2, -1, 1, 0, 127), True)
			# if channels.isGraphEditorVisible():
			# else:

	def master_mixer_level(d2):
		mixer.setTrackVolume(0, d2/127, True)

	def set_efx_track(d2):
		if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
			Action.selected_step = EncoderAction.set_step(d2)
		else:
			channels.setTargetFxTrack(channels.selectedChannel(), d2)

	def set_step(d2):
		pat_len = patterns.getPatternLength(patterns.patternNumber()) - 1	
		step = int(Utility.mapvalues(d2, 0, pat_len, 0, 127))
		# original_name = channels.getChannelName(channels.selectedChannel())
		# channels.setChannelName(channels.selectedChannel(), str(step + 1))
		ui.setHintMsg(f"Step: {step + 1}")				
		return step


	def scroll(d2):
		print(d2)
		if ui.getFocused(0):
			mixer.setTrackNumber(int(Utility.mapvalues(d2, 0, 64, 0, 127)))
			ui.scrollWindow(midi.widMixer, mixer.trackNumber())

		elif ui.getFocused(1):
			channels.selectOneChannel(int(round(Utility.mapvalues(d2, channels.channelCount()-1, 0, 0, 127), 0)))			

		elif ui.getFocused(2):
			playlist.deselectAll()
			playlist.selectTrack(int(Utility.mapvalues(d2, 1, 30, 0, 127)))

		elif ui.getFocused(4):
			ui.navigateBrowser(midi.FPT_Down, 41)

	def jog_wheel_up(d2):
		Action.jog_wheel_up()

	def jog_wheel_down(d2):
		Action.jog_wheel_down()

	def mixer_level(d2):
		mixer.setTrackVolume(Action.track_number, d2/127, True)

	def mixer_pan(d2):
		mixer.setTrackPan(Action.track_number, Utility.mapvalues(d2, -1, 1, 0, 127), True)

	def nothing(d2):
		pass