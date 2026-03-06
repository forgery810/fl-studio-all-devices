Fl Studio Script Builder is Python script which allows any MIDI controller to work with FL Studio. The layout can be custom designed by the user through a web app available at www.midicontrol.cc. 

1.0.5 Update - 3/6/2025

- Fixed recent update
- "Keyboard Always On" and "Sequencer Always On" under default setting were not functioning. This issue is now fixed. This can now be set per controller layout rather than globally for all controllers using the same script. 
- With "Keyboard Always On" set to true, any 144/128 MIDI message not set in the layout will play notes. This is aimed at controllers with keys where the user wants them always to play notes. 
- With "Sequencer Always On" set to true, buttons set in the sequencer portion of the layout will always add remove trigs, regardless of mode. This is for users who want a dedicated sequencer. 
- "Sequencer Always On" overrides "Keyboard Always On" if both are set to true.    

1.0.0 Update - 12/27/2025 

- Script now appears in FL Studio as "All Devices" rather than "No Default".
- layout files (.json files) are must now be placed in the user_files folder. config.py is also found in this folder
- Multiple controllers can now be handled by the same script instance. The script will look in the LAYOUT_MAP     variable in config.py to search the controller name with a matching .json file. user_layout.json will be used if no matching layouts are found. 
- config_layout.py no longer works with the script. Legacy users will have to convert their previous layout dictionary to a json file and placed in the user_files folder. A web converter can be used for this task.

0.9.8 Update - 12/18/2025

- JSON files (user_layout.json) are now used to configure the layout, instead of pasting code into config_layout.py
- Script will function with the config_layout.py code if user_layout.json is empty for past users

0.9.0 Update - 8/11/2025

- shift pattern left/right now includes note data (not panning)
- select next channel function added
- randomize selected channels function added. randomizes the trigs of selected channels
- randomize entire pattern function added
- randomize plugin function added. randomizes all parameters of selected plugin 
- double pattern function added. doubles the length of entire pattern, note and trig data included, up to 512 steps
  


## Installation

Download by clicking the green Code button above and selecting Download ZIP. Unzip the download and place the folder in the following directory:  

```sh
%userprofile%\Documents\Image-Line\FL Studio\Settings\Hardware
```
When unzipped, everything should be in a folder named something like fl-studio-all-devices.
This entire folder should be placed in the above directory.

The user_files folder contains two files that allow user control of the script functionality. 
The first, config.py, can be edited by the user. Descriptions of what each setting affects are in that file.
It can be opened in a text editor or IDE to be edited but the name must not be changed.
    
The second file is user_layout.json. This file should be empty when unzipped. The layout data downloaded from the web app listed above should be placed in the folder, replacing the file in the folder. 

Upon opening FL Studio, go to MIDI Options and select the controller in Input and Output, setting both to the same Port. Under device scripts, select the All Devices script.  

## Multiple Controllers 
  
More than one controller can be controlled with the script. A .json file for each must be placed in the user_files folder and the LAYOUT_MAP variable must be edited to reflect the changes.

```sh
  #  LAYOUT_MAP = {
  #   "default": "user_layout.json", 
  #   "name_of_controller": "name_of_file.json",
  #   "name_of_controller_2": "name_of_file_2.json",
  #         }
```

  name_of_controller must match what appears in FL Studio MIDI options. The name will also appear in the View - Script Output window for the controller. It cannot be set by the user. The .json file can have any name. 

## Editing the Layout

Once created, it may be easier in certain situations to edit the user_layout.json file directly, rather than using the web app. Even users with no coding experience should have little issue.  
  
Look up an web based JSON editor for an easier way to edit. 

The options.txt file is a reference for the function names that can be assigned to controller outputs. 
Open the options.txt file in the script folder to find the correct data to input. As an example, we can edit the button currently set to metronome to focus the browser instead. Looking at user_layout.json, we find this entry,

```sh
    "8": {
      "actions": [
        "metronome",
        "escape"
      ],
      "channel": 1,
      "midi": [
        176,
        49,
        0,
        176
      ],
      "toggle": 0,
      "track": 0
    },
```

options.txt has this entry:
```sh
Focus Browser - focus_browser
```

Copy the function name and replace the previous entry resulting it:

```sh
    "8": {
      "actions": [
        "focus_browser",
        "escape"
      ],
      "channel": 1,
      "midi": [
        176,
        49,
        0,
        176
      ],
      "toggle": 0,
      "track": 0
    },
```

The first entry, the one changed here, controls the function when unshifted. Escape will be active when shift is active.

## Troubleshooting

If you have issues, in FL Studio, go to View and click Script Output. Copy the error info you see there. 
Either create a github issue or, presuming you found out about this script via YouTube, post a the issue there with the copied data. 

 
