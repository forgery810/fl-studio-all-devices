import config_layout 

class Modes():

	current_mode = 0;
	# seq_modes = ['Pattern B', 'Pattern A']
	# seq = itertools.cycle(seq_modes)
	# seq_status = 'Pattern A'
	modes = [ 'Sequencer', 'Keyboard', 'Buttons']
	layer_count = 0

	def set_layer(self, val):

		Modes.layer_count = Mode.layer_count + val
		if Modes.layer_count < 0:
			Modes.layer_count = 2
		elif Modes.layer_count > 2:
			Modes.layer_count = 0
		Modes.set_leds(self)

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

	def get_seq_status():
		return Mode.seq_status

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

