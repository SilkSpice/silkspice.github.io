class Character:
    """
    Base class for all characters in the game (Player, NPCs, enemies).
    """
    def __init__(self, name, health, attack_power, faction="Neutral"):
        self.name = name
        self.health = health
        self.max_health = health  # Store max health for healing
        self.attack_power = attack_power
        self.faction = faction    # e.g., "Alliance", "Horde", "Neutral", "Monster"
        self.is_alive = True

    def take_damage(self, damage):
        """
        Reduces character's health by the damage amount.
        Checks if the character is still alive.
        """
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
            print(f"{self.name} has been defeated!")
        else:
            print(f"{self.name} takes {damage} damage, {self.health}/{self.max_health} HP remaining.")

    def attack(self, target):
        """
        Attacks another character.
        """
        if not self.is_alive:
            print(f"{self.name} cannot attack, they are defeated.")
            return
        if not target.is_alive:
            print(f"{target.name} is already defeated.")
            return

        print(f"{self.name} attacks {target.name} for {self.attack_power} damage!")
        target.take_damage(self.attack_power)

    def __str__(self):
        return f"Name: {self.name}, HP: {self.health}/{self.max_health}, Faction: {self.faction}"


class Player(Character):
    """
    Represents the player character.
    """
    def __init__(self, name, health=100, attack_power=10, faction="Alliance", current_location_id=None):
        super().__init__(name, health, attack_power, faction)
        self.inventory = []  # List of item objects or item IDs
        self.quests = {}     # Quest_id: status (e.g., "accepted", "completed")
        self.current_location_id = current_location_id # Will be set by the game

    def add_item_to_inventory(self, item_name):
        """Adds an item to the player's inventory."""
        self.inventory.append(item_name)
        print(f"{item_name} added to inventory.")

    def view_inventory(self):
        """Displays the player's inventory."""
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:")
            for item in self.inventory:
                print(f"- {item}")

    def __str__(self):
        base_info = super().__str__()
        return f"{base_info}, Location: {self.current_location_id}"


class NPC(Character):
    """
    Represents a Non-Player Character.
    """
    def __init__(self, name, health, attack_power, faction, dialogue=None, trades=None, quests_given=None):
        super().__init__(name, health, attack_power, faction)
        self.dialogue = dialogue if dialogue else ["Hello there, traveler."] # Default dialogue
        self.trades = trades if trades else {} # item_they_want: item_they_give
        self.quests_given = quests_given if quests_given else [] # list of quest IDs

    def talk(self):
        """NPC delivers a line of dialogue."""
        # Simple dialogue system for now, can be expanded
        if self.dialogue:
            print(f"[{self.name}]: {self.dialogue[0]}") # Print the first line
            if len(self.dialogue) > 1: # Cycle dialogue if more than one line
                self.dialogue.append(self.dialogue.pop(0))
        else:
            print(f"{self.name} has nothing to say.")

    def __str__(self):
        return super().__str__()

# Example Usage (for testing purposes, will be removed or commented out later)
if __name__ == '__main__':
    hero = Player("Sir Reginald", health=150, attack_power=15, faction="Alliance")
    print(hero)
    hero.add_item_to_inventory("Health Potion")
    hero.view_inventory()

    guard = NPC("Stormwind Guard", health=80, attack_power=12, faction="Alliance", dialogue=["For the Alliance!", "Move along."])
    print(guard)
    guard.talk()
    guard.talk()

    kobold = Character("Kobold Geomancer", health=30, attack_power=8, faction="Monster")
    print(kobold)

    hero.attack(kobold)
    kobold.attack(hero)
    hero.attack(kobold)
    hero.attack(kobold) # Kobold should be defeated
    hero.attack(kobold) # Should not attack defeated target
    kobold.attack(hero) # Defeated kobold should not attack
    print(hero)
