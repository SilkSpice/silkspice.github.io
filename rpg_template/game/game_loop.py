from .location import WORLD_LOCATIONS, load_locations_from_json
from .character import Player, NPC # Assuming NPC definitions might be in data later

# --- NPC Data and Loading ---
# Placeholder for NPC data. In a real game, this would be more extensive
# and likely loaded from a JSON file, similar to locations.
NPC_TEMPLATES = {
    "guard_elwynn": {
        "name": "Elwynn Forest Guard",
        "health": 70,
        "attack_power": 7,
        "faction": "Alliance",
        "dialogue": ["Greetings, traveler. Be wary of kobolds if you venture too far from the road."]
    },
    "monk_trainee": {
        "name": "Monk Trainee",
        "health": 50,
        "attack_power": 5,
        "faction": "Alliance",
        "dialogue": ["Practice makes perfect. The Light guide my fists."]
    }
}

# This dictionary will hold instantiated NPCs, perhaps keyed by a unique ID or their template ID if only one instance
GAME_NPCS = {}

def initialize_npcs():
    """
    Initializes NPCs based on templates and places them in their starting locations.
    This is a simplified version. A more robust system would read NPC placements
    from location data or a dedicated NPC spawn configuration.
    """
    # Clear any existing NPCs in locations if re-initializing
    for loc in WORLD_LOCATIONS.values():
        loc.npcs_present = []

    # Example: Place a guard in Elwynn Forest Road
    if "elwynn_forest_road" in WORLD_LOCATIONS:
        guard_template = NPC_TEMPLATES["guard_elwynn"]
        guard = NPC(
            name=guard_template["name"],
            health=guard_template["health"],
            attack_power=guard_template["attack_power"],
            faction=guard_template["faction"],
            dialogue=guard_template["dialogue"]
        )
        WORLD_LOCATIONS["elwynn_forest_road"].add_npc(guard)
        GAME_NPCS["guard_elwynn_1"] = guard # Store for global access if needed

    # Example: Place a monk trainee in Northshire Abbey
    if "northshire_abbey" in WORLD_LOCATIONS:
        monk_template = NPC_TEMPLATES["monk_trainee"]
        monk = NPC(
            name=monk_template["name"],
            health=monk_template["health"],
            attack_power=monk_template["attack_power"],
            faction=monk_template["faction"],
            dialogue=monk_template["dialogue"]
        )
        WORLD_LOCATIONS["northshire_abbey"].add_npc(monk)
        GAME_NPCS["monk_trainee_1"] = monk


class Game:
    """
    Manages the overall game state and flow.
    """
    def __init__(self, player_name="Adventurer"):
        # Ensure paths are relative to the project root (rpg_template)
        # This assumes main.py is in rpg_template/
        load_locations_from_json("data/locations.json")
        initialize_npcs() # Initialize NPCs after locations are loaded

        self.player = Player(name=player_name, current_location_id="northshire_abbey")
        if self.player.current_location_id not in WORLD_LOCATIONS:
            print(f"Error: Player's starting location '{self.player.current_location_id}' not found!")
            # Fallback to the first loaded location or handle error
            if WORLD_LOCATIONS:
                self.player.current_location_id = list(WORLD_LOCATIONS.keys())[0]
            else:
                raise Exception("No locations loaded, cannot start game.")

        self.current_location = WORLD_LOCATIONS.get(self.player.current_location_id)
        if self.current_location:
            self.player.current_location_id = self.current_location.location_id # Ensure consistency

        self.game_over = False

    def display_prompt(self):
        """Displays the current location and available actions."""
        if not self.current_location:
            print("Error: Current location is not set.")
            self.game_over = True
            return

        self.current_location.display()
        print("\nWhat do you want to do?")
        print("Available actions: move [direction], look, talk [NPC name], inventory, quit")
        # Add more actions as they are implemented (e.g., attack, take, use)

    def handle_input(self, user_input):
        """Parses user input and calls appropriate game actions."""
        if not user_input:
            return

        parts = user_input.lower().split()
        command = parts[0]

        if command == "quit":
            self.game_over = True
            print(f"Thank you for playing, {self.player.name}!")
        elif command == "look":
            # Handled by display_prompt, but can add more detail here if needed
            pass # display_prompt will re-display
        elif command == "inventory":
            self.player.view_inventory()
        elif command == "move":
            if len(parts) > 1:
                direction = parts[1]
                self.move_player(direction)
            else:
                print("Move where? (e.g., 'move north')")
        elif command == "talk":
            if len(parts) > 1:
                npc_name = " ".join(parts[1:])
                self.talk_to_npc(npc_name)
            else:
                print("Talk to whom? (e.g., 'talk Stormwind Guard')")
        # Add more command handlers here (attack, etc.)
        else:
            print("Invalid command. Type 'help' for a list of commands (not implemented yet).")

    def move_player(self, direction):
        """Moves the player to a new location if the exit exists."""
        if not self.current_location:
            print("Cannot move, current location is unknown.")
            return

        if direction in self.current_location.exits:
            next_location_id = self.current_location.exits[direction]
            if next_location_id in WORLD_LOCATIONS:
                self.current_location = WORLD_LOCATIONS[next_location_id]
                self.player.current_location_id = self.current_location.location_id
                print(f"You move {direction}.")
            else:
                print(f"Error: Location '{next_location_id}' not found.")
        else:
            print(f"You can't go {direction} from here.")

    def talk_to_npc(self, npc_name):
        """Initiates dialogue with an NPC in the current location."""
        if not self.current_location:
            print("Cannot talk, current location is unknown.")
            return

        npc = self.current_location.get_npc_by_name(npc_name)
        if npc:
            npc.talk()
        else:
            print(f"There is no one named '{npc_name}' here.")

    def start(self):
        """Starts the main game loop."""
        print(f"Welcome to Warcraft RPG, {self.player.name}!")
        print("Your adventure begins...")

        while not self.game_over:
            self.display_prompt()
            try:
                user_input = input("> ").strip()
                self.handle_input(user_input)
            except EOFError: # Handle Ctrl+D or other EOF signals
                print("\nExiting game.")
                self.game_over = True
            except KeyboardInterrupt: # Handle Ctrl+C
                print("\nExiting game via interrupt.")
                self.game_over = True
            print("-" * 20) # Separator for clarity


if __name__ == '__main__':
    # This is for testing the game loop directly.
    # Ensure you are in the `rpg_template` directory when running this.
    # If character.py or location.py are not found, Python's import system
    # might need you to run from the project root or adjust PYTHONPATH.

    # To run this test, navigate to the `rpg_template` directory and run:
    # python -m game.game_loop
    # (or ensure rpg_template is in your PYTHONPATH and run python game/game_loop.py)

    print("Testing game_loop.py...")
    # Create a mock game environment for testing

    # Since load_locations_from_json is now called in Game.__init__
    # and uses relative paths from where main.py would be, we need to ensure
    # the CWD is `rpg_template` or adjust paths.
    # For simplicity, we assume this test is run from `rpg_template` root.

    # This simple test will likely fail if not run with `python -m game.game_loop`
    # from the `rpg_template` directory, due to relative imports.
    # The `main.py` will be the proper way to start.

    try:
        # Test if locations load (they should if paths are correct)
        if not WORLD_LOCATIONS:
             # Attempt to load with adjusted path if running directly from game/
            import os
            if os.path.exists("../data/locations.json"):
                load_locations_from_json("../data/locations.json")
                initialize_npcs() # Also initialize NPCs with correct location data
            else:
                print("Test Error: Could not load locations for game_loop test.")

        if WORLD_LOCATIONS:
            print(f"Locations loaded for test: {list(WORLD_LOCATIONS.keys())}")
            game_instance = Game("TestPlayer")
            print(f"Player starting location: {game_instance.player.current_location_id}")
            if game_instance.current_location:
                print(f"Current location object: {game_instance.current_location.name}")
                game_instance.current_location.display()

                # Test NPC interaction
                monk_npc = game_instance.current_location.get_npc_by_name("Monk Trainee")
                if monk_npc:
                    monk_npc.talk()
                else:
                    print("Monk Trainee not found in starting location for test.")

                # Test movement
                game_instance.move_player("south")
                if game_instance.current_location:
                    game_instance.current_location.display()
                    guard_npc = game_instance.current_location.get_npc_by_name("Elwynn Forest Guard")
                    if guard_npc:
                        guard_npc.talk()
                    else:
                        print("Elwynn Forest Guard not found in moved location for test.")
                else:
                    print("Failed to move or new location is None.")
            else:
                print("Test Error: game_instance.current_location is None after init.")
        else:
            print("Skipping direct game_loop tests as WORLD_LOCATIONS is empty.")
            print("Run from main.py or ensure paths are correct for direct testing.")

    except ImportError as e:
        print(f"ImportError during game_loop.py test: {e}")
        print("This test is best run via `python -m game.game_loop` from the `rpg_template` directory,")
        print("or by running the `main.py` script.")
    except Exception as e:
        print(f"An unexpected error occurred during game_loop.py test: {e}")
