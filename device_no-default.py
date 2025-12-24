# name=All Devices
# Author: forgery810
VERSION = '1.0.0'

# from config_layout import cl  
import device
import channels
from midi import *
import midi
import mixer
import patterns
from layout_manager import layout_map
import channels
import ui
import transport
from state import state
from leds import Leds
from process import Process,  Main
from modes import Modes
from notes import Notes, Scales
import user_files.config as config
import plugindata as plg
from action import Action, EncoderAction
import plugindata
import itertools
import constants
import json
import os
import sys
from debug_test import run_test

def OnInit():
    """Function called when script starts"""
    from layout_reader import load_config

    if device.isAssigned():
        port = device.getPortNumber()
        dev_name = device.getName()
        print("")
        print(f"Connected to: {dev_name} on Input Port {port}")
        print("Ensure the Output Port in MIDI Settings matches this number")
        print("")
        print("( <.......................")
        print("")
    else:
        print("Script is not assigned to any device.")

    # Load configuration (handles JSON vs Python fallback internally)
    cl = load_config()

    if cl is None:
        print("-------------------------------------------------------------")
        print("")
        print("ERROR: No layout file could be loaded.")
        print("Please check your user_files folder and config.py.")
        print("Script execution stopped.")
        print("")
        print("-------------------------------------------------------------")
        print("------- Go to www.midicontrol.cc to build a layout ----------")
        print("------- Place user_layout.json in user_files folder ---------")
        print("-------------------------------------------------------------")
        print("""                                                         
                                                    
                         ██          ██  
                           ██      ██    
                         ██████████████  
                       ████  ██████  ████
                       ██████████████████
                         ██████████████  
                         ██          ██  
                           ████  ████    
                           ████  ████    




            ,adPPYba, 8b,dPPYba, 8b,dPPYba,  ,adPPYba,  8b,dPPYba,  
           a8P_____88 88P'   "Y8 88P'   "Y8 a8"     "8a 88P'   "Y8  
           8PP        88         88         8b       d8 88          
           "8b,   ,aa 88         88         "8a,   ,a8" 88          
            `"Ybbd8"' 88         88          `"YbbdP"'  88          
                                                               



                                                               """)
        return  # <--- STOP HERE. Do not run the rest of the function.

    try:
        layout_map.build(cl)
        print("Layout map built successfully.")
        print("")
        # print("...........( <............")
        print("           ( <............")
        print("")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to build layout map from config. Error: {e}")
        # Optionally print traceback here
        return

    # Initialize Notes after config is loaded
    modes_settings = layout_map.get_setting("modes", ["Buttons", "Keyboard", "Sequencer"])
    Notes.init_notes()
    Modes.init_modes(modes_settings)
    Leds.led_setup()
    
    print(f"Device Name: {device.getName()}")
    print(f"Script Version: {VERSION}")
    
    if device.isAssigned():     
        print(f"Assigned Layout: {cl['name']}")        
    else:
        print("Not assigned. In the MIDI settings, set the Input and Output Ports to the same number for this device.")


    if config.Config.PATTERN_CHANGE_WAIT:
        def OnUpdateBeatIndicator(e):
            if e == 1:
                if config.Config.PATTERN_CHANGE_WAIT and state.change_pattern:
                    patterns.jumpToPattern(state.track_original)
                    state.change_pattern = False
    print("")
    print("                       ( <")
    print("")
 
def OnMidiMsg(event):
    """Function called on every midi message sent by controller"""

    # try:
    print(event.midiChan, event.midiId, event.data1, event.data2) 
    p.event = event
    p.channel = channels.selectedChannel()
    p.track = mixer.trackNumber()
    p.pattern = patterns.patternNumber()
    p.d2 = event.data2
    p.triage() # This runs the whole script logic

    # except Exception as e:
    #     # THIS CATCHES EVERYTHING
    #     print("------------------------------------------------")
    #     print(f"Script Error: {e}")
    #     print("------------------------------------------------")

if config.Config.PITCH_BEND:
    def OnPitchBend(event):
        EncoderAction.pitch_bend(event.data2)
        event.handled = True

def OnRefresh(event):
    # print(f"Refresh Event: {event}")
    if Leds.leds_assigned():
        Leds.check_event_leds(event)
    if event == constants.PATTERN_REFRESH:
        state.old_pattern_number = patterns.patternNumber()
    if event == constants.CHANNEL_REFRESH:
        state.channel_index = -1 # Used by Action.select_next_channel()

p = Process()

# def AssignLayoutData(bt, kb, sq, en, jw, df, pf):

#     def process_data(data, key_name):
#         """converts dict from the the easier to edit config_layout to one that is designed for processing efficiently"""
#         try:
#             for v in data.values():
#                 d[key_name][v['channel']] = {}  
#                 d[key_name][v['channel']] = {}  
#             for v in data.values():
#                 d[key_name][v['channel']][v['midi'][0]] = {}    
#                 d[key_name][v['channel']][v['midi'][3]] = {}    
#             for v in data.values():
#                 d[key_name]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ])  
#                 if key_name == 'keyboardData':
#                     d[key_name]['midi_pairs'].append([ v['midi'][3], v['midi'][1], v['channel'] ])  
    
#                 d[key_name][v['channel']][v['midi'][3]][v['midi'][1]] = {
#                     'actions': v['actions'],
#                     'channel': v['channel'],
#                     'midi_2': v['midi'][2],
#                     'toggle': v['toggle'],
#                     # 'release': v['midi'][3],
#                     'track': v['track']
#                 }
#                 d[key_name][v['channel']][v['midi'][0]][v['midi'][1]] = {
#                     'actions': v['actions'],
#                     'channel': v['channel'],
#                     'midi_2': v['midi'][2],
#                     'toggle': v['toggle'],
#                     # 'release': v['midi'][3],
#                     'track': v['track']
#                 }
#         except (KeyError, TypeError, ValueError) as e:
#             print(f"An error occured: {e}")

    

#     def process_jog_data(jw, jogData):
#         """ jog wheel must have its own function as it requires the midi_2 data to be a key"""
#         for k, v in jw.items():
#             d["jogData"][v["channel"]] = {}
#         for k, v in jw.items():
#             d["jogData"][v["channel"]][v['midi'][0]] = {}
#             # d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]] = {} 
#         for k, v in jw.items():
#             d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]] = {} 
#             d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]][v['midi'][2]] = {}
#             # d["jogData"][v["channel"]]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ]) 
#         for k, v in jw.items():
#             d["jogData"][v["channel"]][v['midi'][0]][v['midi'][1]][v['midi'][2]] = { 
#                 'actions': v['actions'],
#                 'channel': v['channel'],
#                 'toggle': v['toggle'],
#                 'release': v['midi'][3],
#                 'midi_2': v['midi'][2]
#                 }
#             d["jogData"]['midi_pairs'].append([ v['midi'][0], v['midi'][1], v['channel'] ]) 
#             # d["jogData"]['midi_pairs'].append([v['midi'][0:2], v['channel']])

#     def process_encoders_for_plugins(data):
#         for v in data.values():
#             plg.knob_num.append(v["midi"][1])

#     def process_colors(color_list):
#         if color_list:
#             d["colors"] = itertools.cycle(color_list)

#     process_data(bt, 'buttonData')
#     process_data(kb, 'keyboardData')
#     process_data(sq, 'sequencerData')
#     process_data(en, 'encoderData')
#     process_encoders_for_plugins(en)
#     process_data(pf, 'performanceData')
#     process_jog_data(jw, 'jogData')
#     process_colors(df["colors"])

transport_leds = ['shift', 'start', 'stop', 'record']

# def AssignLeds(led):

#     for v in led.values():
#         Leds.active_leds.add(v["actions"][0])
#         if v["actions"][0] in transport_leds:
#             d["leds"]["transport_leds"][v["actions"][0]] = [v["midi"][0], v["channel"] - 1, v["midi"][1]]
#             Modes.set_transport_leds(True)
            
#         else:
#             d["leds"]["seq_leds"][v["actions"][0]] = [v["midi"][0], v["channel"] - 1, v["midi"][1]]
#             Modes.set_seq_leds(True)
