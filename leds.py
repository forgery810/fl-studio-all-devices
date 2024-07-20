from data import ledData as l
import data as d
import transport
import device
import midi

class Leds():
	assigned = False

	event_numbers = {
		"transport": 256
	}

	def led_setup():
		if d.ledData:
			Leds.assigned = True 

	def leds_assigned():
		return Leds.assigned

	def check_event_leds(event):
		if event == midi.HW_Dirty_LEDs:
			if transport.isPlaying():
				print(d.ledData["start"])
				device.midiOutMsg(*d.ledData["start"], 127)
				device.midiOutMsg(*d.ledData["stop"], 0)
			elif transport.isPlaying() == False:
				device.midiOutMsg(*d.ledData["stop"], 127)
				device.midiOutMsg(*d.ledData["start"], 0)
		elif event == 260:
			if transport.isRecording():
				device.midiOutMsg(*d.ledData["record"], 127)
			else:
				device.midiOutMsg(*d.ledData["record"], 0)		

	def all_off():
		device.midiOutMsg(*d.ledData["stop"], 0)
