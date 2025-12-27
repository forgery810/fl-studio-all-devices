# name=All Devices
# Author: forgery810
VERSION = '1.0.0'

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
        return

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

    print(event.midiChan, event.midiId, event.data1, event.data2) 
    p.event = event
    p.channel = channels.selectedChannel()
    p.track = mixer.trackNumber()
    p.pattern = patterns.patternNumber()
    p.d2 = event.data2
    p.triage() 


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

