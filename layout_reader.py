import json
import os
import device
import sys


try:
    import user_files.config as config
    # print(config.Config.LAYOUT_MAP)
    # Default to a simple structure if LAYOUT_MAP is missing
    LAYOUT_MAP = getattr(config.Config, 'LAYOUT_MAP', {'default': 'user_layout.json'})
except ImportError:
    LAYOUT_MAP = {'default': 'user_layout.json'}

USER_DIR = os.path.join(os.path.dirname(__file__), 'user_files')

def load_config():
    """
    Determines which JSON to load based on the connected Device Name.
    """
    
    # 1. Get the name of the controller for this specific instance
    # FL Studio runs this script in a separate context for each controller,
    # so device.getName() is unique to the hardware triggering the script.
    current_device_name = device.getName()
    print(f"Device Detected: '{current_device_name}'")
    print(LAYOUT_MAP)
    # 2. Look up the filename in the config
    if current_device_name in LAYOUT_MAP:
        target_file = LAYOUT_MAP[current_device_name]
        print(f"Layout match found. Loading: {target_file}")
    else:
        target_file = LAYOUT_MAP.get('default', 'user_layout.json')
        print(f"No specific map found for '{current_device_name}'. Using default: {target_file}")

    # 3. Load the file
    json_path = os.path.join(USER_DIR, target_file)
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: {target_file} is corrupted. {e}")
            return None
    else:
        print(f"ERROR: Expected file '{target_file}' not found in user_files.")
        return None