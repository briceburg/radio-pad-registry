# API package
# Import the functions from the original api.py module
import sys
from pathlib import Path

# Import everything from the api.py file
sys.path.insert(0, str(Path(__file__).parent.parent))
import importlib.util
api_spec = importlib.util.spec_from_file_location("api_module", Path(__file__).parent.parent / "api.py")
api_module = importlib.util.module_from_spec(api_spec)
api_spec.loader.exec_module(api_module)

# Re-export the functions from api.py
create_app = api_module.create_app
response = api_module.response
load_players = api_module.load_players
PlayerValidationError = api_module.PlayerValidationError