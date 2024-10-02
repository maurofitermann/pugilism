# imports
import random
import math
import csv
import math

# moves
attacks_core = [
{"name":"Head Jab","target":"H","type":"J","fatigue":0,"POW":2},
{"name":"Head Strike","target":"H","type":"S","fatigue":1,"POW":5},
{"name":"Head Heavy","target":"H","type":"H","fatigue":2,"POW":8},
{"name":"Body Jab","target":"B","type":"J","fatigue":0,"POW":1},
{"name":"Body Strike","target":"B","type":"S","fatigue":1,"POW":4},
{"name":"Body Heavy","target":"B","type":"H","fatigue":2,"POW":6}
]

defenses_core = [
    {"name":"Body Protect", "fatigue":0, "description":"Negate all BODY attacks"},
    {"name":"Head Protect", "fatigue":0, "description":"Negate all HEAD attacks"},
    {"name":"Duck & Weave", "fatigue":2, "description":"If one attack against you is  BODY and the other is HEAD, negate both."},
    {"name":"Footwork", "fatigue":3, "description":"Negate all non-JAB attacks"},
    {"name":"General Defense", "fatigue":0, "description":"Negate 1 Heavy attack OR exactly two jabs."},
    {"name":"Counter", "fatigue":0, "description":"negate 1 Heavy attack and deal HALF its POWER back to the opponent."}
]

def get_priority_value(values):
    class_dice = {
        "Barbarian": 12,
        "Fighter": 10,
        "Paladin": 10,
        "Ranger": 10,
        "Bard": 8,
        "Cleric": 8,
        "Druid": 8,
        "Monk": 8,
        "Rogue": 8,
        "Warlock": 8,
        "Sorcerer": 6,
        "Wizard": 6
    }
    
    hit_die = 0
    
    for value in values:
        if value in class_dice:
            hit_die = max(hit_die, class_dice[value])
        return hit_die

class pugilist:
  def __init__(self, id, name, strength, dexterity, constitution, classes):
    self.id=id
    self.name = name
    self.classes = classes
    self.strength = strength
    self.dexterity = dexterity
    self.constitution = constitution

    self.hit_die = get_priority_value(classes)
    
    if "monk" in self.classes:
        self.edges = 1 + max(math.floor((strength-10)/5), 0) + max(math.floor((dexterity-10)/5), 0) # FIX: Scores below 10 →  wrong values
    else:
        self.edges = max(math.floor((strength-10)/5), 0) + max(math.floor((dexterity-10)/5), 0)
    
    self.composure: int = ...

    self.winded = False

  def ready(self):
    self.composure = 15+max(random.randint(1, self.hit_die),random.randint(1, self.hit_die))+math.floor((self.constitution-10)/2)
    self.initiative = math.floor((self.dexterity-10)/2)

  def __str__(self):
    return f"{self.name}"

  def tire(self, x):
      self.composure = max( self.composure - x, 1)

  def suffer(self, x):
      self.composure -= x

  def stand(self):
    self.winded = True
    self.composure = 15 + random.randint(1, self.hit_die) +math.floor((self.constitution-10)/2)

def getModifier(ability_score):
    modifier = math.floor((ability_score-10)/2)
    return modifier

# file path to CSV file
character_data_file = './pugilists.csv'

# Function to convert the csv boolean value(s) to a boolean
def str_to_bool(s):
    return s.lower() == 'true'

# Read the CSV file
with open(character_data_file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    # Process each row in the CSV
    pugilists=[]
    for row in csv_reader:
        classes = ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard']
        character_classes = [cls for cls in classes if str_to_bool(row[cls])] # No I will never support the Alert feat. NEVER


        # Save the character object in a dictionary
        #characters[f'c{character_id}'] = character
        character=pugilist(int(row['id']), row['name'], int(row['Strength']), int(row['Dexterity']), int(row['Constitution']), character_classes)
        pugilists.append(character)