class State:

	def __init__(self):
		self.channel_name = ''
		self.random_max_octave = 3
		self.random_min_octave = 6
		self.octave_index = 3
		self.current_mode = 0
		self.active_track = 0
		self.parameter_index = 0
		self.mixer_num = 0 
		self.mixer_send = 0 
		self.random_offset = 63
		self.rotate_set_count = 0
		self.shift_status = 0
		self.selected_step = 0
		self.track_number = -1
		self.track_original = -1
		self.performance_row = -1
		self.old_pattern_number = -1
		self.new_pattern_number = -1
		self.change_pattern = False
		self.selected_playlist_track = 1
		self.channel_index = 0

state = State()