import transport
import device
import channels
import user_files.config as config
from layout_manager import layout_map

class Leds():
    active_leds = set() # Kept for state tracking if needed, or we can query layout_map directly
    events = {
        "transport": [256, 260],
        "sequencer": [65824, 1056, 1024, 1280],
    }
    mode = ''
    sequence_leds = False

    @staticmethod
    def led_setup():
        # Reset all known sequencer LEDs on startup
        if layout_map.leds_assigned():
            Leds.reset_sequence()

    @staticmethod
    def check_shift(shift):
        midi_data = layout_map.get_transport_led("shift")
        if midi_data:
            val = 127 if shift else 0
            device.midiOutMsg(*midi_data, val)

    @staticmethod
    def leds_assigned():
        return layout_map.leds_assigned()

    @staticmethod
    def check_event_leds(event):   
        # Check Sequencer Events
        if event in Leds.events["sequencer"] and Leds.mode == 'Sequencer':
            Leds.set_sequence()
        
        # Check Transport Events
        elif event in Leds.events["transport"]:
            Leds._update_transport_leds()

    @staticmethod
    def _update_transport_leds():
        """Updates Play, Stop, Record LEDs based on current Transport state."""
        
        # Handle Play/Stop
        is_playing = transport.isPlaying()
        
        play_led = layout_map.get_transport_led("start")
        stop_led = layout_map.get_transport_led("stop")

        if is_playing:
            if play_led: device.midiOutMsg(*play_led, 127)
            if stop_led: device.midiOutMsg(*stop_led, 0)
        else:
            if play_led: device.midiOutMsg(*play_led, 0)
            if stop_led: device.midiOutMsg(*stop_led, 127)

        # Handle Record
        rec_led = layout_map.get_transport_led("record")
        if rec_led:
            val = 127 if transport.isRecording() else 0
            device.midiOutMsg(*rec_led, val)

    @staticmethod
    def set_sequence():
        """Updates the step sequencer grid LEDs."""
        # Get all defined sequencer LEDs
        seq_leds = layout_map.get_sequencer_leds()
        selected_channel = channels.selectedChannel()

        for step, midi_data in seq_leds.items():
            # Check if the bit is set in FL Studio
            is_active = channels.getGridBit(selected_channel, step)
            val = 127 if is_active else 0
            device.midiOutMsg(*midi_data, val)

    @staticmethod
    def reset_sequence():
        """Turns off all sequencer LEDs."""
        seq_leds = layout_map.get_sequencer_leds()
        for midi_data in seq_leds.values():
            device.midiOutMsg(*midi_data, 0)

    @staticmethod
    def set_current_mode(mode):
        Leds.mode = mode
        if mode == 'Sequencer' or config.Config.SEQUENCE_LEDS_ALWAYS_ON:
            Leds.set_sequence()
        else:
            Leds.reset_sequence()

# # from data import dledData as l
# from data import d
# import transport
# import device
# import midi
# import channels
# import data
# import user_files.config as config

# class Leds():
# 	assigned = True
# 	active_leds = set()
# 	events = {
# 		"transport": [256, 260],
# 		"sequencer": [65824, 1056, 1024, 1280],
# 	}
# 	mode = ''
# 	sequence_leds = False

# 	def led_setup():
# 		if d["leds"]:
# 			Leds.assigned = True 
# 			Leds.reset_sequence()

# 	def check_shift(shift):
# 		if shift:
# 			device.midiOutMsg(*d["leds"]["transport_leds"]["shift"], 127)
# 		else:
# 			device.midiOutMsg(*d["leds"]["transport_leds"]["shift"], 0)						# turn step leds off

# 	def check_if_led_set(led):
# 		if led in Leds.active_leds:
# 			return True
# 		else:			
# 			return False
 
# 	def leds_assigned():
# 		return Leds.assigned

# 	def set_leds_assigned(b):
# 		Leds.assigned = b

# 	def check_event_leds(event):   
# 		if event in Leds.events["sequencer"] and Leds.mode == 'Sequencer':
# 			Leds.set_sequence()
# 		elif event in Leds.events["transport"]:
# 			if transport.isPlaying():
# 				if Leds.check_if_led_set("start"):
# 					device.midiOutMsg(*d["leds"]["transport_leds"]["start"], 127)
# 				if Leds.check_if_led_set("stop"):
# 					device.midiOutMsg(*d["leds"]["transport_leds"]["stop"], 0)						# turn step leds off
# 			else:
# 				if Leds.check_if_led_set("start"):
# 					device.midiOutMsg(*d["leds"]["transport_leds"]["start"], 0)						# turn step leds off
# 				if Leds.check_if_led_set("stop"):
# 					device.midiOutMsg(*d["leds"]["transport_leds"]["stop"], 127)
# 			if Leds.check_if_led_set("record"):
# 				if transport.isRecording():
# 					device.midiOutMsg(*d["leds"]["transport_leds"]["record"], 127)
# 				else:
# 					device.midiOutMsg(*d["leds"]["transport_leds"]["record"], 0)

# 	def set_sequence():
# 		for k, v in d["leds"]["seq_leds"].items():
# 			if channels.getGridBit(channels.selectedChannel(), int(k) ) == 0:
# 				device.midiOutMsg(*d["leds"]["seq_leds"][k], 0)						# turn step leds off
# 			elif channels.getGridBit(channels.selectedChannel(), int(k)) == 1:
# 				device.midiOutMsg(*d["leds"]["seq_leds"][k], 127)

# 	def reset_sequence():
# 		for k in d["leds"]["seq_leds"].keys():
# 			device.midiOutMsg(*d["leds"]["seq_leds"][k], 0)

# 	def set_current_mode(mode):
# 		Leds.mode = mode
# 		if mode == 'Sequencer' or config.Config.SEQUENCE_LEDS_ALWAYS_ON:
# 			Leds.set_sequence()
# 		else:
# 			Leds.reset_sequence()


# 	def all_off():
# 		device.midiOutMsg(*d["ledData"]["stop"], 0)
