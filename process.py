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
import user_files.config as config
import data
import plugindata as plg
from notes import Notes, Scales
from modes import Modes
from state import state
from layout_manager import layout_map

class Process():
    """
    Main processing class.
    
    Subclasses, like Keys, Sequencer, are used as static namespaces to organize logic.
    They are not instantiated individually. Rhe Process instance (created as 'p') 
    is passed to their methods as 'self'.
    
    """

    def triage(self):

        """
        Handles incoming MIDI events and routes them to the appropriate category to be processed.
        
        This functions retrieves MIDI data from the incoming message and checks if it matches
        any of the controller categories. If so, it evaluates the FL Studio's state (active windows and 
        selected modes) and determines the intended category. 
        The MIDI data is then sent to the corresponding category class call the associated action. 
        If no matching category is found, the event is marked as handled and no longer processed.
        """

        midi_chan = self.event.midiChan + config.Config.CHANNEL_OFFSET
        midi_id = self.event.midiId
        data_1 = self.event.data1
        data_2 = self.event.data2

        
        active_contexts = []
        
 
        # Check if in Performance Mode
        if playlist.getPerformanceModeState() and ui.getFocused(midi.widPlaylist) and transport.getLoopMode():
            active_contexts.append("performance")
            
        # Check current Mode
       
        current_mode_name = Modes.get_mode() 
        active_contexts.append(current_mode_name)
        
        # If the button isn't found in "Sequencer" check "Buttons".
        # avoids adding it twice if current_mode_name is already "Buttons".
        if current_mode_name != "Buttons":
            active_contexts.append("Buttons")
        
        active_contexts.append("encoder")
        active_contexts.append("jogwheel")
        
        target = layout_map.get_contextual_action(midi_chan, midi_id, data_1, active_contexts)

        # Handle Unmapped
        if not target:
            self.event.handled = config.Config.PREVENT_PASSTHROUGH
            return

        # dispatch
        category = target["type"]
        is_press = (data_2 > 0)
        
        # check if the category found is any of the button types
        if category == "performance":
            if is_press:
                if len(target["actions"]) > 0:
                    state.performance_row = int(target["actions"][0])
                Main.set_track(target)
                Action.trig_clip()
                self.event.handled = True

        elif category in ["Sequencer", "sequencer"]:
             if target.get("toggle") or is_press:
                Sequencer.step_pressed(self, target)

        elif category in ["Keyboard", "keyboard"]:
            Keys.decide(self, target)

        elif category in ["Buttons", "button"]:
            # handles the "Default" actions 
            if target.get("toggle") or is_press:
                Main.set_track(target)
                Main.transport_act(self, target["actions"], state.shift_status)

        elif category == "encoder":
            Main.set_track(target)
            Encoder.set(self, target)
            
        elif category == "jogwheel":
            Encoder.jogWheel(self, target)



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



class Keys(Process):
    oct_iter = 2
    octave = [-36, -24, -12, 0, 12, 24, 36]

    def decide(self, data):

        index = Notes.note_list.index(data["actions"][0])
        if config.Config.KEYBOARD_CHROMATIC:
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


    def step_pressed(self, midi_data):
        act = midi_data["actions"][state.shift_status] 
        if act.isdigit():
            track = int(act) // data.cl["defaults"]["sequence_length"]
            step_num = Sequencer.get_step(int(act), data.cl["defaults"]["sequence_length"])
            chan = Sequencer.get_seq_channel(track, step_num)

            if channels.isGraphEditorVisible() and config.Config.SELECT_PARAM_STEP:
                state.selected_step = step_num
                self.event.handled = True
            else:
                Sequencer.set_step(self, step_num, chan) 
        else:
            track = midi_data["track"]
            Main.set_track(midi_data)
            Main.transport_act(self, midi_data["actions"], state.shift_status)

    def get_step(input, len):
        """
        This function takes in the action as a step number and the user-defined sequence length set for 
        the controller. It returns the remainder as to determine if the step applies to the selected channel
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

    def set(self, midi_data):
        if ui.getFocused(5) and plugins.isValid(channels.channelNumber()) and data.cl["defaults"]["plugin_control"]:
            Encoder.control_plugin(self)
        else:       
            EncoderAction.call_func(midi_data['actions'][state.shift_status], self.event.data2)

    def set_data(d):
        if config.Config.FOLLOW_TRACK and mixer.trackNumber() != 0:
            track_offset = data.cl["defaults"]["mixer_tracks"] % mixer.trackNumber()
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
        Action.call_func(offset_event[status])
        if offset_event[status] != 'nothing':
            self.event.handled = True

    def set_track(midi_data):
        """
        Gets the track associated with the currently selected output.
        track_original is direct from the dictionary entry. track_number is
        the entry plus the offset. The offset is calculated by finding the range
        the currently selected track is in. The range is a decided by the mixer_tracks
        setting from the default settings set by the user.
        """
        if config.Config.FOLLOW_TRACK and mixer.trackNumber() != 0:
            num_tracks = data.cl["defaults"]["mixer_tracks"]
            # this catches an issue when the selected track / mixer_tracks has 0 remainder
            mult = (mixer.trackNumber() - 1) // num_tracks if mixer.trackNumber() > 1 else 0
            track_offset = mult * num_tracks
        else:
            track_offset = 0
        state.track_number = midi_data["track"] + track_offset 
        state.track_original = midi_data["track"]

