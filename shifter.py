import _random 
import itertools
from midi import *
import midi  
import arrangement 
import channels 
import general
import device 
import mixer 
import patterns
import playlist 
import plugins  
import transport 
import ui 
import data 
from config import Config 
from utility import Utility

class Shifter():

	def __init__(self):
		self.channel = channels.selectedChannel()
		self.pattern = []
		self.pat_num = patterns.patternNumber()
		self.pat_len = patterns.getPatternLength(self.pat_num)
		self.p_str = self.pattern_to_string() 	
		self.p_int = self.str_to_int(self.p_str)
		self.formatted = 0
		self.list_outgoing = []

	def back(self):
		self.formatted = format(self.shift_left(), self.get_format())	
		self.list_outgoing = self.str_to_list()
		if len(self.list_outgoing) > self.pat_len:
			self.list_outgoing.pop(0)
		self.write_to_pattern()

	def forward(self):
		self.formatted = format(self.shift_right(), self.get_format())	
		self.list_outgoing = self.str_to_list()
		if len(self.list_outgoing) > self.pat_len:
			self.list_outgoing.pop(0)
		self.write_to_pattern()

	def pattern_to_string(self):
		"""takes current pattern, appends to list, return string of list"""
		for bit in range(0, self.pat_len):
			self.pattern.append(str(channels.getGridBit(self.channel, bit)))
		return (''.join(self.pattern))

	def str_to_int(self, pattern):
		"""takes pattern as string of numbers and returns int"""

		return int(pattern, 2)	

	def get_format(self):
		"""gets patterns num and returns appropriate string to format in into bits"""

		length = patterns.getPatternLength(self.pat_num) + 2
		return f'#0{length}b'

	def shift_left(self):

		out = (self.p_int << 1) | (self.p_int >> (self.pat_len - 1))
		return out

	def shift_right(self):

		out = (self.p_int >> 1) | (self.p_int << (self.pat_len - 1)) & self.max_bits(self.pat_len)
		return out

	def str_to_list(self):
		"""takes string and returns list without first two characters'b0' """

		out_list = []
		for i in self.formatted[2:]:
			out_list.append(int(i))
		return out_list

	def write_to_pattern(self):
		"""writes bit shifted pattern to approriate channel"""

		inx = 0
		if patterns.patternNumber() == self.pat_num:
			for i in range(patterns.getPatternLength(self.pat_num)):    # clear pattern
				channels.setGridBit(self.channel, i, 0)
			for step in self.list_outgoing:
				channels.setGridBit(self.channel, inx, step)
				inx += 1

	def max_bits(self, num):
		"""returns the maximun integer based on num in bits"""

		max_num = (1 << num) - 1
		return max_num


