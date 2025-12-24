class LayoutManager:
    def __init__(self):
        self._map = {} 
        self._defaults = {}
        self._led_map = {
            "transport": {},
            "sequencer": {}
        }
        self.transport_led_names = { "shift", "start", "stop", "record"}
        self._encoder_ccs = []

    def build(self, cl):
        self._map.clear()
        self._led_map["transport"].clear()
        self._led_map["sequencer"].clear()
        self._encoder_ccs.clear()
        
        self._defaults = cl.get("defaults", {})
        # We map the JSON section names to "Context Keys"
        # The user_layout.json sections:
        
        encoder_data = cl.get("encoder", {})
        self._process_section(encoder_data, "encoder")
        self._map_encoder_indices(encoder_data) # Populate the list
        self._process_section(cl.get("performance", {}), "performance")
        self._process_section(cl.get("encoder", {}), "encoder")
        self._process_section(cl.get("jogwheel", {}), "jogwheel")
        
        # Mode-specific sections
        # In your JSON, "defaults"["modes"] = ["Buttons", "Keyboard", "Sequencer"]
        # These correspond to "button", "keyboard", "sequencer" sections.
        self._process_section(cl.get("button", {}), "Buttons")
        self._process_section(cl.get("keyboard", {}), "Keyboard")
        self._process_section(cl.get("sequencer", {}), "Sequencer")
        self._process_leds(cl.get("led", {}))

    def _map_encoder_indices(self, encoder_data):
        """
        Stores the CC numbers of encoders in the order they appear in the JSON.
        This preserves the mapping of Knob 1 -> Param 1, Knob 2 -> Param 2, etc.
        """
        for item in encoder_data.values():
            # item["midi"][1] is the data1 / CC number
            self._encoder_ccs.append(item["midi"][1])

    def get_encoder_index(self, cc_value):
        """
        Returns the index of the CC value in the encoder list.
        Returns -1 if not found.
        """
        try:
            return self._encoder_ccs.index(cc_value)
        except ValueError:
            return -1
            
    def _process_section(self, section_data, context_key):
        for item in section_data.values():
            # Standardize Key extraction
            status = item['midi'][0]
            data1 = item['midi'][1]
            channel = item['channel'] 
            
            key = (channel, status, data1)
            
            # Ensure the slot exists
            if key not in self._map:
                self._map[key] = {}
            
            # Store the action under its specific context (Mode name)
            self._map[key][context_key] = {
                "type": context_key, # Useful to know later
                "actions": item.get('actions', []),
                "track": item.get('track', 0),
                "toggle": item.get('toggle', False),
                "midi_2": item.get('midi', [0,0,0])[2] # Store data2 filter if needed
            }

    def _process_leds(self, led_data):
        """
        Parses the 'led' section of the JSON.
        Separates entries into 'transport' or 'sequencer' based on action name.
        """
        for item in led_data.values():
            action_name = item["actions"][0]
            # LED data usually needs channel 0-15 for midiOutMsg, 
            # but config usually provides 1-16. Adjusting by -1 to match legacy logic.
            # Using tuple (status, channel, data1)
            midi_packet = (item["midi"][0], item["channel"] - 1, item["midi"][1])
            
            if action_name in self.transport_led_names:
                self._led_map["transport"][action_name] = midi_packet
            else:
                # Assuming sequencer steps are stored as strings "0", "1", etc.
                # converting to int for easier lookup by step index
                try:
                    step_index = int(action_name)
                    self._led_map["sequencer"][step_index] = midi_packet
                except ValueError:
                    print(f"Warning: Unknown LED action '{action_name}' ignored.")

    def get_contextual_action(self, channel, status, data1, active_contexts):
        """
        Looks up the key, then checks the 'active_contexts' list in order.
        Returns the first match found.
        """
        potential_actions = self._map.get((channel, status, data1))
        
        if not potential_actions:
            return None
            
        # Iterate through our priorities (e.g. ['performance', 'Sequencer', 'encoder'])
        for ctx in active_contexts:
            if ctx in potential_actions:
                return potential_actions[ctx]
                
        return None

    def get_setting(self, key, default_val=None):
        """
        Safe access to the 'defaults' section of the JSON.
        Example: layout_map.get_setting("sequence_length", 16)
        """
        return self._defaults.get(key, default_val)

    # --- LED Retrieval Methods ---

    def get_transport_led(self, name):
        """Returns (status, channel, data1) for a transport action or None"""
        return self._led_map["transport"].get(name)

    def get_sequencer_led(self, step):
        """Returns (status, channel, data1) for a sequence step or None"""
        return self._led_map["sequencer"].get(step)

    def get_sequencer_leds(self):
        """Returns the entire dictionary of sequencer LEDs {step: (midi...)}"""
        return self._led_map["sequencer"]

    def leds_assigned(self):
        """Returns True if any LEDs were loaded"""
        return bool(self._led_map["transport"] or self._led_map["sequencer"])


layout_map = LayoutManager()