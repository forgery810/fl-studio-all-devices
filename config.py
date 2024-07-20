class Config:

	INIT_MODE = 6

	SELECT_PARAM_STEP = True

	CHANNEL_OFFSET = 1
	###

	FOLLOW_TRACK = True			
	""" Set to True if you want your encoders to automatically adjust what mixer tracks 
		they control based on the currently highlighted track. Only relavent if you have 
		encoders set to control specific tracks. This is used in conjuction with the 
		Number of Mixer Tracks setting on the web app. For example, if you have a controller 
		set to control mixer tracks 1-8, if you highlight track 9, they will then control 
		tracks 9-16 respectively. This affects track level, arm, mute, solo and pan.""" 
		
	PREVENT_PASSTHROUGH = True
	""" True will prevent any unset MIDI messages from reaching FL Studio. False will 
		allow them to be set within FL via the Link to Controller option. It is probably better to
		set each button/knob to pass when linking is desired and leaving this True but
		the option is here"""


	PATTERN_CHANGE_WAIT = True


