# import config_layout 
from leds import Leds

class Modes():

	current_mode = 0;
	# seq_modes = ['Pattern B', 'Pattern A']
	# seq = itertools.cycle(seq_modes)
	# seq_status = 'Pattern A'
	modes = [  'Buttons', 'Sequencer', 'Keyboard']
	layer_count = 0
	sequence_leds = False
	transport_leds = False

	def set_transport_leds(b):
		Modes.transport_leds = b

	def get_transport_leds():
		return Modes.transport_leds

	def set_seq_leds(b):
		Modes.sequence_leds = b

	def get_sequence_leds():
		return Modes.sequence_leds

	def set_layer(self, val):

		Modes.layer_count = Mode.layer_count + val
		if Modes.layer_count < 0:
			Modes.layer_count = 2
		elif Modes.layer_count > 2:
			Modes.layer_count = 0

	def set_mode():
		Modes.current_mode += 1
		if (Modes.current_mode >= len(Modes.modes)):
			Modes.current_mode = 0
			# Change to mode_assigned()
		# if Leds.leds_assigned():
		# 	Leds.set_current_mode(Modes.modes[Modes.current_mode])

	def get_layer():
		return Modes.layer_count

	def set_mode_direct(mode):
		Modes.current_mode = mode

	def get_mode():
		return Modes.modes[Modes.current_mode]

		# return Modes.modes[Action.get_mode()]

	def set_pattern_range(self):
		"""rotates between pattern a and pattern b"""

		if Modes.get_layer() <= 1:
			Modes.seq_status = next(Mode.seq)
			ui.setHintMsg(f'Seq Mode: {Mode.seq_status}')

	# def get_seq_status():
	# 	return Mode.seq_status

	@classmethod
	def remove_mode(cls, m):
		cls.modes.remove(m)

	@classmethod
	def mode_active(cls, mode):
		if mode in cls.modes and Modes.get_mode() == mode:
			return True 
		# elif cl.defaults[mode]:
		# 	return True 
		else:
			return False

