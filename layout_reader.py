import json
import os
import sys

# Define the user directory relative to this script
USER_DIR = os.path.join(os.path.dirname(__file__), 'user_files')

def load_config():
    # 1. Try to load user_layout.json from the new folder
    json_path = os.path.join(USER_DIR, 'user_layout.json')
    
    try:
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                print(f"Loading layout from {json_path}")
                return json.load(f)
        
        # FUTURE PROOFING: 
        # If you later want to load *any* json file found in that folder:
        # for filename in os.listdir(USER_DIR):
        #     if filename.endswith(".json"):
        #         ... load and merge logic ...

    except json.JSONDecodeError as e:
        print("----------------")
        print(f"ERROR in user_layout.json: {e}")
        print("----------------")
        return None 
    except Exception as e:
        print(f"Error loading JSON: {e}")

    # 2. Fallback to config_layout.py (now inside user_files package)
    try:
        # We import it from the package structure now
        import user_files.config_layout as config_layout
        print('Loading layout from user_files/config_layout.py')
        return config_layout.cl
    except ImportError:
        pass
        
    print("Error: Could not load layout from user_files.")
    return None