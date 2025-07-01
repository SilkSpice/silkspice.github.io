import json

class Location:
    """
    Represents a single location in the game world.
    """
    def __init__(self, location_id, name, description, exits=None, npc_ids=None, item_ids=None, npcs=None):
        self.location_id = location_id
        self.name = name
        self.description = description
        self.exits = exits if exits else {}  # e.g., {"north": "another_location_id", "south": ...}
        self.npc_ids = npc_ids if npc_ids else [] # IDs of NPCs present, to be loaded
        self.item_ids = item_ids if item_ids else [] # IDs of items available, to be loaded

        # These will hold the actual NPC objects once loaded/spawned
        self.npcs_present = npcs if npcs else [] # List of NPC objects

    def display(self, player_can_see_npcs=True):
        """
        Prints the details of the location.
        """
        print(f"\n--- {self.name} ---")
        print(self.description)

        if self.exits:
            print("\nExits:")
            for direction, target_location_id in self.exits.items():
                print(f"- {direction.capitalize()}") # Later, could show target_location_id or target_location.name

        if self.npcs_present and player_can_see_npcs:
            print("\nPeople here:")
            for npc in self.npcs_present:
                print(f"- {npc.name} ({npc.faction})")

        # TODO: Display items available for pickup

    def add_npc(self, npc):
        """Adds an NPC object to the location."""
        if npc not in self.npcs_present:
            self.npcs_present.append(npc)
            # print(f"{npc.name} has arrived at {self.name}.") # Optional: for dynamic spawning

    def remove_npc(self, npc):
        """Removes an NPC object from the location."""
        if npc in self.npcs_present:
            self.npcs_present.remove(npc)
            # print(f"{npc.name} has left {self.name}.") # Optional

    def get_npc_by_name(self, name):
        """Returns an NPC object in the location by name (case-insensitive)."""
        for npc in self.npcs_present:
            if npc.name.lower() == name.lower():
                return npc
        return None

    def __str__(self):
        return f"Location({self.location_id}: {self.name})"


# --- Static Game Data Loading ---
# In a larger game, this might be in a separate data_manager.py

WORLD_LOCATIONS = {} # Dictionary to store all loaded Location objects: {location_id: Location_object}

def load_locations_from_json(filepath="data/locations.json"):
    """
    Loads location data from a JSON file and populates WORLD_LOCATIONS.
    This version only loads location structure, not NPC objects yet.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            for loc_id, loc_data in data.items():
                WORLD_LOCATIONS[loc_id] = Location(
                    location_id=loc_id,
                    name=loc_data.get("name", "Unknown Location"),
                    description=loc_data.get("description", "No description available."),
                    exits=loc_data.get("exits", {}),
                    npc_ids=loc_data.get("npcs", []), # Store IDs for now
                    item_ids=loc_data.get("items", [])  # Store IDs for now
                )
            print(f"Successfully loaded {len(WORLD_LOCATIONS)} locations from {filepath}")
    except FileNotFoundError:
        print(f"Error: Location data file not found at {filepath}")
        WORLD_LOCATIONS.clear() # Ensure it's empty if file not found
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}")
        WORLD_LOCATIONS.clear()
    return WORLD_LOCATIONS

# Example usage (for testing, will be called from game_loop or main later)
if __name__ == '__main__':
    # Assume rpg_template is the root for pathing if running this file directly
    # For actual game, paths will be relative to main.py or handled by a config
    import os
    # Correct path when running this file directly for testing
    if os.path.exists("data/locations.json"):
        test_locations = load_locations_from_json("data/locations.json")
    elif os.path.exists("../data/locations.json"): # If running from game/ directory
        test_locations = load_locations_from_json("../data/locations.json")
    else:
        print("Could not find locations.json for testing.")
        test_locations = {}

    if test_locations:
        northshire = test_locations.get("northshire_abbey")
        if northshire:
            northshire.display()
            # Example of adding an NPC (NPC class needs to be importable)
            # from character import NPC
            # guard = NPC("Brother Paxton", 100, 5, "Alliance", dialogue=["Light be with you."])
            # northshire.add_npc(guard)
            # northshire.display()
            # found_npc = northshire.get_npc_by_name("Brother Paxton")
            # if found_npc:
            #     print(f"Found: {found_npc.name}")

        elwynn_road = test_locations.get("elwynn_forest_road")
        if elwynn_road:
            elwynn_road.display()
    else:
        print("No locations loaded for testing.")
