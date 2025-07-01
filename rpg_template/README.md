# Warcraft RPG Template

This is a text-based RPG template set in the Warcraft universe.
It provides a basic structure for creating your own adventures in Azeroth.

## Current Features

*   **Character Representation**: Basic `Player` and `NPC` classes with health, attack power.
*   **Location System**: `Location` class to define areas with descriptions, exits, and NPCs.
*   **Game Data**: Locations are loaded from `data/locations.json`. Sample NPCs are defined in `game_loop.py`.
*   **Basic Game Loop**:
    *   Player can navigate between locations using directional commands (e.g., "move south").
    *   Player can "look" to see location details.
    *   Player can "talk" to NPCs in the current location.
    *   Player can view their (currently empty) "inventory".
    *   Player can "quit" the game.
*   **Simple Combat Mechanics**: Characters can attack each other (not yet integrated into player commands).
*   **Warcraft Setting**: Initial locations (Northshire Abbey, Elwynn Forest) and NPCs provide a Warcraft flavor.

## How to Run

1.  **Navigate to the project directory**:
    Open your terminal or command prompt and change to the `rpg_template` directory.
    ```bash
    cd path/to/your/rpg_template
    ```

2.  **Run the game**:
    Execute the `main.py` script using Python.
    ```bash
    python main.py
    ```
    (If you have multiple Python versions, you might need to use `python3 main.py`)

3.  **Play the game**:
    *   You will be prompted to enter your character's name.
    *   Follow the on-screen prompts and use commands like:
        *   `move [north/south/east/west]`
        *   `look`
        *   `talk [NPC name]` (e.g., `talk Monk Trainee`)
        *   `inventory`
        *   `quit`

## Project Structure

*   `main.py`: Main entry point for the game. Initializes and starts the game loop.
*   `game/`: Contains the core game logic.
    *   `__init__.py`: Makes `game` a Python package.
    *   `character.py`: Defines `Character`, `Player`, and `NPC` classes.
    *   `location.py`: Defines the `Location` class and loads location data.
    *   `game_loop.py`: Contains the main `Game` class, game loop, input parsing, and NPC initialization.
*   `data/`: Contains game content.
    *   `__init__.py`: Makes `data` a Python package.
    *   `locations.json`: JSON file defining game locations, their descriptions, exits, and NPC placeholders.
*   `utils/`: Intended for helper functions (currently empty).
    *   `__init__.py`: Makes `utils` a Python package.
*   `README.md`: This file.

## Future Enhancements (Ideas)

*   Combat system accessible via player commands.
*   Item system (pickup, use, drop).
*   Quest system.
*   More sophisticated NPC interactions and dialogues.
*   Saving and loading game progress.
*   Expanding the world with more locations, NPCs, and lore.
*   Loading NPC data from JSON files.
*   Shops and trading.
*   Skills and abilities.

This template provides a starting point. Feel free to expand upon it!
