
import ui
from utility import Utility
from config_layout import cl

class Notes():
	something = 2
	octaves = [-60, -48, -24, -12, 0, 12, 24, 36, 48, 60]
	upper_limit = -25
	lower_limit = 25
	note_list = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	all_notes = note_list * cl["defaults"]["keyboard_count"]
	all_notes = []
	print(all_notes)
	for i in range(0, cl["defaults"]["keyboard_count"]):
		for n in note_list:
			text = str(n) + str(i)
			all_notes.append(text)

	octaves = [-36, -24, -12, 0, 12, 24, 36]
	root = note_list.index(cl["defaults"]["root"])

	def get_root_note():
		return Notes.root

	def set_root_note(data_two):
		Notes.root = data_two

	def set_upper_limit(data_two):
		Notes.upper_limit = data_two

	def set_lower_limit(data_two):
		Notes.lower_limit = data_two
		
	def get_upper_limit():
		return Notes.upper_limit

	def get_lower_limit():
		return Notes.lower_limit

	# def display_limits():
	# 	Timing.begin_message(f"Lower Limit: {Notes.lower_limit} - Upper Limit: {Notes.upper_limit}")

	def root_name():
		return Notes.note_list[Notes.root]

class Scales(Notes):

	major_scale = [0, 2, 4, 5, 7, 9, 11, 12,] 
	natural_scale =[0, 2, 3, 5, 7, 8, 10, 12,] 
	harmonic_scale = [0, 2, 3, 5, 7, 8, 11, 12,] 
	dorian_scale = [0, 2, 3, 5, 7, 9, 10, 12, 14,] 
	mixolydian_scale = [0, 2, 4, 5, 7, 9, 10, 12,] 
	min_pent_scale = [0, 3, 5, 7, 10, 12, 15, 17,] 
	chromatic_scale = [i for i in range(0, 145)]
	scales = [major_scale, natural_scale, harmonic_scale, dorian_scale, mixolydian_scale, min_pent_scale, chromatic_scale]
	scale_names = ["Major", "Natural Minor", "Harmonic Minor", "Dorian", "Mixolydian", "Minor Pentatonic", "Chromatic"]
	scale_choice = scale_names.index(cl["defaults"]["scale"])
	print(scale_choice)

	def set_scale(data_two):
		Scales.scale_choice = data_two

	def increment_scale():
		Scales.scale_choice += 1
		if Scales.scale_choice >= len(Scales.scales):
			Scales.scale_choice = 0

	def get_scale_choice():
		return Scales.scale_choice

	def scale_message(data_two):
		return ui.setHintMsg(Scales.scale_names[int(mapvalues(self.data_two, 0, len(Scales.scale_names)-1, 0, 127))])

	def get_scale_name():
		return Scales.scale_names[Scales.scale_choice]

	def display_scale():
		return Timing.begin_message(f"Root: {Notes.root_name(Notes.get_root_note())} Scale: {Scales.scale_name(Scales.get_scale_choice())}")