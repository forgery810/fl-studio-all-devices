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
import user_files.config as config
from utility import Utility
from notes import Notes, Scales 
from modes import Modes
from leds import Leds
from state import state
from layout_manager import layout_map

class Action():

    def call_func(f):
        try:
            method = getattr(Action, f)
            return method()
        except Exception as e:
            print(f"Error in Action: '{f}' failed")
            print(f"Error: {e}")
            return None
                    
    def double_pattern():
        '''Repeats steps and notes for all channels in current pattern, doubling its length '''
        pattern = patterns.patternNumber()
        original_length = patterns.getPatternLength(pattern)

        new_length = original_length * 2
        if new_length >= 513:
            print("Pattern too long for doubling")
        else:
            for channel in range(channels.channelCount()):
                for step in range(original_length):
                    new_step = step + original_length  # Calculate the new step index
                    bit = channels.getGridBit(channel, step)
                    channels.setGridBit(channel, new_step, bit)

                    if bit:  
                        note = channels.getStepParam(step, 0, channel, 0, patterns.getPatternLength(patterns.patternNumber()))  # Use 64 as padsStride
                        channels.setStepParameterByIndex(channel, pattern, new_step, 0, note) # Use 64 as padsStride

    def select_next_channel():
        """ state.channel_index is reset by OnRefresh(65824) """
        if state.channel_index == -1:
            state.channel_index = channels.selectedChannel()
        elif state.channel_index >= channels.channelCount() - 1:
            state.channel_index = -1
        state.channel_index += 1
        channels.selectChannel(state.channel_index)

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
        modes = layout_setting.get_setting("modes")
        return modes[Modes.current_mode]

    def channel_mixer():
        if ui.getFocused(midi.widMixer):
            Action.focus_channels()
        elif ui.getFocused(midi.widChannelRack):
            Action.focus_mixer()
        else:
            Action.focus_channels()

    def octave_up():
        state.octave_index += 1
        if (state.octave_index >= len(Notes.octaves)):
            state.octave_index = 0
        ui.setHintMsg(f"Octave: {Action.get_octave()}")

    def octave_down():
        state.octave_index -= 1
        if (state.octave_index < 0):
            state.octave_index = len(Notes.octaves) - 1
        ui.setHintMsg(f"Octave: {Action.get_octave()}")

    def get_octave():
        return Notes.octaves[state.octave_index]

    def set_random_max_octave(data2):
        state.random_max_octave = int(Utility.mapvalues(data2, 0, 10, 1, 127))
        ui.setHintMsg(f"Max Octave: {state.random_max_octave}")
        return 

    def set_random_min_octave(data2):
        state.random_min_octave = int(Utility.mapvalues(data2, 0, 10, 1, 127))
        ui.setHintMsg(f"Min Octave: {state.random_min_octave}")
        return 

    def get_mixer_route():
        return state.mixer_send

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
            channels.setChannelName(channels.selectedChannel(), state.channel_name)

        else:
            state.channel_name = channels.getChannelName(channels.selectedChannel())
            channels.showGraphEditor(True, 0, 0, channels.selectedChannel())

    def stop():
        return transport.stop()

    # def setPosition(position = 0):
    #   return transport.setSongPos(position)

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
            playlist.muteTrack(state.selected_playlist_track)

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
        state.rotate_set_count += 1
        windows = layout_map.get_setting('windows', [4, 0, 2, 1, 3])
        if state.rotate_set_count >= len(windows):
            state.rotate_set_count = 0
        ui.showWindow(windows[state.rotate_set_count])

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
        elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(state.selected_playlist_track):
            playlist.soloTrack(state.selected_playlist_track)  

    def link_mix():
        mixer.linkTrackToChannel(0)

    def item_menu():
        transport.globalTransport(FPT_ItemMenu, 91)

    def countdown():
        transport.globalTransport(FPT_CountDown, 115)

    def change_step_parameter():
        state.parameter_index += 1
        if state.parameter_index > 6:
            state.parameter_index = 0
        ui.setHintMsg(f"{state.parameter_index}")
        channels.showGraphEditor(True, state.parameter_index, state.selected_step, channels.selectedChannel())

    def change_color():
        colors = layout_map.get_setting("colors")
        state.current_color += 1
        if state.current_color >= len(colors):
            count = 0
        if colors:
            if ui.getFocused(widChannelRack):
                channels.setChannelColor(channels.selectedChannel(), colors[state.current_color])
            elif ui.getFocused(widMixer):
                mixer.setTrackColor(mixer.trackNumber(), colors[count])
            elif ui.getFocused(widPlaylist) and playlist.isTrackSelected(state.selected_playlist_track):
                playlist.setTrackColor(state.selected_playlist_track, colors[state.current_color])
        else:
            print('No colors set in default settings.')

    def trig_clip():
        mode = playlist.getLiveLoopMode(state.performance_row)
        if playlist.getLiveBlockStatus(state.performance_row, state.track_number, 2) == 2: 
            if mode == 1:
                playlist.triggerLiveClip(state.performance_row, state.track_number, midi.TLC_MuteOthers | midi.TLC_Fill)
            else:
                playlist.triggerLiveClip(state.performance_row, -1, midi.TLC_MuteOthers | midi.TLC_Fill)

        else:
            playlist.triggerLiveClip(state.performance_row, state.track_number, midi.TLC_MuteOthers | midi.TLC_Fill)

    def rand_trigs():
            """Function clears pattern and for each step, generates a random number. The number is checked"""
            for i in range(patterns.getPatternLength(patterns.patternNumber())): 
                channels.setGridBit(channels.selectedChannel(), i, 0)
            for z in range (patterns.getPatternLength(patterns.patternNumber())):
                y = Utility.num_gen()
                if y < ( state.random_offset * 516):
                    channels.setGridBit(channels.selectedChannel(), z, 1)
                else:
                    pass

    def rand_notes():
        """function sets random notes for selected pattern when called based on scale/root selected in switch along with Knob() class"""

        scale = Scales.get_scale_choice()
        root = Notes.get_root_note()
        # upper = Notes.get_upper_limit()
        # lower = Notes.get_lower_limit()
        upper = state.random_max_octave
        lower = state.random_min_octave
        for i in range(patterns.getPatternLength(patterns.patternNumber())):
            interval = Scales.scales[scale][int(Utility.mapvalues(Utility.num_gen(), 0, len(Scales.scales[scale]), 0, 65535))]
            octave = int(Utility.mapvalues(Utility.num_gen(), lower, upper, 0, 65535)) * 12
            note = interval + octave
            finalNote = note + root
            channels.setStepParameterByIndex(channels.selectedChannel(), patterns.patternNumber(), i, 0, finalNote)     

    def rand_pattern():
        Action.rand_trigs()
        Action.rand_notes()

    def randomize_all_channel_trigs():
        number_of_channels = channels.channelCount(patterns.patternNumber())
        for chan in range(number_of_channels):
            channels.selectOneChannel(chan)
            Action.rand_trigs()

    def randomize_selected_channel_trigs():     ## Should consolidate along with random_trigs()
        number_of_channels = channels.channelCount(patterns.patternNumber())
        for chan in range(number_of_channels):
            if channels.isChannelSelected(chan):
                for i in range(patterns.getPatternLength(patterns.patternNumber())): 
                    channels.setGridBit(chan, i, 0)
                for z in range (patterns.getPatternLength(patterns.patternNumber())):
                    y = Utility.num_gen()
                    if y < ( state.random_offset * 516):
                        channels.setGridBit(chan, z, 1)
                    else:
                        pass

    def randomize_plugin():
        channel = channels.selectedChannel()
        try:
            parameter_count = plugins.getParamCount(channel)
            for i in range(parameter_count):
                rand_val = Utility.mapvalues(Utility.num_gen(), 0, 127, 0, 65535)/127.0
                plugins.setParamValue(rand_val, i, channel)
        except Exception as e:
            print(e)

    def shift():
        if state.shift_status == 0:
            state.shift_status = 1
            ui.setHintMsg('Shift Active')
        elif state.shift_status == 1:
            state.shift_status = 0
            ui.setHintMsg('Shift Disabled')
        if Leds.check_if_led_set('shift'):
            Leds.check_shift(state.shift_status)

    def get_shift_status():
        return state.shift_status

    def set_random_offset(val):
        state.random_offset = val
        ui.setHintMsg(f'Random: {int(val/127 * 100)}%')
    # def get_random_offset():
    #   return state.random_offset

    def get_step_param():
        return state.parameter_index

    # def get_mixer_num():
    #   return state.mixer_num

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
        mixer.soloTrack(state.track_number)

    def mixer_record():
        mixer.armTrack(state.track_number)

    def mixer_mute():
        mixer.muteTrack(state.track_number)

    def select_pattern():
        """is pattern_change_wait set, onupbeatindicator will trigger
            change when change_patten = true """

        if state.track_original != patterns.patternNumber() and transport.isPlaying() and config.Config.PATTERN_CHANGE_WAIT:
            state.change_pattern = True

        else:
            device.midiOutMsg(176, 1, 50, 80)
            patterns.jumpToPattern(state.track_original)

    def mute_channel():
        chan = state.track_original - 1
        if state.track_original <= channels.channelCount():
            channels.muteChannel(chan)

class EncoderAction(Action):
    parameter_ranges = [ 0, 19, 37, 56, 74, 92, 110, 128 ]

    def set_parameter_value(d2):

        c = channels.selectedChannel()
        p = patterns.patternNumber()
        s = state.selected_step
        pi = state.parameter_index
        if state.parameter_index == midi.pModX or state.parameter_index == midi.pModY:                    
                        #long index, long patNum, long step, long param, long value, (long globalIndex = 0)
            channels.setStepParameterByIndex(c, p, s, pi, int(Utility.mapvalues(d2, 0 , 255, 0, 127)), 1)
        elif state.parameter_index == midi.pFinePitch: 
            channels.setStepParameterByIndex(c, p, s, pi, int(Utility.mapvalues(d2, 0 , 240, 0, 127)), 1)
        else:
            channels.setStepParameterByIndex(c, p, s, pi, d2, 1)
        channels.showGraphEditor(True, state.parameter_index, state.selected_step, channels.selectedChannel())

    def call_func(f, d2):
        method = getattr(EncoderAction, f)
        return method(d2) 

    def set_mixer_route(d2):
        state.mixer_send = d2
        ui.setHintMsg(f"Route Mixer to {d2}") 

    def set_random_min_octave(d2):
        Action.set_random_min_octave(d2)

    def set_random_max_octave(d2):
        Action.set_random_max_octave(d2)

    def set_step_parameter(d2):
        state.parameter_index = EncoderAction.get_param_from_range(d2)
        channels.showGraphEditor(True, state.parameter_index, state.selected_step, channels.selectedChannel())

    def set_random_offset(d2):
        Action.set_random_offset(d2)

    def selected_level(d2):
        levels_control = layout_map.get_setting('levels_control_parameter')
        if channels.isGraphEditorVisible() and levels_control_parameter:
            Action.set_parameter_value(d2)
        elif ui.getFocused(midi.widMixer):
            mixer.setTrackVolume(mixer.trackNumber(), d2/127, True)
        elif ui.getFocused(midi.widChannelRack):
            channels.setChannelVolume(channels.selectedChannel(), d2/127, True)

    def get_param_from_range(cc):
        for i, r in enumerate(Encoderstate.parameter_ranges):
            if cc < r:
                return i 

    def selected_pan(d2):
        levels_control = layout_map.get_setting('levels_control_parameter')
        if channels.isGraphEditorVisible() and levels_control_parameter:
            Action.set_step_parameter(d2)
        if ui.getFocused(midi.widMixer):
            mixer.setTrackPan(mixer.trackNumber(), Utility.mapvalues(d2, -1, 1, 0, 127), True)
        elif ui.getFocused(midi.widChannelRack):
            channels.setChannelPan(channels.selectedChannel(), Utility.mapvalues(d2, -1, 1, 0, 127), True)

    def master_mixer_level(d2):
        mixer.setTrackVolume(0, d2/127, True)

    def set_efx_track(d2):
        levels_control = layout_map.get_setting('levels_control_parameter')
        if channels.isGraphEditorVisible() and levels_control_parameter:
            state.selected_step = EncoderAction.set_step(d2)
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
            mixer.setTrackNumber(int(Utility.mapvalues(d2, 0, config.Config.MIXER_SCROLL_MAX, 0, 127)))
            ui.scrollWindow(midi.widMixer, mixer.trackNumber())

        elif ui.getFocused(1):
            channels.selectOneChannel(int(round(Utility.mapvalues(d2, 0, channels.channelCount()-1, 0, 127), 0)))           

        elif ui.getFocused(2):
            track = int(Utility.mapvalues(d2, 1, 30, 0, 127))
            playlist.deselectAll()
            playlist.selectTrack(track)
            state.selected_playlist_track = track 

        elif ui.getFocused(4):
            ui.navigateBrowser(midi.FPT_Down, 41)

    def jog_wheel_up(d2):
        Action.jog_wheel_up()

    def jog_wheel_down(d2):
        Action.jog_wheel_down()

    def pitch_bend(d2):
        # mixer.setTrackVolume(0, d2/127, True)
        channels.setChannelPitch(channels.selectedChannel(), Utility.mapvalues(d2, -1, 1, 0, 127))

    def mixer_level(d2):
        mixer.setTrackVolume(state.track_number, d2/127, True)

    def mixer_pan(d2):
        mixer.setTrackPan(state.track_number, Utility.mapvalues(d2, -1, 1, 0, 127), True)

    def nothing(d2):
        pass


