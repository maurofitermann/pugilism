# Pugilism readme
Pugilism.py is a port of a 5e D&D minigame of the same name, created by [tabletopnotch](www.twitch.tv/tabletopnotch) and released for free.

Knowing the simple rules almost by heart, this is an ongoing personal project I work on to establish and polish my python skills.

After getting a running CLI version, I've started building a TUI to give it a proper look and gamefeel along with a better interfacing and features like character loading and saving, records for characters' fights, and support for optional and more complicated game rules like edges, class cards, and non-reusable cards.

pugilism.py holds the main game definitions and functionality like imports, the "pugilist" python class, functions to parse character data, and the simpler values for core attacks and defenses. 

pugilism_CLI.py is the base working game. It includes core attacks, takes stats into account, and can properly run the base game, albeit with no good way to hide each player's choice of cards.

pugilists.csv is a comma-separated value file with the stats for a handful of example characters. Right now, this means they each have a unique id, a name, and a boolean value for each class the game has cards for.

pugilism_textual.py is my ongoing effort to make a TUI/GUI for the game, using Textualize.io's "Rapid Application Development framework", Textual.