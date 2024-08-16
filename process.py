from action import Action, EncoderAction
import transport
import channels
import ui 
import device
import mixer 
import channels 
import playlist
import plugins
import patterns
from utility import Utility
import midi
from data import d
from config import Config
from config_layout import cl
import plugindata as plg
from notes import Notes, Scales
from modes import Modes

class Process():

	def triage(self):

		"""
		Handles incoming MIDI events and routes them to the appropriate category to be processed.
		
    	This functions retrieves MIDI data from the incoming message and checks if it matches
    	any of the controller categories. If so, it evaluates the FL Studio's state (active windows and 
    	selected modes) and determines the intended category. 
    	The MIDI data is then sent to the corresponding category class call the associated action. 
    	If no matching category is found, the event is marked as handled and no longer processed.
    	"""

		midi_id = self.event.midiId
		data_1 = self.event.data1
		data_2 = self.event.data2
		self.midi_chan = self.event.midiChan + Config.CHANNEL_OFFSET
		midi_pair = [midi_id, data_1, self.midi_chan]

		cat = Process.get_categories(midi_pair)
		active = Process.get_active_category(cat)

		if active in d:
			midi_data = d[active][self.midi_chan][midi_id][data_1]

		if active == "performanceData":
			if data_2 > 0:
				Action.performance_row = int(midi_data["actions"][0])
				Main.set_track(midi_data)
				Action.trig_clip()
				self.event.handled = True
		elif active == "keyboardData":
			Keys.decide(self, midi_data)
		elif active == "sequencerData":
			if midi_data["toggle"] or data_2 > 0:
				Sequencer.step_pressed(self, midi_data)
		elif active == "buttonData":
			if (midi_data["toggle"]) or data_2 > 0:
				Main.set_track(midi_data)
				Main.transport_act(self, midi_data["actions"], Action.shift_status)
		elif active == "encoderData":
			Main.set_track(midi_data)
			Encoder.set(self, midi_data)
		elif active == "jogData":
			Encoder.jogWheel(self, d["jogData"][self.midi_chan][midi_id])
		else:
			print('passthrough')
			self.event.handled = Config.PREVENT_PASSTHROUGH

	def get_categories(midi_pair):

	    """
	    Returns all categories a MIDI pair belongs to.

		Categories are the names of the various dictionaries within d. midi_pair may be a member
		of more than one dictionary.
	    """
	    categories = ["performanceData", "keyboardData", "sequencerData", "buttonData", "encoderData", "jogData"]
	    all_categories = []
	    for category in categories:
	        if midi_pair in d[category]["midi_pairs"]:
	            all_categories.append(category)
	    return all_categories

	def get_active_category(cat):

	    """
	    Determines the active category based on a list of categories and the application state.
		
	    """
	    category = []
	    if "performanceData" in cat and playlist.getPerformanceModeState() and ui.getFocused(midi.widPlaylist) and transport.getLoopMode():
	        category = "performanceData"
	    elif "keyboardData" in cat and Modes.mode_active('Keyboard'):
	        category = "keyboardData"
	    elif "sequencerData" in cat and Modes.mode_active('Sequencer'):
	        category = "sequencerData"
	    elif "buttonData" in cat:
	        category = "buttonData"
	    elif "encoderData" in cat:
	    	category = "encoderData"
	    elif "jogData" in cat:
	    	category = "jogData"
	    else:
	    	category = "none"
	    return category


class Keys(Process):
	oct_iter = 2
	octave = [-36, -24, -12, 0, 12, 24, 36]
	def decide(self, data):

		index = Notes.note_list.index(data["actions"][0])
		if Config.KEYBOARD_CHROMATIC:
			si =  Scales.scale_names.index("Chromatic")
			scale = Scales.scales[si]
			root = 0
		else:
			scale = Scales.scales[Scales.get_scale_choice()]
			root = Notes.get_root_note()
		note = scale[index] +  data["track"] * scale[12]  +  Action.get_octave() + 60 
		channels.midiNoteOn(self.channel, note, self.event.data2)
		self.event.handled = True

	def play_note(self, data):
		channels.midiNoteOn(channels.selectedChannel(), Keys.notes.index(data) + 36, self.event.data2)

class Sequencer(Process):


	def step_pressed(self, data):
		act = data["actions"][Action.shift_status] 
		if act.isdigit():
			track = int(act) // cl["defaults"]["sequence_length"]
			print(f"track: {track}")
			print(int(act))
			step_num = Sequencer.get_step(int(act), cl["defaults"]["sequence_length"])
			chan = Sequencer.get_seq_channel(track, step_num)

			if channels.isGraphEditorVisible() and Config.SELECT_PARAM_STEP:
				Action.selected_step = step_num
				print('step_selected')
				self.event.handled = True
			else:
				Sequencer.set_step(self, step_num, chan) 
		else:
			track = data["track"]
			Main.set_track(data)
			Main.transport_act(self, data["actions"], Action.shift_status)

	def get_step(input, len):
		"""
		This function takes in the action as a step number and the user-defined sequence length set for 
		the controller. It returns the remainder as to determine if the step applies to the selected channel.
		or another
		"""
		if input == 0:
			return 0
		else:
			return input % len
			
	def set_step(self, step, chan):
		if chan < channels.channelCount():
			if channels.getGridBit(chan, step) == 0:						
				channels.setGridBit(chan, step, 1)
				self.event.handled = True
			else:															
				channels.setGridBit(chan, step, 0)
				self.event.handled = True
		else:
			self.event.handled = True

	def get_seq_channel(track, step):
			chan = channels.selectedChannel() + track
			return chan

class Encoder(Process):

	def set(self, data):
		if ui.getFocused(5) and plugins.isValid(channels.channelNumber()) and cl["defaults"]["plugin_control"]:
			Encoder.control_plugin(self)
		else:		
			print(data['actions'][Action.shift_status])
			EncoderAction.call_func(data['actions'][Action.shift_status], self.event.data2)

	def set_data(d):
		if Config.FOLLOW_TRACK and mixer.trackNumber() != 0:
			track_offset = cl["defaults"]["mixer_tracks"] % mixer.trackNumber()
		else:
			track_offset = 0
		EncoderAction.track_number = d["track"] + track_offset

	def control_plugin(self):
		plugin = plugins.getPluginName(channels.selectedChannel())	
		param_count = plugins.getParamCount(channels.selectedChannel())
		if plugin in plg.plugin_dict and plg.knob_num.index(self.event.data1) < len(plg.plugin_dict[plugin]):
			param = plg.plugin_dict[plugin][plg.knob_num.index(self.event.data1)]
			param_value =  self.event.data2/127 #Utility.level_adjust(self.event.data2, plugins.getParamValue(param, channels.selectedChannel()), .025)		                                                                           																		
			plugins.setParamValue(param_value, param, channels.selectedChannel())
			self.event.handled = True
		else:	
			param = self.event.data1 - 15
			plugins.setParamValue(self.event.data2/127, param, self.channel)
			self.event.handled = True

	def jogWheel(self, data):
		if data[self.event.data1].get(self.event.data2, {}):
			# print(data[self.event.data1][self.event.data2]['actions'])
			Main.transport_act(self, data[self.event.data1][self.event.data2]['actions'], Action.get_shift_status())

	def channel_link(cc):
		tracks = [i for i in range(0, 128)]
		if cc >= 65:
			if Encoder.link_chan > 0:
				Encoder.link_chan -= 1
		elif Encoder.link_chan < 127:
			Encoder.link_chan += 1
		return tracks[Encoder.link_chan]

class Main(Process):	

	def transport_act(self, offset_event, status):
		print(f"event: {offset_event[status]}")
		print(f"status: { Action.get_shift_status()}")
		Action.call_func(offset_event[status])
		if offset_event[status] != 'nothing':
			self.event.handled = True

	def set_track(data):
		"""
		Gets the track associated with the currently selected output.
		track_original is direct from the dictionary entry. track_number is
		the entry plus the offset. The offset is calculated by finding the range
		the currently selected track is in. The range is a decided by the mixer_tracks
		setting from the default settings set by the user.
		"""
		if Config.FOLLOW_TRACK and mixer.trackNumber() != 0:
			num_tracks = cl["defaults"]["mixer_tracks"]
			# this catches an issue when the selected track / mixer_tracks has 0 remainder
			mult = (mixer.trackNumber() - 1) // num_tracks if mixer.trackNumber() > 1 else 0
			track_offset = mult * num_tracks
		else:
			track_offset = 0
		Action.track_number = data["track"] + track_offset 
		Action.track_original = data["track"]

