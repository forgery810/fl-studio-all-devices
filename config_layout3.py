cl = {"leds": {},

      "jog_wheel": {
          '91': {'channel': 1, 'midi': [176, 60, 1, 176], 'actions': ['jog_wheel_up', ''], 'toggle': 0, 'track': 0},
          '92': {'channel': 1, 'midi': [176, 60, 65, 176], 'actions': ['jog_wheel_down', ''], 'toggle': 0, 'track': 0}, 
                 },

      "defaults": {"octaves": 5, "sequence_length": 16, "sequence_length": 16, "seq_mult": 0, "plugin_control": 1,
                   "mixer_tracks": 1, "Keyboard": 0, "Sequencer": 0, "keyboard_count": 5,
                   "modes": ["Buttons", "Keyboard", "Sequencer", ], "levels_control_parameter": 1, "colors": [],
                   "root": "C", "scale": "Major", "windows": [4, 0, 2, 1, 3, ]},

      "encoders": {
          '13': {'channel': 1, 'midi': [176, 14, 3, 176], 'actions': ['selected_level', 'selected_level'], 'toggle': 0, 'track': 0},
          '14': {'channel': 1, 'midi': [176, 15, 0, 176], 'actions': ['selected_pan', 'selected_level'], 'toggle': 0, 'track': 0},
          '15': {'channel': 1, 'midi': [176, 16, 0, 176], 'actions': ['set_efx_track', 'selected_level'], 'toggle': 0, 'track': 0},
          '16': {'channel': 1, 'midi': [176, 17, 0, 176], 'actions': ['mixer_level', 'mixer_pan'], 'toggle': 0, 'track': 1},
          '17': {'channel': 1, 'midi': [176, 18, 0, 176], 'actions': ['mixer_level', 'mixer_pan'], 'toggle': 0, 'track': 2},
          '18': {'channel': 1, 'midi': [176, 19, 0, 176], 'actions': ['mixer_level', 'mixer_pan'], 'toggle': 0, 'track': 3},
          '19': {'channel': 1, 'midi': [176, 20, 0, 176], 'actions': ['mixer_level', 'mixer_pan'], 'toggle': 0, 'track': 4},
          '20': {'channel': 1, 'midi': [176, 21, 0, 176], 'actions': ['mixer_level', 'mixer_level'], 'toggle': 0, 'track': 5}, 
        },

      "buttons": {
          '1':  {'channel': 1, 'midi': [176, 24, 0, 176], 'actions': ['change_mode', 'solo'], 'toggle': 0, 'track': 0},
          '2':  {'channel': 1, 'midi': [176, 25, 0, 176], 'actions': ['down', 'solo'], 'toggle': 0, 'track': 0},
          '3':  {'channel': 1, 'midi': [176, 26, 0, 176], 'actions': ['up', 'solo'], 'toggle': 0, 'track': 0},
          '4':  {'channel': 1, 'midi': [176, 27, 0, 176], 'actions': ['enter', 'solo'], 'toggle': 0, 'track': 0},
          '5':  {'channel': 1, 'midi': [144, 28, 0, 176], 'actions': ['rotate_set_windows', 'solo'], 'toggle': 0, 'track': 0},
          '6':  {'channel': 1, 'midi': [176, 29, 0, 176], 'actions': ['set_root_note', 'increment_scale'], 'toggle': 0, 'track': 0},
          '7':  {'channel': 1, 'midi': [176, 30, 0, 176], 'actions': ['rand_pat', 'rand_trigs'], 'toggle': 0, 'track': 0},
          '8':  {'channel': 1, 'midi': [176, 31, 0, 176], 'actions': ['shift', 'solo'], 'toggle': 0, 'track': 0},
          '9':  {'channel': 1, 'midi': [144, 93, 0, 144], 'actions': ['stop', 'solo'], 'toggle': 0, 'track': 0},
          '10': {'channel': 1, 'midi': [144, 94, 0, 144], 'actions': ['start', 'solo'], 'toggle': 0, 'track': 0},
          '11': {'channel': 1, 'midi': [144, 95, 0, 144], 'actions': ['record', 'solo'], 'toggle': 0, 'track': 0},
          '12': {'channel': 1, 'midi': [144, 89, 0, 144], 'actions': ['song_pat', 'solo'], 'toggle': 0, 'track': 0},
          '89': {'channel': 1, 'midi': [144, 98, 0, 144], 'actions': ['left', 'solo'], 'toggle': 0, 'track': 0},
          '90': {'channel': 1, 'midi': [144, 99, 0, 144], 'actions': ['right', 'solo'], 'toggle': 0, 'track': 0}, 
          },

      "keyboard": {
                   '53': {'channel': 10, 'midi': [144, 52, 0, 128], 'actions': ['C#', ''], 'toggle': 0, 'track': 0},
                   # '54': {'channel': 10, 'midi': [144, 53, 0, 128], 'actions': ['D#', ''], 'toggle': 0, 'track': 0},
                   # '55': {'channel': 10, 'midi': [144, 55, 0, 128], 'actions': ['F#', ''], 'toggle': 0, 'track': 0},
                   # '56': {'channel': 10, 'midi': [144, 56, 0, 128], 'actions': ['G#', ''], 'toggle': 0, 'track': 0},
                   # '57': {'channel': 10, 'midi': [144, 57, 0, 128], 'actions': ['A#', ''], 'toggle': 0, 'track': 0},
                   # '58': {'channel': 10, 'midi': [144, 36, 0, 128], 'actions': ['C', ''], 'toggle': 0, 'track': 0},
                   # '59': {'channel': 10, 'midi': [144, 37, 0, 128], 'actions': ['D', ''], 'toggle': 0, 'track': 0},
                   # '60': {'channel': 10, 'midi': [144, 38, 0, 128], 'actions': ['E', ''], 'toggle': 0, 'track': 0},
                   # '61': {'channel': 10, 'midi': [144, 39, 0, 128], 'actions': ['F', ''], 'toggle': 0, 'track': 0},
                   # '62': {'channel': 10, 'midi': [144, 40, 0, 128], 'actions': ['G', ''], 'toggle': 0, 'track': 0},
                   # '63': {'channel': 10, 'midi': [144, 41, 0, 128], 'actions': ['A', ''], 'toggle': 0, 'track': 0},
                   # '64': {'channel': 10, 'midi': [144, 42, 0, 128], 'actions': ['B', ''], 'toggle': 0, 'track': 0},
                   # '65': {'channel': 10, 'midi': [144, 59, 0, 128], 'actions': ['C#', ''], 'toggle': 0, 'track': 0},
                   # '66': {'channel': 10, 'midi': [144, 60, 0, 128], 'actions': ['D#', ''], 'toggle': 0, 'track': 0},
                   # '67': {'channel': 10, 'midi': [144, 61, 0, 128], 'actions': ['F#', ''], 'toggle': 0, 'track': 0},
                   # '68': {'channel': 10, 'midi': [144, 62, 0, 128], 'actions': ['G#', ''], 'toggle': 0, 'track': 0},
                   # '69': {'channel': 10, 'midi': [144, 63, 0, 128], 'actions': ['A#', ''], 'toggle': 0, 'track': 0},
                   # '70': {'channel': 10, 'midi': [144, 43, 0, 128], 'actions': ['C', ''], 'toggle': 0, 'track': 0},
                   # '71': {'channel': 10, 'midi': [144, 44, 0, 128], 'actions': ['D', ''], 'toggle': 0, 'track': 0},
                   # '72': {'channel': 10, 'midi': [144, 45, 0, 128], 'actions': ['E', ''], 'toggle': 0, 'track': 0},
                   # '73': {'channel': 10, 'midi': [144, 46, 0, 128], 'actions': ['F', ''], 'toggle': 0, 'track': 0},
                   # '74': {'channel': 10, 'midi': [144, 47, 0, 128], 'actions': ['G', ''], 'toggle': 0, 'track': 0},
                   # '75': {'channel': 10, 'midi': [144, 48, 0, 128], 'actions': ['A', ''], 'toggle': 0, 'track': 0},
                   # '76': {'channel': 10, 'midi': [144, 49, 0, 128], 'actions': ['B', ''], 'toggle': 0, 'track': 0},
                   # '77': {'channel': 10, 'midi': [144, 66, 0, 128], 'actions': ['C#', ''], 'toggle': 0, 'track': 0},
                   # '78': {'channel': 10, 'midi': [144, 67, 0, 128], 'actions': ['D#', ''], 'toggle': 0, 'track': 0},
                   # '82': {'channel': 10, 'midi': [144, 50, 0, 128], 'actions': ['C', ''], 'toggle': 0, 'track': 0},
                   # '83': {'channel': 10, 'midi': [144, 51, 0, 128], 'actions': ['D', ''], 'toggle': 0, 'track': 0}, 
        },

      "sequencer": {
                    # '21': {'channel': 10, 'midi': [144, 36, 0, 128], 'actions': ['0', '0'], 'toggle': 0, 'track': 0},
                    # '22': {'channel': 10, 'midi': [144, 37, 0, 128], 'actions': ['1', '1'], 'toggle': 0, 'track': 0},
                    # '23': {'channel': 10, 'midi': [144, 38, 0, 128], 'actions': ['2', '2'], 'toggle': 0, 'track': 0},
                    # '24': {'channel': 10, 'midi': [144, 39, 0, 128], 'actions': ['3', '3'], 'toggle': 0, 'track': 0},
                    # '25': {'channel': 10, 'midi': [144, 40, 0, 128], 'actions': ['4', '4'], 'toggle': 0, 'track': 0},
                    # '26': {'channel': 10, 'midi': [144, 41, 0, 128], 'actions': ['5', '5'], 'toggle': 0, 'track': 0},
                    # '27': {'channel': 10, 'midi': [144, 42, 0, 128], 'actions': ['6', '6'], 'toggle': 0, 'track': 0},
                    # '28': {'channel': 10, 'midi': [144, 43, 0, 128], 'actions': ['7', '7'], 'toggle': 0, 'track': 0},
                    # '29': {'channel': 10, 'midi': [144, 44, 0, 128], 'actions': ['8', '8'], 'toggle': 0, 'track': 0},
                    # '30': {'channel': 10, 'midi': [144, 45, 0, 128], 'actions': ['9', '9'], 'toggle': 0, 'track': 0},
                    # '31': {'channel': 10, 'midi': [144, 46, 0, 128], 'actions': ['10', '10'], 'toggle': 0, 'track': 0},
                    # '32': {'channel': 10, 'midi': [144, 47, 0, 128], 'actions': ['11', '11'], 'toggle': 0, 'track': 0},
                    # '33': {'channel': 10, 'midi': [144, 48, 0, 128], 'actions': ['12', '12'], 'toggle': 0, 'track': 0},
                    # '34': {'channel': 10, 'midi': [144, 49, 0, 128], 'actions': ['13', '13'], 'toggle': 0, 'track': 0},
                    # '35': {'channel': 10, 'midi': [144, 50, 0, 128], 'actions': ['14', '14'], 'toggle': 0, 'track': 0},
                    # '36': {'channel': 10, 'midi': [144, 51, 0, 128], 'actions': ['15', '15'], 'toggle': 0, 'track': 0},
                    # '37': {'channel': 10, 'midi': [144, 52, 0, 128], 'actions': ['16', '16'], 'toggle': 0, 'track': 0},
                    # '38': {'channel': 10, 'midi': [144, 53, 0, 128], 'actions': ['17', '17'], 'toggle': 0, 'track': 0},
                    # '39': {'channel': 10, 'midi': [144, 54, 0, 128], 'actions': ['18', '18'], 'toggle': 0, 'track': 0},
                    # '40': {'channel': 10, 'midi': [144, 55, 0, 128], 'actions': ['19', '19'], 'toggle': 0, 'track': 0},
                    # '41': {'channel': 10, 'midi': [144, 56, 0, 128], 'actions': ['20', '20'], 'toggle': 0, 'track': 0},
                    # '42': {'channel': 10, 'midi': [144, 57, 0, 128], 'actions': ['21', '21'], 'toggle': 0, 'track': 0},
                    # '43': {'channel': 10, 'midi': [144, 58, 0, 128], 'actions': ['22', '22'], 'toggle': 0, 'track': 0},
                    # '44': {'channel': 10, 'midi': [144, 59, 0, 128], 'actions': ['23', '23'], 'toggle': 0, 'track': 0},
                    # '45': {'channel': 10, 'midi': [144, 60, 0, 128], 'actions': ['24', '24'], 'toggle': 0, 'track': 0},
                    # '46': {'channel': 10, 'midi': [144, 61, 0, 128], 'actions': ['25', '25'], 'toggle': 0, 'track': 0},
                    # '47': {'channel': 10, 'midi': [144, 62, 0, 128], 'actions': ['26', '26'], 'toggle': 0, 'track': 0},
                    # '48': {'channel': 10, 'midi': [144, 63, 0, 128], 'actions': ['27', '27'], 'toggle': 0, 'track': 0},
                    # '49': {'channel': 10, 'midi': [144, 64, 0, 128], 'actions': ['28', '28'], 'toggle': 0, 'track': 0},
                    # '50': {'channel': 10, 'midi': [144, 65, 0, 128], 'actions': ['29', '29'], 'toggle': 0, 'track': 0},
                    # '51': {'channel': 10, 'midi': [144, 66, 0, 128], 'actions': ['30', '30'], 'toggle': 0, 'track': 0},
                    # '52': {'channel': 10, 'midi': [144, 67, 0, 128], 'actions': ['31', '31'], 'toggle': 0, 'track': 0}, 
},

      "performance": {
                    # '93': {'channel': 10, 'midi': [144, 44, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 0},
                    # '94': {'channel': 10, 'midi': [144, 45, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 1},
                    # '95': {'channel': 10, 'midi': [144, 46, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 2},
                    # '96': {'channel': 10, 'midi': [144, 47, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 3},
                    # '97': {'channel': 10, 'midi': [144, 48, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 4},
                    # '98': {'channel': 10, 'midi': [144, 49, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 5},
                    # '99': {'channel': 10, 'midi': [144, 50, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 6},
                    # '100': {'channel': 10, 'midi': [144, 51, 0, 128], 'actions': ['1', ''], 'toggle': 0, 'track': 7},
                    # '101': {'channel': 10, 'midi': [144, 36, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 0},
                    # '102': {'channel': 10, 'midi': [144, 37, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 1},
                    # '103': {'channel': 10, 'midi': [144, 38, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 2},
                    # '104': {'channel': 10, 'midi': [144, 39, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 3},
                    # '105': {'channel': 10, 'midi': [144, 40, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 4},
                    # '106': {'channel': 10, 'midi': [144, 41, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 5},
                    # '107': {'channel': 10, 'midi': [144, 42, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 6},
                    # '108': {'channel': 10, 'midi': [144, 43, 0, 128], 'actions': ['2', ''], 'toggle': 0, 'track': 7},
                    # '109': {'channel': 10, 'midi': [144, 60, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 0},
                    # '110': {'channel': 10, 'midi': [144, 61, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 1},
                    # '111': {'channel': 10, 'midi': [144, 62, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 2},
                    # '112': {'channel': 10, 'midi': [144, 63, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 3},
                    # '113': {'channel': 10, 'midi': [144, 64, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 4},
                    # '114': {'channel': 10, 'midi': [144, 65, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 5},
                    # '115': {'channel': 10, 'midi': [144, 66, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 6},
                    # '116': {'channel': 10, 'midi': [144, 67, 0, 128], 'actions': ['3', ''], 'toggle': 0, 'track': 7},
                    # '117': {'channel': 10, 'midi': [144, 52, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 0},
                    # '118': {'channel': 10, 'midi': [144, 53, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 1},
                    # '119': {'channel': 10, 'midi': [144, 54, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 2},
                    # '120': {'channel': 10, 'midi': [144, 55, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 3},
                    # '121': {'channel': 10, 'midi': [144, 56, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 4},
                    # '122': {'channel': 10, 'midi': [144, 57, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 5},
                    # '123': {'channel': 10, 'midi': [144, 58, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 6},
                    # '124': {'channel': 10, 'midi': [144, 59, 0, 128], 'actions': ['4', ''], 'toggle': 0, 'track': 7}, 
    }, }