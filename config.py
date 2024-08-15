class Config:

	INIT_MODE = 6

	SELECT_PARAM_STEP = True

	CHANNEL_OFFSET = 1
	"""WebMidi, the API used to create the layout, allows MIDI communication on the browser. It
		uses a 0-15 for MIDI channels rather than 1-16 like FL Studio. This is the offset for 
		that. It is unlikely that this needs to be changed."""

	FOLLOW_TRACK = True			
	""" Set to True if you want your encoders to automatically adjust what mixer tracks 
		they control based on the currently highlighted track. Only relavent if you have 
		encoders set to control specific tracks. This is used in conjuction with the 
		Number of Mixer Tracks setting on the web app. For example, if you have a controller 
		set to control mixer tracks 1-8, if you highlight any track between 9-16, they will then control 
		tracks 9-16 respectively. This affects track level, arm, mute, solo and pan.""" 
		
	PREVENT_PASSTHROUGH = False
	""" True will prevent any unset MIDI messages from reaching FL Studio. False will 
		allow them to be set within FL via the Link to Controller option. It is probably better to
		set each button/knob to pass when linking is desired and leaving this True but
		the option is here"""

	ALLOW_KEYS = True
	"""This works with PREVENT_PASSTHROUGH. This will allow MIDI data with 144 or 128 MIDI id to 
		pass through and block everything else. This allows a keyboard notes to be played 
		but all other data blocked. Only relavent if PREVENT_PASSTHROUGH is True."""


	PATTERN_CHANGE_WAIT = True	
	""" This only affects pattern changes when using the 'Select Pattern *' where buttons are 
		set with specific patterns to change to when pushed. If set to true, the pattern will not
		change until the end of the current bar. False will mean patterns are changed immediately."""


	SEQUENCE_LEDS_ALWAYS_ON = False
	""" Use True if your layout has a dedicated sequencer that does not have other functions 
		attached to the same buttons and you have LEDs functionality set up for the sequencer.
		Use False if the same buttons used for sequencing are also used for keys or other functions 
		and you do not want sequencer status always reflected."""

	JOGWHEEL_USES_SAME_MIDI_CC = True  
	"""	Specific for jog wheels, as some use the same Midi ID and CC number for both directions but 
		different MIDI 2 (Velocity) values to differ between the two. Set to True if this is the case.
		If different CC values are used, then set to False. """

	KEYBOARD_CHROMATIC = True
	"""True will keep the keyboard chromatic no matter the root and scale setting. Changing the root and scale will 
		only affect random note generation. If False, the keyboard will only play notes from the selected scale."""

	ROOT_NOTE = "C"
	SCALE = "Harmonic Minor"


	"""Root Note and Scale combined will set the default scale the script opens with. These can both be changed
		with a MIDI controller if you dedicate buttons to it. It may be easier, though, to change the values here
		and reload the script and dedicated the buttons to a more commonly used function.
		
		Valid note and scale entries are:
			["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
			["Major", "Natural Minor", "Harmonic Minor", "Dorian", "Mixolydian", "Minor Pentatonic", "Chromatic"] """

	PITCH_BEND = True
	"""True enables pitch bend."""

	MIXER_SCROLL_MAX = 32