# from data import dledData as l
from data import d
import transport
import device
import midi
import channels
from config_layout import cl
from config import Config

class Leds():
	assigned = True
	active_leds = set()
	events = {
		"transport": [256, 260],
		"sequencer": [65824, 1056, 1024],
	}
	mode = ''
	sequence_leds = False

	def led_setup():
		if d["leds"]:
			Leds.assigned = True 
			Leds.reset_sequence()

	def check_shift(shift):
		print(*d["leds"]["transport_leds"]["shift"])
		if shift:
			device.midiOutMsg(*d["leds"]["transport_leds"]["shift"], 127)
		else:
			device.midiOutMsg(*d["leds"]["transport_leds"]["shift"], 0)						# turn step leds off

	def check_if_led_set(led):
		if led in Leds.active_leds:
			return True
		else:			
			return False
 
	def leds_assigned():
		return Leds.assigned

	def set_leds_assigned(b):
		Leds.assigned = b

	def check_event_leds(event):   
		if event in Leds.events["sequencer"] and Leds.mode == 'Sequencer':
			Leds.set_sequence()
		elif event in Leds.events["transport"]:
			if transport.isPlaying():
				if Leds.check_if_led_set("start"):
					device.midiOutMsg(*d["leds"]["transport_leds"]["start"], 127)
				if Leds.check_if_led_set("stop"):
					device.midiOutMsg(*d["leds"]["transport_leds"]["stop"], 0)						# turn step leds off
			else:
				if Leds.check_if_led_set("start"):
					device.midiOutMsg(*d["leds"]["transport_leds"]["start"], 0)						# turn step leds off
				if Leds.check_if_led_set("stop"):
					device.midiOutMsg(*d["leds"]["transport_leds"]["stop"], 127)
			if Leds.check_if_led_set("record"):
				if transport.isRecording():
					device.midiOutMsg(*d["leds"]["transport_leds"]["record"], 127)
				else:
					device.midiOutMsg(*d["leds"]["transport_leds"]["record"], 0)

	def set_sequence():
		for k, v in d["leds"]["seq_leds"].items():
			if channels.getGridBit(channels.selectedChannel(), int(k) ) == 0:
				device.midiOutMsg(*d["leds"]["seq_leds"][k], 0)						# turn step leds off
			elif channels.getGridBit(channels.selectedChannel(), int(k)) == 1:
				device.midiOutMsg(*d["leds"]["seq_leds"][k], 127)

	def reset_sequence():
		for k in d["leds"]["seq_leds"].keys():
			device.midiOutMsg(*d["leds"]["seq_leds"][k], 0)

	def set_current_mode(mode):
		Leds.mode = mode
		if mode == 'Sequencer' or Config.SEQUENCE_LEDS_ALWAYS_ON:
			Leds.set_sequence()
		else:
			Leds.reset_sequence()


	def all_off():
		device.midiOutMsg(*d["ledData"]["stop"], 0)
