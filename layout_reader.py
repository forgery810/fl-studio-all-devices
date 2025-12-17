import json
import os 
import sys

def load_config():
	try:
		json_path = os.path.join(os.path.dirname(__file__), 'user_layout.json')
		if os.path.exists(json_path):
			with open(json_path, 'r') as f:
				print("Loading layout from user_layout.json")
				return json.load(f)
	except json.JSONDecodeError as e:
		print("----------------")
		print(f"ERROR in user_layout.json: {e}")
		print("Please fix the JSON syntax error or remove json entirely to load config_layout.py dict instead.")
		print("----------------")
		return None # Stop loading to avoid confusing fallback
	except Exception as e:
		print(f"Error loading user_layout.json: {e}")


	try:
		import config_layout
		print('Loading layout from config_layout.py')
		return config_layout.cl
	except ImportError:
		print("Error: could not load config file from user_layout.json or config_layout.py.")
		print("Make sure there is either a json file in user_layout.json or a dictionary in config_layout.py.")
		print("If not, go to www.midicontrol.cc/script-builder/build to create one.")