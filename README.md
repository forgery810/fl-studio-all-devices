Fl Studio Script Builder is Python script which allows any MIDI controller to work with FL Studio. The layout can be custom designed by the user through a web app available at www.midicontrol.cc. 


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

Two files in the folder allow user control of the script functionality. 
The first, config.py, can be edited by the user. Descriptions of what each setting affects are in that file.
It can be opened in a text editor or IDE to be edited but the name must not be changed.
    
The second file is user_layout.json. This file should be empty when unzipped. The layout data downloaded from the web app listed above should be placed in the folder, replacing the file in the folder. 

Upon opening FL Studio, go to MIDI Options and select the controller in Input and Output, setting both to the same Port. Under device scripts, select the All Devices script.  
  

## Multiple Controllers 

If you have more than one contoller that uses the script, you will need additional instances of it. An additional copy of the folder will be needed for each. The folder can be named anything. Rename the device_no-default.py file. It MUST start with device_ . It can be named anything else after. 

For example:


```sh
device_no-default.py
```

can be changed to

```sh
device_korg_nanoKontrol2.py
```


Open this file and edit the first line. As is, the first line is # name=All Devices. Again, it must start with # name= but after that it can be named anything. This is what will appear in the list of available scripts under MIDI Options. 

```sh
# name=No Default
```

can be change to

```sh
# name=Korg nanoKontrol2
```


## Editing the Layout

Once created, it may be easier in certain situations to edit the user_layout.json file directly, rather than using the web app. 
Even users with no coding experience should have little issue.  
  
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

 
