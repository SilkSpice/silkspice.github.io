# Main entry point for the Warcraft RPG Template

# This structure handles the case where the script is run directly
# or as part of a package. It ensures that imports from game.* work correctly.
import os
import sys

# Add the parent directory (rpg_template) to the Python path
# This allows us to use absolute imports like `from game.game_loop import Game`
# when `main.py` is inside `rpg_template` and `rpg_template` is the CWD.
# If `rpg_template`'s parent is the CWD, then `from rpg_template.game.game_loop import Game` would be used,
# but for simplicity, we assume `rpg_template` is the root for execution.

# Get the absolute path of the directory containing main.py (rpg_template/)
project_root = os.path.dirname(os.path.abspath(__file__))

# If the project_root is not already in sys.path, add it.
# This is useful if you run `python main.py` from within the `rpg_template` directory.
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# If you are running `python rpg_template/main.py` from the parent directory of `rpg_template`,
# then `rpg_template` itself needs to be in the path for `from game...` to work,
# or the parent of `rpg_template` for `from rpg_template.game...`
# The above lines should handle the common case of running from within `rpg_template`.

try:
    from game.game_loop import Game
except ImportError as e:
    print(f"Error importing game modules: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Current working directory: {os.getcwd()}")
    print("Please ensure you are running this script from the `rpg_template` directory,")
    print("or that the `rpg_template` directory is in your PYTHONPATH.")
    sys.exit(1)

def start_game():
    """
    Initializes and starts the game.
    """
    player_name = input("Enter your character's name: ")
    if not player_name:
        player_name = "Adventurer" # Default name

    game_instance = Game(player_name=player_name)
    game_instance.start()

if __name__ == "__main__":
    # Check if running from the correct directory for asset loading
    # data/locations.json should exist relative to the current working directory
    # if CWD is rpg_template. game_loop.py assumes this structure.
    expected_data_path = os.path.join(project_root, "data", "locations.json")
    if not os.path.exists(expected_data_path):
        print(f"Warning: Could not find data file at expected path: {expected_data_path}")
        print(f"Current working directory: {os.getcwd()}")
        print("Please ensure you are running main.py from the 'rpg_template' directory.")
        # Game might still run if paths in game_loop are absolute or relative to game_loop.py,
        # but it's good practice to run from project root.
        # The Game class itself tries to load "data/locations.json" assuming CWD is project_root.

    print("Starting Warcraft RPG Template...")
    start_game()
