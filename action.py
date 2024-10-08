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
from data import d
from config import Config 
from utility import Utility
from notes import Notes, Scales 
from modes import Modes
from leds import Leds 

class Action():

	channel_name = ''

	random_max_octave = 3
	random_min_octave = 6
	octave_index = 3
	current_mode = 0
	active_track = 0
	parameter_index = 0
	mixer_num = 0 
	mixer_send = 0 
	random_offset = 63
	rotate_set_count = 0
	shift_status = 0
	selected_step = 0
	track_number = -1
	track_original = -1
	performance_row = -1
	old_pattern_number = -1
	new_pattern_number = -1
	change_pattern = False
	selected_playlist_track = 1


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
		Modes.set_mode()
		ui.setHintMsg(Modes.modes[Modes.current_mode])

	def get_mode():
		return cl["default"]["modes"][Modes.current_mode]

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

	def get_mixer_route():
		return Action.mixer_send

	def mixer_route():
		return mixer.setRouteTo(mixer.trackNumber(), Action.get_mixer_route(), 1)

	def start():
		# device.midiOutMsg(176, 1, 42, 127)
		return transport.start()	

	def start_reset():
		if (transport.isPlaying()):
			transport.stop()
			transport.start()
		else:
			transport.start()

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

	def jog_tempo_up():
		return transport.globalTransport(FPT_TempoJog, 1)

	def jog_tempo_down():
		return transport.globalTransport(FPT_TempoJog, -1)

	def open_editor():
		channels.showEditor();

	def mute():
		if ui.getFocused(0):
			return mixer.muteTrack(mixer.trackNumber())
		elif ui.getFocused(1):
			return channels.muteChannel(channels.selectedChannel())
		elif ui.getFocused(2):
			print('nute')
			playlist.muteTrack(Action.selected_playlist_track)

	def open_channel():
		return channels.showCSForm(channels.selectedChannel(), -1)

	def up():
		return ui.up()

	def down():
		return ui.down()

	def left():
		if ui.getFocused(5) and channels.getChannelType(channels.selectedChannel()) != CT_Sampler:
			return ui.previous()
		elif ui.getFocused(widPlaylist):
			return arrangement.jumpToMarker(0, 1)
		else:
			return ui.left()

	def right():
		if ui.getFocused(5) and channels.getChannelType(channels.selectedChannel()) != CT_Sampler:
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
		if ui.getFocused(5) and channels.getChannelType(channels.selectedChannel()) != CT_Sampler:
			return ui.previous()
		else:
			Action.pattern_down()

	def next_pre_pat():
		if ui.getFocused(5) and channels.getChannelType(channels.selectedChannel()) != CT_Sampler:
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

	def arm():
		mixer.armTrack(mixer.trackNumber())

	def quantize():
		channels.quickQuantize(channels.selectedChannel())

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

	def clone_pattern():
		patterns.clonePattern()

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
		elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(Action.selected_playlist_track):
			playlist.soloTrack(Action.selected_playlist_track)	

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
		if cl["defaults"]["colors"]:
			if ui.getFocused(widChannelRack):
				channels.setChannelColor(channels.selectedChannel(), next(d["colors"]))
			elif ui.getFocused(widMixer):
				mixer.setTrackColor(mixer.trackNumber(), next(Action.c))
			elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(Action.selected_playlist_track):
				playlist.setTrackColor(Action.selected_playlist_track, next(d["colors"]))

	def trig_clip():
		mode = playlist.getLiveLoopMode(Action.performance_row)
		if playlist.getLiveBlockStatus(Action.performance_row, Action.track_number, 2) == 2: 
			if mode == 1:
				print(f"mode: {playlist.getLiveLoopMode(Action.performance_row)}");
				playlist.triggerLiveClip(Action.performance_row, Action.track_number, midi.TLC_MuteOthers | midi.TLC_Fill)
			else:
				playlist.triggerLiveClip(Action.performance_row, -1, midi.TLC_MuteOthers | midi.TLC_Fill)

		else:
			playlist.triggerLiveClip(Action.performance_row, Action.track_number, midi.TLC_MuteOthers | midi.TLC_Fill)

	def rand_trigs():
			"""Function clears pattern and for each step, generates a random number. The number is checked"""
			for i in range(patterns.getPatternLength(patterns.patternNumber())): 
				channels.setGridBit(channels.selectedChannel(), i, 0)
			for z in range (patterns.getPatternLength(patterns.patternNumber())):
				y = Utility.num_gen()
				if y < ( Action.random_offset * 516):
					channels.setGridBit(channels.selectedChannel(), z, 1)
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
			interval = Scales.scales[scale][int(Utility.mapvalues(Utility.num_gen(), 0, len(Scales.scales[scale]), 0, 65535))]
			octave = int(Utility.mapvalues(Utility.num_gen(), lower, upper, 0, 65535)) * 12
			note = interval + octave
			finalNote = note + root
			channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, finalNote)		

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
		if Leds.check_if_led_set('shift'):
			Leds.check_shift(Action.shift_status)

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

	def zoom_in_horz():
		ui.horZoom(1)

	def zoom_out_horz():
		ui.horZoom(-1)

	def zoom_in_vert():
		ui.verZoom(1)

	def zoom_out_vert():
		ui.verZoom(-1)

	def mixer_solo():
		print(f"track_num {Action.track_number}")
		mixer.soloTrack(Action.track_number)

	def mixer_record():
		print(f"track_num {Action.track_number}")
		mixer.armTrack(Action.track_number)

	def mixer_mute():
		print(f"track_num {Action.track_number}")
		mixer.muteTrack(Action.track_number)

	def select_pattern():
		"""is pattern_change_wait set, onupbeatindicator will trigger
			change when change_patten = true """

		if Action.track_original != patterns.patternNumber() and transport.isPlaying() and Config.PATTERN_CHANGE_WAIT:
			Action.change_pattern = True

		else:
			device.midiOutMsg(176, 1, 50, 80)
			patterns.jumpToPattern(Action.track_original)

	def mute_channel():
		chan = Action.track_original - 1
		if Action.track_original <= channels.channelCount():
			channels.muteChannel(chan)

class EncoderAction(Action):
	parameter_ranges = [ 0, 19, 37, 56, 74, 92, 110, 128 ]

	def set_parameter_value(d2):

		c = channels.selectedChannel()
		p = patterns.patternNumber()
		s = Action.selected_step
		pi = Action.parameter_index
		if Action.parameter_index == midi.pModX or Action.parameter_index == midi.pModY: 					
						#long index, long patNum, long step, long param, long value, (long globalIndex = 0)
			channels.setStepParameterByIndex(c, p, s, pi, int(Utility.mapvalues(d2, 0 , 255, 0, 127)), 1)
		elif Action.parameter_index == midi.pFinePitch:	
			channels.setStepParameterByIndex(c, p, s, pi, int(Utility.mapvalues(d2, 0 , 240, 0, 127)), 1)
		else:
			channels.setStepParameterByIndex(c, p, s, pi, d2, 1)
		channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())

	def call_func(f, d2):
		method = getattr(EncoderAction, f)
		return method(d2) 

	def set_mixer_route(d2):
		Action.mixer_send = d2
		ui.setHintMsg(f"Route Mixer to {d2}") 

	def set_random_min_octave(d2):
		Action.set_random_min_octave(d2)

	def set_random_max_octave(d2):
		Action.set_random_max_octave(d2)

	def set_step_parameter(d2):
		Action.parameter_index = EncoderAction.get_param_from_range(d2)
		channels.showGraphEditor(True, Action.parameter_index, Action.selected_step, channels.selectedChannel())

	def set_random_offset(d2):
		Action.set_random_offset(d2)

	def selected_level(d2):
		if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
			Action.set_parameter_value(d2)
		elif ui.getFocused(midi.widMixer):
			mixer.setTrackVolume(mixer.trackNumber(), d2/127, True)
		elif ui.getFocused(midi.widChannelRack):
			channels.setChannelVolume(channels.selectedChannel(), d2/127, True)

	def get_param_from_range(cc):
		for i, r in enumerate(EncoderAction.parameter_ranges):
			if cc < r:
				return i 

	def selected_pan(d2):
		if channels.isGraphEditorVisible() and cl["defaults"]['levels_control_parameter']:
			Action.set_step_parameter(d2)
		if ui.getFocused(midi.widMixer):
			mixer.setTrackPan(mixer.trackNumber(), Utility.mapvalues(d2, -1, 1, 0, 127), True)
		elif ui.getFocused(midi.widChannelRack):
			channels.setChannelPan(channels.selectedChannel(), Utility.mapvalues(d2, -1, 1, 0, 127), True)

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
		if ui.getFocused(0):
			mixer.setTrackNumber(int(Utility.mapvalues(d2, 0, Config.MIXER_SCROLL_MAX, 0, 127)))
			ui.scrollWindow(midi.widMixer, mixer.trackNumber())

		elif ui.getFocused(1):
			channels.selectOneChannel(int(round(Utility.mapvalues(d2, 0, channels.channelCount()-1, 0, 127), 0)))			

		elif ui.getFocused(2):
			track = int(Utility.mapvalues(d2, 1, 30, 0, 127))
			playlist.deselectAll()
			playlist.selectTrack(track)
			Action.selected_playlist_track = track 
			print(track)

		elif ui.getFocused(4):
			ui.navigateBrowser(midi.FPT_Down, 41)

	def jog_wheel_up(d2):
		Action.jog_wheel_up()

	def jog_wheel_down(d2):
		Action.jog_wheel_down()

	def pitch_bend(d2):
		# mixer.setTrackVolume(0, d2/127, True)
		channels.setChannelPitch(channels.selectedChannel(), Utility.mapvalues(d2, -1, 1, 0, 127))
		print('pitch')

	def mixer_level(d2):
		mixer.setTrackVolume(EncoderAction.track_number, d2/127, True)

	def mixer_pan(d2):
		mixer.setTrackPan(EncoderAction.track_number, Utility.mapvalues(d2, -1, 1, 0, 127), True)

	def nothing(d2):
		pass

