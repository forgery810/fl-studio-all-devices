# layout = {'one': 'left', 'two': 'up', 'three': 'right', 'four': 'copy', 'five': 'paste', 'six': 'overdub', 'seven': 'metronome', 'eight': 'undo', 'nine': 'enter', 'ten': 'down', 'eleven': 'prev_pre_pat', 'twelve': 'next_pre_pat', 'thirteen': 'loop_record', 'fourteen': 'stop', 'fifteen': 'start', 'sixteen': 'record', 'seventeen': 'left', 'eighteen': 'up', 'nineteen': 'right', 'twenty': 'focus_browser', 'twentyone': 'focus_playlist', 'twentytwo': 'focus_piano', 'twentythree': 'song_pat', 'twentyfour': 'tap_tempo', 'twentyfive': 'enter', 'twentysix': 'down', 'twentyseven': 'prev_pre_pat', 'twentyeight': 'next_pre_pat', 'twentynine': 'loop_record', 'thirty': 'stop', 'thirtyone': 'start', 'thirtytwo': 'record', 'thirtythree': 'left', 'thirtyfour': 'up', 'thirtyfive': 'right', 'thirtysix': 'overdub', 'thirtyseven': 'change_color', 'thirtyeight': 'menu', 'thirtynine': 'item_menu', 'forty': 'quantize', 'fortyone': 'enter', 'fortytwo': 'down', 'fortythree': 'focus_browser', 'fortyfour': 'arm_track', 'fortyfive': 'rotate', 'fortysix': 'escape', 'fortyseven': 'countdown', 'fortyeight': 'save', 'knob_one': 'channel_mixer', 'knob_two': 'open_channel', 'knob_three': 'mute', 'knob_four': 'solo', 'knob_five': 'rand_pat', 'one_b': 'left', 'two_b': 'up', 'three_b': 'right', 'four_b': 'escape', 'five_b': 'open_plugins', 'six_b': 'overdub', 'seven_b': 'rand_notes', 'eight_b': 'focus_browser', 'nine_b': 'enter', 'ten_b': 'down', 'eleven_b': 'prev_pre_pat', 'twelve_b': 'next_pre_pat', 'thirteen_b': 'loop_record', 'fourteen_b': 'stop', 'fifteen_b': 'start', 'sixteen_b': 'record'}

octaves = [-36, -24, -12, 0, 12, 24, 36]

buttonData = {}
keyboardData = {}
sequencerData = {}
encoderData = {}
jogData = {}
data = {}
# rotate = [ 4, 0, 3]

# encoders = { 	'1': [1, [176, 18], ['selected_level', 'selected_level']], 
# 				'2': [1, [176, 19], ['selected_pan', 'selected_pan']],
# 			 	'3': [1, [176, 20], ['set_efx_track', 'set_efx_track']],
# 			 	'4': [1, [176, 21], ['scroll', 'scroll']],
# 			 } 

# buttons = { 	'1': [1, [176, 24], ['change_mode', 'record']], 
# 				'2': [1, [176, 25], ['shift_pattern_left', 'start']], 
# 				'3': [1, [176, 26], ['rand_notes', 'change_step_parameter']], 
# 				'4': [1, [176, 27], ['shift', 'shift']], 
# 				'5': [1, [144, 98], ['left', 'left']], 
# 				'6': [1, [144, 24], ['up', 'mute']], 
# 				'7': [1, [144, 25], ['down', 'down']], 
# 				'8': [1, [144, 99], ['right', 'right']], 
# 				'9': [1, [144, 93], ['stop', 'stop']], 
# 				'10': [1, [176, 119], ['start','start']], 
# 				'11': [1, [144, 95], ['record', 'record']],
# 				'12': [10, [144, 52], ['nothing', 'nothing']], 
# 				'13': [1, [176, 28], ['octave_up', 'octave_up']], 
# 				'16': [1, [176, 28], ['increment_scale', 'change_color']],
# 			 }

# jog_wheel = {
# 	'1': [1, [176, 60, 1], ['jog_wheel_up', 'jog_wheel_up']],
# 	'2': [1, [176, 60, 65], ['jog_wheel_down', 'jog_wheel_down']]
# }

# jog_wheel = { 
# 	'1': [1,[176, 60, 1], ['jog_wheel_up, ']], 
# 	'2': [1,[176, 60, 65], ['jog_wheel_down, ']], }

# # keyboard = { 	'13': [10, [144, 53], 'C#'], 
# # 				'14': [10, [144, 54], 'D#'], 
# # 				'15': [10, [144, 55], 'F#'], 
# # 				'16': [10, [144, 56], 'G#'], 
# # 				'17': [10, [144, 57], 'A#'], 
# # 				'18': [10, [144, 36], 'C'], 
# # 				'19': [10, [144, 37], 'D'], 
# # 				'20': [10, [144, 38], 'E'], 
# # 				'21': [10, [144, 39], 'F'], 
# # 				'22': [10, [144, 40], 'G'], 
# # 				'23': [10, [144, 41], 'A'], 
# # 				'24': [10, [144, 42], 'B'], 
# # 			}



# keyboard = { '1': [10, [144, 53], 'C#0'], '2': [10, [144, 54], 'D#0'], 
# 			'3': [10, [144, 56], 'F#0'], '4': [10, [144, 57], 'G#0'], '5': [10, [144, 58], 
# 			'A#0'], '6': [10, [144, 36], 'C0'], '7': [10, [144, 37], 'D0'], 
# 			'8': [10, [144, 38], 'E0'], '9': [10, [144, 39], 'F0'], '10': [10, [144, 40], 'G0'], 
# 			'11': [10, [144, 41], 'A0'], '12': [10, [144, 42], 'B0'], '13': [10, [144, 60], 'C#1'], 
# 			'14': [10, [144, 61], 'D#1'], '15': [10, [144, 62], 'F#1'], '16': [10, [144, 63], 'G#1'], 
# 			'17': [10, [144, 64], 'A#1'], '18': [10, [144, 43], 'C1'], '19': [10, [144, 44], 'D1'], 
# 			'20': [10, [144, 45], 'E1'], '21': [10, [144, 46], 'F1'], '22': [10, [144, 47], 'G1'], 
# 			'23': [10, [144, 48], 'A1'], '24': [10, [144, 49], 'B1'], '25': [10, [144, 66], 'C#2'], 
# 			'26': [10, [144, 67], 'D#2'], '30': [10, [144, 50], 'C2'], '31': [10, [144, 51], 'D2'], }

# sequencer = { 	'1': [10, [144, 36], '0'], '2': [10, [144, 37], '1'], '3': [10, [144, 38], '2'], '4': [10, [144, 39], '3'], '5': [10, [144, 40], '4'], '6': [10, [144, 41], '5'], '7': [10, [144, 42], '6'], '8': [10, [144, 43], '7'], '9': [10, [144, 44], '8'], '10': [10, [144, 45], '9'], '11': [10, [144, 46], '10'], '12': [10, [144, 47], '11'], '13': [10, [144, 48], '12'], '14': [10, [144, 49], '13'], '15': [10, [144, 50], '14'], 
# 				'16': [10, [144, 51], '15'], '17': [10, [144, 52], '16'], '18': [10, [144, 53], '17'], '19': [10, [144, 54], '18'], '20': [10, [144, 55], '19'], '21': [10, [144, 56], '20'], '22': [10, [144, 57], '21'], '23': [10, [144, 58], '22'], '24': [10, [144, 59], '23'], '25': [10, [144, 60], '24'], '26': [10, [144, 61], '25'], '27': [10, [144, 62], '26'], '28': [10, [144, 63], '27'], '29': [10, [144, 64], '28'], '30': [10, [144, 65], '29'], '31': [10, [144, 66], '30'], '32': [10, [144, 67], '31']}

# sequencer = { '1': [10, [144, 36], '0'], '2': [10, [144, 37], '1'], '3': [10, [144, 38], '2'], '4': [10, [144, 39], '3'], '5': [10, [144, 40], '4'], '6': [10, [144, 41], '5'], '7': [10, [144, 42], '6'], '8': [10, [144, 43], '7'], '9': [10, [144, 44], '8'], '10': [10, [144, 45], '9'], '11': [10, [144, 46], '10'], '12': [10, [144, 47], '11'], '13': [10, [144, 48], '12'], '14': [10, [144, 49], '13'], '15': [10, [144, 50], '14'], '16': [10, [144, 51], '15'], '17': [10, [144, 52], '16'], '18': [10, [144, 53], '17'], '19': [10, [144, 54], '18'], '20': [10, [144, 55], '19'], '21': [10, [144, 56], '20'], '22': [10, [144, 57], '21'], '23': [10, [144, 58], '22'], '24': [10, [144, 59], '23'], '25': [10, [144, 60], '24'], '26': [10, [144, 61], '25'], '27': [10, [144, 62], '26'], '28': [10, [144, 63], '27'], '29': [10, [144, 64], '28'], '30': [10, [144, 65], '29'], '31': [10, [144, 66], '30'], '32': [10, [144, 67], '31'], }

modes = ["Keyboard", "Sequencer", ]

# defaults = { 	"colors": [ -13177619,-15859589,-4503765], 
# 				"root": "G", 
# 				"scale": "Natural Minor", 
# 				"windows": [4, 0, 2, ] 
# 			}
sequencer = { '13': {'channel': 10, 'midi': [144, 36, 8], 'actions': ['0', '0'], 'toggle': 0 }, '14': {'channel': 10, 'midi': [144, 37, 8], 'actions': ['1', '1'], 'toggle': 0 }, '15': {'channel': 10, 'midi': [144, 38, 41], 'actions': ['2', '2'], 'toggle': 0 }, '16': {'channel': 10, 'midi': [144, 39, 56], 'actions': ['3', '3'], 'toggle': 0 }, '17': {'channel': 10, 'midi': [144, 40, 71], 'actions': ['4', '4'], 'toggle': 0 }, '18': {'channel': 10, 'midi': [144, 41, 39], 'actions': ['5', '5'], 'toggle': 0 }, '19': {'channel': 10, 'midi': [144, 42, 45], 'actions': ['6', '6'], 'toggle': 0 }, '20': {'channel': 10, 'midi': [144, 43, 31], 'actions': ['7', '7'], 'toggle': 0 }, '21': {'channel': 10, 'midi': [144, 44, 50], 'actions': ['8', '8'], 'toggle': 0 }, '22': {'channel': 10, 'midi': [144, 45, 62], 'actions': ['9', '9'], 'toggle': 0 }, '23': {'channel': 10, 'midi': [144, 46, 60], 'actions': ['10', '10'], 'toggle': 0 }, '24': {'channel': 10, 'midi': [144, 47, 28], 'actions': ['11', '11'], 'toggle': 0 }, '25': {'channel': 10, 'midi': [144, 48, 33], 'actions': ['12', '12'], 'toggle': 0 }, '26': {'channel': 10, 'midi': [144, 49, 22], 'actions': ['13', '13'], 'toggle': 0 }, '27': {'channel': 10, 'midi': [144, 50, 48], 'actions': ['14', '14'], 'toggle': 0 }, '28': {'channel': 10, 'midi': [144, 51, 18], 'actions': ['15', '15'], 'toggle': 0 }, }

# default_root_note = 'C'
# default_scale = 'Harmonic Minor'
# keyboard = { 	'1': {'channel': 10, 'midi': [144, 52, 37], 'actions': ['C#0', 'C#0'], 'toggle': 0 }, 
				# '2': {'channel': 10, 'midi': [144, 53, 6], 'actions': ['D#0', ''], 'toggle': 0 }, '3': {'channel': 10, 'midi': [144, 55, 12], 'actions': ['F#0', ''], 'toggle': 0 }, '4': {'channel': 10, 'midi': [144, 56, 5], 'actions': ['G#0', ''], 'toggle': 0 }, '5': {'channel': 10, 'midi': [144, 57, 40], 'actions': ['A#0', ''], 'toggle': 0 }, '6': {'channel': 10, 'midi': [144, 36, 7], 'actions': ['C0', ''], 'toggle': 0 }, '7': {'channel': 10, 'midi': [144, 37, 9], 'actions': ['D0', ''], 'toggle': 0 }, '8': {'channel': 10, 'midi': [128, 52, 0], 'actions': ['E0', ''], 'toggle': 0 }, '9': {'channel': 10, 'midi': [128, 38, 0], 'actions': ['F0', ''], 'toggle': 0 }, '10': {'channel': 10, 'midi': [144, 40, 8], 'actions': ['G0', ''], 'toggle': 0 }, '11': {'channel': 10, 'midi': [144, 41, 32], 'actions': ['A0', ''], 'toggle': 0 }, 
				# '12': {'channel': 10, 'midi': [144, 42, 11], 'actions': ['B0', ''], 'toggle': 0 }, }

buttons = { '2': {'channel': 1, 'midi': [176, 24, 0, 176], 'actions': ['change_mode', 'solo'], 'toggle': 0 }, 
			'3': {'channel': 1, 'midi': [176, 25, 0, 176], 'actions': ['start', 'solo'], 'toggle': 0 },  
			}

# keyboard = {
# 				'4': {'channel': 10, 'midi': [144, 88, 0, 128], 'actions': ['C#0', ''], 'toggle': 0 }, 
# 			'5': {'channel': 10, 'midi': [144, 89, 0, 128], 'actions': ['D#0', ''], 'toggle': 0 }, 
# 			'6': {'channel': 10, 'midi': [144, 91, 0, 128], 'actions': ['F#0', ''], 'toggle': 0 }, 
# 			'7': {'channel': 10, 'midi': [144, 92, 0, 128], 'actions': ['G#0', ''], 'toggle': 0 }, 
# 			'8': {'channel': 10, 'midi': [144, 93, 0, 128], 'actions': ['A#0', ''], 'toggle': 0 }, 
# 			'9': {'channel': 10, 'midi': [144, 72, 0, 128], 'actions': ['C0', ''], 'toggle': 0 }, 
# 			'10': {'channel': 10, 'midi': [144, 73, 0, 128], 'actions': ['D0', ''], 'toggle': 0 }, 
# 			'11': {'channel': 10, 'midi': [144, 74, 0, 128], 'actions': ['E0', ''], 'toggle': 0 }, 
# 			'12': {'channel': 10, 'midi': [144, 75, 0, 128], 'actions': ['F0', ''], 'toggle': 0 }, 
# 			'13': {'channel': 10, 'midi': [144, 76, 0, 128], 'actions': ['G0', ''], 'toggle': 0 }, 
# 			'14': {'channel': 10, 'midi': [144, 77, 0, 128], 'actions': ['A0', ''], 'toggle': 0 }, 
# 			'15': {'channel': 10, 'midi': [144, 78, 0, 128], 'actions': ['B0', ''], 'toggle': 0 }, 
# }

keyboard = { '1': {'channel': 10, 'midi': [144, 53, 0, 128], 'actions': ['C#0', ''], 'toggle': 0 }, '2': {'channel': 10, 'midi': [144, 53, 0, 128], 'actions': ['D#0', ''], 'toggle': 0 }, '3': {'channel': 10, 'midi': [144, 55, 0, 128], 'actions': ['F#0', ''], 'toggle': 0 }, '4': {'channel': 10, 'midi': [144, 56, 0, 128], 'actions': ['G#0', ''], 'toggle': 0 }, '5': {'channel': 10, 'midi': [144, 57, 0, 128], 'actions': ['A#0', ''], 'toggle': 0 }, '6': {'channel': 10, 'midi': [144, 36, 0, 128], 'actions': ['C0', ''], 'toggle': 0 }, '7': {'channel': 10, 'midi': [144, 37, 0, 128], 'actions': ['D0', ''], 'toggle': 0 }, '8': {'channel': 10, 'midi': [144, 38, 0, 128], 'actions': ['E0', ''], 'toggle': 0 }, '9': {'channel': 10, 'midi': [144, 39, 0, 128], 'actions': ['F0', ''], 'toggle': 0 }, '10': {'channel': 10, 'midi': [144, 40, 0, 128], 'actions': ['G0', ''], 'toggle': 0 }, '11': {'channel': 10, 'midi': [144, 41, 0, 128], 'actions': ['A0', ''], 'toggle': 0 }, '12': {'channel': 10, 'midi': [144, 42, 0, 128], 'actions': ['B0', ''], 'toggle': 0 }, }

keyboard_count = 3

jog_wheel = { }

# buttons = { '13': 
# 				{'channel': 1, 
# 				'midi': [176, 24, 0], 
# 				'actions': ['start', 'solo'], 
# 				'toggle': 0, },
# 			'14': {'channel': 5, 'midi': [176, 25, 0], 'actions': ['pattern_down', 'solo'], 'toggle': 1, },}
defaults = { "colors": [], "root": "C", "scale": "Major", "windows": [4, 0, 2, 1, 3, ] }
encoders = { '1': [1, [176, 20], ['selected_level', 'selected_level']], '2': [1, [176, 21], ['master_mixer_level', 'selected_level']], '3': [1, [176, 21], ['set_efx_track', 'selected_level']], '10': [1, [176, 23], ['selected_pan', 'selected_level']], }


sequencer = { '1': {'channel': 10, 'midi': [144, 36, 0, 128], 'actions': ['0', '0'], 'toggle': 0 }, '2': {'channel': 10, 'midi': [144, 37, 0, 128], 'actions': ['1', '1'], 'toggle': 0 }, '3': {'channel': 10, 'midi': [144, 38, 0, 128], 'actions': ['2', '2'], 'toggle': 0 }, '4': {'channel': 10, 'midi': [144, 39, 0, 128], 'actions': ['3', '3'], 'toggle': 0 }, '5': {'channel': 10, 'midi': [144, 40, 0, 128], 'actions': ['4', '4'], 'toggle': 0 }, '6': {'channel': 10, 'midi': [144, 41, 0, 128], 'actions': ['5', '5'], 'toggle': 0 }, '7': {'channel': 10, 'midi': [144, 42, 0, 128], 'actions': ['6', '6'], 'toggle': 0 }, '8': {'channel': 10, 'midi': [144, 43, 0, 128], 'actions': ['7', '7'], 'toggle': 0 }, '9': {'channel': 10, 'midi': [144, 44, 0, 128], 'actions': ['8', '8'], 'toggle': 0 }, '10': {'channel': 10, 'midi': [144, 45, 0, 128], 'actions': ['9', '9'], 'toggle': 0 }, '11': {'channel': 10, 'midi': [144, 46, 0, 128], 'actions': ['10', '10'], 'toggle': 0 }, '12': {'channel': 10, 'midi': [144, 47, 0, 128], 'actions': ['11', '11'], 'toggle': 0 }, '13': {'channel': 10, 'midi': [144, 48, 0, 128], 'actions': ['12', '12'], 'toggle': 0 }, '14': {'channel': 10, 'midi': [144, 50, 0, 128], 'actions': ['13', '13'], 'toggle': 0 }, '15': {'channel': 10, 'midi': [144, 50, 0, 128], 'actions': ['14', '14'], 'toggle': 0 }, '16': {'channel': 10, 'midi': [144, 51, 0, 128], 'actions': ['15', '15'], 'toggle': 0 }, }

# buttons = { '1': [1, false, [176, 118], ['stop', 'solo']], '2': [1, false, [176, 119], ['start', 'solo']], '3': [1, false, [176, 115], ['loop_record', 'solo']], '4': [1, true, [176, 64], ['solo', 'solo']], 
			# '5': [1, true, [176, 81], ['overdub', 'solo']], '6': [1, true, [176, 118], ['focus_browser', 'solo']], }
# '5': [1, true, [128, 54],
# keyboard = { }
# sequencer = { }


	# cl.buttonData['channels'][v['channel']] = {v['midi'][0]}

# 
	# allData = { '2': {'channel': 1, 'midi': [176, 24, 0, 176], 'actions': ['record', 'solo'], 'toggle': 0 }, 
			# '3': {'channel': 1, 'midi': [176, 25, 0, 176], 'actions': ['start', 'solo'], 'toggle': 0 },  
			# '4': {'channel': 10, 'midi': [144, 88, 0, 128], 'actions': ['C#0', ''], 'toggle': 0 }, 
			# '5': {'channel': 10, 'midi': [144, 89, 0, 128], 'actions': ['D#0', ''], 'toggle': 0 }, 
			# '6': {'channel': 10, 'midi': [144, 91, 0, 128], 'actions': ['F#0', ''], 'toggle': 0 }, 
			# '7': {'channel': 10, 'midi': [144, 92, 0, 128], 'actions': ['G#0', ''], 'toggle': 0 }, 
			# '8': {'channel': 10, 'midi': [144, 93, 0, 128], 'actions': ['A#0', ''], 'toggle': 0 }, 
			# '9': {'channel': 10, 'midi': [144, 72, 0, 128], 'actions': ['C0', ''], 'toggle': 0 }, 
			# '10': {'channel': 10, 'midi': [144, 73, 0, 128], 'actions': ['D0', ''], 'toggle': 0 }, 
			# '11': {'channel': 10, 'midi': [144, 74, 0, 128], 'actions': ['E0', ''], 'toggle': 0 }, 
			# '12': {'channel': 10, 'midi': [144, 75, 0, 128], 'actions': ['F0', ''], 'toggle': 0 }, 
			# '13': {'channel': 10, 'midi': [144, 76, 0, 128], 'actions': ['G0', ''], 'toggle': 0 }, 
			# '14': {'channel': 10, 'midi': [144, 77, 0, 128], 'actions': ['A0', ''], 'toggle': 0 }, 
			# '15': {'channel': 10, 'midi': [144, 78, 0, 128], 'actions': ['B0', ''], 'toggle': 0 }, 
			# }