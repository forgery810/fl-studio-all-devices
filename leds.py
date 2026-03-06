import transport
import device
import channels
import user_files.config as config
from layout_manager import layout_map

class Leds():
    active_leds = set() # Kept for state tracking if needed, or  query layout_map directly
    events = {
        "transport": [256, 260],
        "sequencer": [65824, 1056, 1024, 1280],
    }
    mode = ''
    sequence_leds = False

    @staticmethod
    def led_setup():
        # Reset all known sequencer LEDs on startup
        if layout_map.leds_assigned():
            Leds.reset_sequence()

    @staticmethod
    def check_shift(shift):
        midi_data = layout_map.get_transport_led("shift")
        if midi_data:
            val = 127 if shift else 0
            device.midiOutMsg(*midi_data, val)

    @staticmethod
    def leds_assigned():
        return layout_map.leds_assigned()

    @staticmethod
    def check_event_leds(event):   
        # 1. Transport Check (Robust Bitwise)
        # 256 is the specific flag for HW_Dirty_LEDs
        if event & 256:
            Leds._update_transport_leds()

        # 2. Sequencer Check
        # Check if Sequencer mode is active OR if layout has it "Always On"
        is_seq_active = Leds.mode == 'Sequencer' or layout_map.get_setting('Sequencer')
        if event in Leds.events["sequencer"] and is_seq_active:
            Leds.set_sequence()
            
    @staticmethod
    def _update_transport_leds():
        """Updates Play, Stop, Record LEDs based on current Transport state."""
        
        # Handle Play/Stop
        is_playing = transport.isPlaying()
        
        play_led = layout_map.get_transport_led("start")
        stop_led = layout_map.get_transport_led("stop")

        if is_playing:
            if play_led: device.midiOutMsg(*play_led, 127)
            if stop_led: device.midiOutMsg(*stop_led, 0)
        else:
            if play_led: device.midiOutMsg(*play_led, 0)
            if stop_led: device.midiOutMsg(*stop_led, 127)

        # Handle Record
        rec_led = layout_map.get_transport_led("record")
        if rec_led:
            val = 127 if transport.isRecording() else 0
            device.midiOutMsg(*rec_led, val)

    @staticmethod
    def set_sequence():
        """Updates the step sequencer grid LEDs."""
        # Get all defined sequencer LEDs
        seq_leds = layout_map.get_sequencer_leds()
        selected_channel = channels.selectedChannel()

        for step, midi_data in seq_leds.items():
            # Check if the bit is set in FL Studio
            is_active = channels.getGridBit(selected_channel, step)
            val = 127 if is_active else 0
            device.midiOutMsg(*midi_data, val)

    @staticmethod
    def reset_sequence():
        """Turns off all sequencer LEDs."""
        seq_leds = layout_map.get_sequencer_leds()
        for midi_data in seq_leds.values():
            device.midiOutMsg(*midi_data, 0)

    @staticmethod
    def set_current_mode(mode):
        Leds.mode = mode
        # Enable LEDs if entering Sequencer mode OR if it's "Always On" in layout
        if mode == 'Sequencer' or layout_map.get_setting('Sequencer'):
            Leds.set_sequence()
        else:
            Leds.reset_sequence()
