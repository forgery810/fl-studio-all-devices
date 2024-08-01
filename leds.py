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

	events = {
		"transport": [256, 260],
		"sequencer": [65824, 1056, 1024],
	}

	def led_setup():
		if d["ledData"]:
			# print(f"d.ledData: {bool(d["ledData"])}")
			Leds.assigned = True 
				# turn step leds off

	def check_shift(shift):
		if cl.get("leds", {}).get("shift"):
			if shift:
				print('shift present')
				device.midiOutMsg(*cl["leds"]["transport_leds"]["shift"], 127)
			else:
				device.midiOutMsg(*cl["leds"]["transport_leds"]["shift"], 0)						# turn step leds off


	def leds_assigned():
		return Leds.assigned

	def set_leds_assigned(b):
		Leds.assigned = b

	def check_event_leds(event):   
		if event in Leds.events["sequencer"]:
			Leds.set_sequence()
		elif event in Leds.events["transport"]:
			if transport.isPlaying():
				device.midiOutMsg(*cl["leds"]["transport_leds"]["start"], 127)
				device.midiOutMsg(*cl["leds"]["transport_leds"]["stop"], 0)						# turn step leds off
			else:
				device.midiOutMsg(*cl["leds"]["transport_leds"]["start"], 0)						# turn step leds off
				device.midiOutMsg(*cl["leds"]["transport_leds"]["stop"], 127)
			if transport.isRecording():
				print('record')
				device.midiOutMsg(*cl["leds"]["transport_leds"]["record"], 127)
			else:
				device.midiOutMsg(*cl["leds"]["transport_leds"]["record"], 0)

	def set_sequence():
		for k, v in cl["leds"]["seq_leds"].items():
			print(cl["leds"]["seq_leds"][k])
			if channels.getGridBit(channels.selectedChannel(), k - 1 ) == 0:
				device.midiOutMsg(*cl["leds"]["seq_leds"][k], 0)						# turn step leds off
			elif channels.getGridBit(channels.selectedChannel(), k - 1) == 1:
				device.midiOutMsg(*cl["leds"]["seq_leds"][k], 127)

	def reset_sequence():
		for k in cl["leds"]["seq_leds"].keys():
			device.midiOutMsg(*cl["leds"]["seq_leds"][k], 127)

	def set_current_mode(mode):
		if mode == 'Sequencer' or Config.SEQUENCE_LEDS_ALWAYS_ON:
			Leds.set_sequence()
		else:
			print('resey')
			Leds.reset_sequence()


	def all_off():
		device.midiOutMsg(*d["ledData"]["stop"], 0)
