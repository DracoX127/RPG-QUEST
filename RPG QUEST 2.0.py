from typing import Any, Dict, Tuple
import copy
import threading
import platform
import select
import random
import time
import json
import sys
import os
import importlib.util

from arena_combat import run_arena_style_combat as _arena_combat_engine

'''
1. Starlight Armory - Enchantment ✅
2. Obsidian Anvil - Repairing ✅
3. Trade ✅
4. Sapphire Docks - Fishing ✅
5. Goldspire Market - Exclusive Items ✅
5. Arena Duel Clash
6. Arena Duel Clash - Potion of Strength and Defense
6. Arena Duels
7. Arena Knockout
6. Adventure
7. Rotfang Depths - Boss Arena
'''

#clear player save
'''
with open("players.json", "w") as file:
    json.dump({}, file)
os.system('git add players.json')
os.system('git commit -m "player save"')
os.system('git push')
quest()
'''

# =========PREFIXES, MIDDLES, SUFFIXES=========
prefixes = [
    "Shadow", "Iron", "Ghost", "Night", "Steel", "Storm", "Fire", "Frost", "Dragon", "Thunder",
    "Blood", "Stone", "Dark", "Silver", "Crystal", "Wind", "Dusk", "Ember", "Flame", "Grim",
    "Ice", "Lunar", "Mystic", "Phantom", "Razor", "Savage", "Silent", "Sky", "Solar", "Spirit",
    "Star", "Swift", "Valkyrie", "Venom", "Void", "Wolf", "Zephyr", "Arcane", "Ash", "Bane",
    "Beast", "Black", "Blaze", "Bright", "Chaos", "Claw", "Cold", "Cinder", "Dagger", "Death",
    "Deep", "Dire", "Dread", "Edge", "Eternal", "Fang", "Glory", "Hawk", "Hell", "Jade",
    "King", "Lion", "Lone", "Midnight", "Nova", "Pierce", "Rage", "Raven", "Reaper", "Smoke",
    "Soul", "Sun", "Talon", "Tide", "Tomb", "Toxic", "Venge", "Viper", "Wraith", "Zenith",
    "Zodiac", "Ashen", "Blight", "Brimstone", "Chrome", "Crimson", "Doom", "Echo",
    "Feral", "Frostbite", "Gale", "Gloom", "Grave", "Hallowed", "Icefang", "Ivory",
    "Jagged", "Keen", "Knight", "Lethal", "Magma", "Noble", "Obsidian", "Omen", "Pale",
    "Quake", "Radiant", "Rogue", "Rune", "Seeker", "Shade", "Shattered", "Skull",
    "Slayer", "Specter", "Spine", "Terror", "Twilight", "Umbral", "Vicious",
    "Wild", "Wrath", "Wretched", "Corrupted", "Darkened", "Deadly", "Desolate",
    "Enchanted", "Fierce", "Haunted", "Infernal", "Lost", "Malevolent", "Molten",
    "Piercing", "Raging", "Sinister", "Sorrow", "Spectral", "Spellbound", "Tempered",
    "Vengeful", "War", "Wicked", "Zealous", "Zeroth", "Abyssal", "Amber", "Aquila",
    "Berserk", "Celestial", "Cobalt", "Crag", "Cryptic", "Dawn", "Duskborn",
    "Ebon", "Emberglow", "Frostwind", "Gilded", "Gloomshade", "Harrow",
    "Ironclad", "Jadefire", "Kiln", "Luminous", "Moonlit", "Nether", "Onyx", "Pyre",
    "Quicksilver", "Runebound", "Sable", "Seismic", "Serrated", "Shard", "Silentfall",
    "Skyfire", "Smolder", "Snowdrift", "Solaris", "Stormborn", "Sunfire", "Tempest",
    "Thunderstrike", "Tundra", "Umber", "Voidborne", "Vortex", "Wildfire", "Winter",
    "Wither", "Zephyrwind", "Zodiacal", "Ardent", "Aurora", "Blazing", "Boulder",
    "Brumal", "Cinderfall", "Cloud", "Crimsonfire", "Dreadnought", "Eclipse", "Emberstorm",
    "Frostfang", "Galeheart", "Graveborn", "Iceveil", "Ironfang", "Jaggededge",
    "Knightfall", "Lurking", "Moonshadow", "Nighthawk", "Obsidianflame", "Phantomshade",
    "Quartz", "Ravenwing", "Runic", "Shadowflame", "Silverwind", "Stormwatch", "Thorn",
    "Thunderclap", "Tidebreaker", "Twilightfall", "Voidwalker", "Windshear", 
    "Alex", "Ben", "Cara", "Dylan", "Ella", "Finn", "Grace", "Hannah", "Ian", "Jade",
    "Kai", "Liam", "Mia", "Nina", "Owen", "Piper", "Quinn", "Rory", "Sage", "Tara",
    "Uma", "Vera", "Will", "Xander", "Yara", "Zane", "Adam", "Bella", "Caleb", "Daisy",
    "Eli", "Fiona", "Gavin", "Hazel", "Isaac", "Jenna", "Kara", "Leo", "Maya", "Noah",
    "Olivia", "Paige", "Reed", "Sara", "Theo", "Violet", "Wyatt", "Zoe", "Aaron", "Bria",
    "Cody", "Daphne", "Evan", "Faith", "Gabe", "Hailey", "Ivan", "June", "Kris", "Lara",
    "Mark", "Nora", "Omar", "Penny", "Quincy", "Rhea", "Sean", "Tess", "Uri", "Val",
    "Wade", "Yasmin", "Zack", "Amber", "Blake", "Cora", "Derek", "Erin", "Felix", "Gina",
    "Holden", "Ivy", "Jack", "Kylie", "Landon", "Molly", "Nate", "Opal", "Paul", "Rose",
    "Rylan", "Sienna", "Trent", "Una", "Vince", "Willa", "Xena", "Yosef", "Zara", "Asher",
    "Brooke", "Colin", "Diana", "Eliot", "Freya", "Glen", "Hope", "Jesse", "Kara", "Luke",
    "Mila", "Nash", "Olive", "Parker", "Reese", "Shay", "Toby", "Ursula", "Vance", "Wren",
    "Xavi", "Yvette", "Zion", "Alina", "Brady", "Casey", "Dana", "Eden", "Frank", "Gia",
    "Harry", "Isla", "Jude", "Kira", "Lila", "Miles", "Nina", "Owen", "Pia", "Quinn",
    "Rex", "Seth", "Tia", "Vera", "West", "Yanni", "Zeke", "Aidan", "Brielle", "Craig",
    "Delia", "Ezra", "Faye", "Gage", "Holly", "Ira", "Jillian", "Kian", "Leah", "Mason",
    "Nyla", "Orion", "Paula", "Rhys", "Sky", "Tyler", "Ulysses", "Vivian", "Wesley",
    "Ximena", "Yolanda", "Zander"
]
middles = [
    "Slayer", "Sniper", "Blade", "Knight", "Hunter", "Rogue", "Warden", "Nomad", "Ranger", "Scout",
    "Archer", "Berserker", "Duelist", "Lancer", "Gladiator", "Corsair", "Privateer", "Brigand", "Bandit", "Paladin",
    "Templar", "Crusader", "Warlock", "Sorcerer", "Wizard", "Enchanter", "Pyromancer", "Juggernaut", "Colossus", "Titan",
    "Behemoth", "Leviathan", "Kraken", "Wyrm", "Drake", "Serpent", "Centurion", "Marshal", "Captain", "Admiral",
    "Harbinger", "Herald", "Envoy", "Emissary", "Messenger", "Trickster", "Jester", "Harrier", "Huntsman", "Pathfinder",
    "Pioneer", "Outrider", "Rider", "Cavalier", "Dragoon", "Skirmisher", "Watcher", "Guardian", "Defender", "Protector",
    "Bulwark", "Shield", "Hammer", "Fist", "Fang", "Claw", "Maul", "Axe", "Spear", "Bow",
    "Arrow", "Bolt", "Blast", "Charge", "Rush", "Strike", "Smite", "Slash", "Pierce", "Sting",
    "Bite", "Roar", "Howl", "Growl", "Snarl", "Tracker", "Packleader", "Alpha", "Scoutmaster", "Watchman",
    "Lookout", "Sentry", "Seafarer", "Mariner", "Voyager", "Navigator", "Seeker", "Sentinel",
    "Vanguard", "Marauder", "Reaver", "Brawler", "Prowler", "Cutter", "Striker", "Marksman", "Champion", "Keeper",
    "Rune", "Glyph", "Sigil", "Spell", "Hex", "Curse", "Charm", "Blessing", "Altar", "Ritual",
    "Shrine", "Totem", "Relic", "Artifact", "Talisman", "Amulet", "Ring", "Crown", "Throne", "Banner",
    "Emblem", "Badge", "Insignia", "Mystic", "Oracle", "Beast", "Wolf", "Tiger", "Bear", "Lion",
    "Panther", "Jaguar", "Cobra", "Viper", "Wyvern", "Basilisk", "Hydra", "Manticore", "Golem", "Elemental",
    "Sprite", "Imp", "Demon", "Angel", "Djinn", "Nymph", "Dryad", "Specter", "Revenant", "Zombie",
    "Skeleton", "Ghoul", "Lich", "Kappa", "Griffin", "Phoenix", "Roc", "Sword", "Dagger", "Rapier",
    "Cutlass", "Sabre", "Mace", "Flail", "Pike", "Halberd", "Lance", "Crossbow", "Shot", "Thrust",
    "Jab", "Stab", "Chop", "Cleave", "Crush", "Bash", "Whirl", "Spin", "Sprint", "Leap",
    "Vault", "Dash", "Ambush", "Snipe", "Ambusher", "Cleric", "Priest", "Bard", "Minstrel", "Chronicler",
    "Archivist", "Scribe", "Cartographer", "Beacon", "Light", "Night", "Dawn", "Dusk", "Sun", "Moon", "Star", "Tide", "Wave", "Ocean", "Reef", "Sand", "Dust", "Earth", "Stone", "Rock",
    "Cliff", "Peak", "Vale", "Grove", "Thorn", "Ice", "Frost", "Flame", "Ember", "Blaze",
    "Ash", "Smoke", "Gale", "Wind", "Breeze", "Zephyr", "Thunder", "Lightning", "Rain", "Snow",
    "Hail", "Mist", "Fog", "Cloud", "Sky", "Solar", "Lunar", "Tempest", "Tundra", "Umber",
    "Void", "James", "Marie", "Lee", "Ann", "John", "Grace", "Ray", "Lou", "Paul", "Jane",
    "Mark", "Elle", "Jean", "Kai", "Beth", "Rey", "Rae", "Dean", "Jay", "May",
    "Dale", "Nell", "Clara", "Jude", "Mae", "Noel", "Tate", "Eve", "Quinn", "Ruth",
    "Lynn", "Beau", "Hope", "Gail", "Wade", "Blair", "Jace", "Skye", "Lane", "Drew",
    "Reed", "Cade", "Rex", "Vance", "Saul", "Eli", "Asa", "Faye", "Zane", "Lux",
    "Troy", "Shay", "Seth", "Hale", "Finn", "Joss", "Kirk", "Milo", "Owen", "Zeke",
    "Tess", "Paige", "Dean", "Glenn", "Holly", "Jill", "Kaye", "Lee", "Lark", "Neal",
    "Perry", "Rory", "Sage", "Tina", "Vera", "Wynn", "Zara", "Alex", "Blake", "Chase",
    "Dane", "Ellis", "Frank", "Gale", "Haze", "Ira", "Jack", "Kane", "Lane", "Mace",
    "Nate", "Olin", "Pax", "Rey", "Sean", "Tate", "Vail", "Wade", "Zion", "Abel",
    "Blaine", "Casey", "Drew", "Evan", "Flynn", "Grant", "Hayes", "Ivy", "Jude", "Kirk",
    "Luca", "Mila", "Noah", "Owen", "Paige", "Quinn", "Reese", "Shane", "Tara", "Vince",
    "Wren", "Xane", "Yara", "Zane", "Amos", "Beck", "Cruz", "Dale", "Eli", "Finn",
    "Gray", "Hale", "Ivan", "Joss", "Kade", "Lyle", "Mace", "Nico", "Omar", "Pax",
    "Reed", "Seth", "Troy", "Vale", "Wynn", "Zeke", "Asa", "Beau", "Cal", "Dane",
    "Ellis", "Gage", "Holt", "Jace", "Kane", "Leif", "Milo", "Nash", "Oren", "Pierce",
    "Rex", "Saul", "Tate", "Vail", "West", "Zion", "Ari", "Bryn", "Cade", "Drew",
    "Evan", "Fox", "Gray", "Hale", "Ira", "Jett", "Kirk", "Lane", "Milo", "Nash",
    "Odin", "Pax", "Reed", "Seth", "Tate", "Vail", "Wynn", "Zane"
]
suffixes = [
    "123", "x", "xx", "zzz", "guy", "gal", "pro", "player", "gamer", "hd", "jr", "sr",
    "boss", "king", "queen", "god", "noob", "legend", "champ", "killer", "sniper", "shot",
    "fire", "ice", "blade", "wolf", "hawk", "fox", "bear", "dragon", "shadow", "ghost",
    "ninja", "samurai", "viper", "cobra", "wolfy", "beast", "killer", "sniper", "strike",
    "rush", "shot", "dash", "speed", "flash", "boom", "blast", "storm", "stormy",
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "xoxo", "luv", "life", "fire", "ice", "light", "dark", "warrior", "fighter", "hunter",
    "rocket", "rocketman", "rocketgirl", "smash", "crush", "bang", "buzz", "pop", "snap",
    "zoom", "kingpin", "queenbee", "alpha", "omega", "max", "mini", "mega", "super", "ultra",
    "mega", "baby", "cool", "rad", "lit", "dope", "fresh", "wild", "mad", "crazy",
    "fast", "quick", "sharp", "slick", "smooth", "loud", "heavy", "bold", "brave", "keen",
    "dark", "light", "red", "blue", "green", "black", "white", "gold", "silver", "bronze",
    "steel", "iron", "chrome", "neon", "urban", "retro", "classic", "modern", "prime", "neo",
    "meta", "cyber", "tech", "ghost", "shadow", "phantom", "mystic", "legend", "champ",
    "ace", "rookie", "veteran", "master", "boss", "king", "queen", "duke", "baron", "sir",
    "lady", "captain", "commander", "chief", "spark", "pulse", "beat", "flow", "wave",
    "gear", "zone", "quest", "path", "trail", "step", "move", "spin", "roll", "crash",
    "blast", "kick", "jump", "fly", "run", "climb", "slide", "burst", "flash", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
    "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes",
    "Stewart", "Morris", "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
    "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
    "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez",
    "Powell", "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes",
    "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham",
    "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson",
    "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro", "Marshall", "Owens",
    "Harrison", "Fernandez", "Mcdonald", "Woods", "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen",
    "Freeman", "Webb", "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter",
    "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz", "Hunt", "Hicks",
    "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd", "Rose", "Stone", "Salazar", "Fox",
    "Warren", "Mills", "Meyer", "Rice", "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens",
    "Soto", "Weaver", "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins"
]

# ========ITEMS=========
swords = [
    {'Name': 'Reinforced Bark Sword', 'ATK': 1.7, 'SP': 1.1, 'Crit': 1.0, 'MAX DUR': 70, 'DUR': 70, 'Class': 'Weapon', 'Cost': 12000},
    {'Name': 'Rusty Iron Blade', 'ATK': 1.8, 'SP': 0.9, 'Crit': 1.1, 'MAX DUR': 80, 'DUR': 80, 'Class': 'Weapon', 'Cost': 13000},
    {'Name': 'Worn Bronze Saber', 'ATK': 1.6, 'SP': 1.0, 'Crit': 1.0, 'MAX DUR': 75, 'DUR': 75, 'Class': 'Weapon', 'Cost': 11000},
    {'Name': 'Steel Shortsword', 'ATK': 2.0, 'SP': 1.1, 'Crit': 1.2, 'MAX DUR': 120, 'DUR': 120, 'Class': 'Weapon', 'Cost': 15000},
    {'Name': 'Leather Cutter', 'ATK': 1.4, 'SP': 1.2, 'Crit': 1.0, 'MAX DUR': 50, 'DUR': 50, 'Class': 'Weapon', 'Cost': 10000},
    {'Name': 'Golden Dirk', 'ATK': 1.9, 'SP': 1.0, 'Crit': 1.3, 'MAX DUR': 110, 'DUR': 110, 'Class': 'Weapon', 'Cost': 14000},
    {'Name': 'Bark Cleaver', 'ATK': 1.3, 'SP': 1.1, 'Crit': 0.9, 'MAX DUR': 60, 'DUR': 60, 'Class': 'Weapon', 'Cost': 9000},
    {'Name': 'Iron Shortsword', 'ATK': 1.7, 'SP': 1.0, 'Crit': 1.0, 'MAX DUR': 85, 'DUR': 85, 'Class': 'Weapon', 'Cost': 12000},
    {'Name': 'Bronze Falchion', 'ATK': 1.8, 'SP': 1.0, 'Crit': 1.1, 'MAX DUR': 90, 'DUR': 90, 'Class': 'Weapon', 'Cost': 13000},
    {'Name': 'Steel Saber', 'ATK': 2.0, 'SP': 1.2, 'Crit': 1.3, 'MAX DUR': 130, 'DUR': 130, 'Class': 'Weapon', 'Cost': 15000},
    {'Name': 'Leather Blade', 'ATK': 1.5, 'SP': 1.3, 'Crit': 1.0, 'MAX DUR': 55, 'DUR': 55, 'Class': 'Weapon', 'Cost': 11000},
    {'Name': 'Golden Saber', 'ATK': 1.9, 'SP': 1.1, 'Crit': 1.4, 'MAX DUR': 125, 'DUR': 125, 'Class': 'Weapon', 'Cost': 14000},
    {'Name': 'Bark Sword', 'ATK': 1.4, 'SP': 1.0, 'Crit': 0.9, 'MAX DUR': 50, 'DUR': 50, 'Class': 'Weapon', 'Cost': 9000},
    {'Name': 'Iron Cutlass', 'ATK': 1.6, 'SP': 1.1, 'Crit': 1.0, 'MAX DUR': 80, 'DUR': 80, 'Class': 'Weapon', 'Cost': 12000},
    {'Name': 'Bronze Scimitar', 'ATK': 1.7, 'SP': 1.0, 'Crit': 1.1, 'MAX DUR': 85, 'DUR': 85, 'Class': 'Weapon', 'Cost': 13000},
    {'Name': 'Leather Sword', 'ATK': 1.3, 'SP': 1.1, 'Crit': 1.0, 'MAX DUR': 45, 'DUR': 45, 'Class': 'Weapon', 'Cost': 10000},
    {'Name': 'Golden Cutlass', 'ATK': 1.8, 'SP': 1.0, 'Crit': 1.2, 'MAX DUR': 115, 'DUR': 115, 'Class': 'Weapon', 'Cost': 14000},
    {'Name': 'Bark Dagger', 'ATK': 1.2, 'SP': 1.0, 'Crit': 0.8, 'MAX DUR': 40, 'DUR': 40, 'Class': 'Weapon', 'Cost': 9000},
    {'Name': 'Iron Saber', 'ATK': 1.7, 'SP': 1.1, 'Crit': 1.0, 'MAX DUR': 90, 'DUR': 90, 'Class': 'Weapon', 'Cost': 13000},
    {'Name': 'Bronze Cutter', 'ATK': 1.6, 'SP': 1.0, 'Crit': 1.0, 'MAX DUR': 70, 'DUR': 70, 'Class': 'Weapon', 'Cost': 10000},
    {'Name': 'Steel Cutter', 'ATK': 1.9, 'SP': 1.1, 'Crit': 1.1, 'MAX DUR': 140, 'DUR': 140, 'Class': 'Weapon', 'Cost': 1500},
    {'Name': 'Leather Falchion', 'ATK': 1.4, 'SP': 1.2, 'Crit': 1.0, 'MAX DUR': 50, 'DUR': 50, 'Class': 'Weapon', 'Cost': 10000},
    {'Name': 'Golden Falchion', 'ATK': 1.9, 'SP': 1.0, 'Crit': 1.3, 'MAX DUR': 120, 'DUR': 120, 'Class': 'Weapon', 'Cost': 15000},
    {'Name': 'Bark Shortsword', 'ATK': 1.3, 'SP': 1.0, 'Crit': 0.9, 'MAX DUR': 60, 'DUR': 60, 'Class': 'Weapon', 'Cost': 10000},
    {'Name': 'Iron Rapier', 'ATK': 1.8, 'SP': 1.2, 'Crit': 1.1, 'MAX DUR': 95, 'DUR': 95, 'Class': 'Weapon', 'Cost': 13000},
    {'Name': 'Bronze Rapier', 'ATK': 1.7, 'SP': 1.1, 'Crit': 1.0, 'MAX DUR': 85, 'DUR': 85, 'Class': 'Weapon', 'Cost': 12000},
    {'Name': 'Steel Dagger', 'ATK': 1.9, 'SP': 1.0, 'Crit': 1.2, 'MAX DUR': 130, 'DUR': 130, 'Class': 'Weapon', 'Cost': 14000},
    {'Name': 'Leather Rapier', 'ATK': 1.4, 'SP': 1.3, 'Crit': 1.0, 'MAX DUR': 55, 'DUR': 55, 'Class': 'Weapon', 'Cost': 11000},
    {'Name': 'Golden Rapier', 'ATK': 1.8, 'SP': 1.1, 'Crit': 1.4, 'MAX DUR': 125, 'DUR': 125, 'Class': 'Weapon', 'Cost': 13500}
] #average cost ~= 11000
elite_swords = [
    {'Name': 'Stormglass Longblade', 'ATK': 3.3, 'SP': 0.8, 'Crit': 2.4, 'MAX DUR': 210, 'DUR': 210, 'Class': 'Weapon', 'Cost': 20000},
    {'Name': 'Sunblessed Broadsword', 'ATK': 4.8, 'SP': 0.9, 'Crit': 2.4, 'MAX DUR': 320, 'DUR': 320, 'Class': 'Weapon', 'Cost': 30000},
    {'Name': 'Lunarfire Carver Longblade', 'ATK': 3.5, 'SP': 0.9, 'Crit': 2.5, 'MAX DUR': 230, 'DUR': 230, 'Class': 'Weapon', 'Cost': 23000},
    {'Name': 'Moonstone Obsidian Blade', 'ATK': 4.0, 'SP': 1.4, 'Crit': 1.5, 'MAX DUR': 270, 'DUR': 270, 'Class': 'Weapon', 'Cost': 25500},
    {'Name': 'Voidcrystal Sword', 'ATK': 3.4, 'SP': 1.9, 'Crit': 1.9, 'MAX DUR': 250, 'DUR': 250, 'Class': 'Weapon', 'Cost': 21000},
    {'Name': 'Glintstone Broadsword', 'ATK': 4.4, 'SP': 1.4, 'Crit': 1.9, 'MAX DUR': 290, 'DUR': 290, 'Class': 'Weapon', 'Cost': 27000},
    {'Name': 'Celestial Broadsword Phantom', 'ATK': 4.9, 'SP': 2.0, 'Crit': 2.5, 'MAX DUR': 340, 'DUR': 340, 'Class': 'Weapon', 'Cost': 34000},
    {'Name': 'Crimson Saber Iron', 'ATK': 3.4, 'SP': 1.6, 'Crit': 1.5, 'MAX DUR': 240, 'DUR': 240, 'Class': 'Weapon', 'Cost': 20500},
    {'Name': 'Shatterfang Damascus', 'ATK': 4.9, 'SP': 1.7, 'Crit': 2.3, 'MAX DUR': 320, 'DUR': 320, 'Class': 'Weapon', 'Cost': 33000},
    {'Name': 'Runebound Cutlass', 'ATK': 3.8, 'SP': 0.9, 'Crit': 2.3, 'MAX DUR': 260, 'DUR': 260, 'Class': 'Weapon', 'Cost': 23000},
    {'Name': 'Lunarfire Etherium Phantom', 'ATK': 4.8, 'SP': 1.7, 'Crit': 2.1, 'MAX DUR': 310, 'DUR': 310, 'Class': 'Weapon', 'Cost': 31000},
    {'Name': 'Ghoststeel Damascus', 'ATK': 4.1, 'SP': 1.0, 'Crit': 2.4, 'MAX DUR': 300, 'DUR': 300, 'Class': 'Weapon', 'Cost': 30000},
    {'Name': 'Blackglass Blade', 'ATK': 4.8, 'SP': 1.9, 'Crit': 2.3, 'MAX DUR': 335, 'DUR': 335, 'Class': 'Weapon', 'Cost': 33500},
    {'Name': 'Celestial Cutlass', 'ATK': 4.0, 'SP': 1.4, 'Crit': 2.3, 'MAX DUR': 300, 'DUR': 300, 'Class': 'Weapon', 'Cost': 30000},
    {'Name': 'Blackglass Saber', 'ATK': 4.8, 'SP': 0.8, 'Crit': 1.7, 'MAX DUR': 320, 'DUR': 320, 'Class': 'Weapon', 'Cost': 33000},
    {'Name': 'Crimson Iron', 'ATK': 4.1, 'SP': 0.9, 'Crit': 1.7, 'MAX DUR': 280, 'DUR': 280, 'Class': 'Weapon', 'Cost': 28000},
    {'Name': 'Glintstone Steel', 'ATK': 4.9, 'SP': 1.7, 'Crit': 1.7, 'MAX DUR': 360, 'DUR': 360, 'Class': 'Weapon', 'Cost': 36000},
    {'Name': 'Celestial Iron', 'ATK': 3.1, 'SP': 1.3, 'Crit': 2.3, 'MAX DUR': 210, 'DUR': 210, 'Class': 'Weapon', 'Cost': 20000},
    {'Name': 'Bloodiron Saber', 'ATK': 4.2, 'SP': 0.8, 'Crit': 1.8, 'MAX DUR': 320, 'DUR': 320, 'Class': 'Weapon', 'Cost': 32000},
    {'Name': 'Shatterfang Damascus', 'ATK': 4.0, 'SP': 0.9, 'Crit': 1.5, 'MAX DUR': 270, 'DUR': 270, 'Class': 'Weapon', 'Cost': 27000},
    {'Name': 'Blackglass Sharpsword', 'ATK': 3.1, 'SP': 1.4, 'Crit': 1.8, 'MAX DUR': 210, 'DUR': 210, 'Class': 'Weapon', 'Cost': 20000},
    {'Name': 'Ashenroot Broadsword', 'ATK': 4.4, 'SP': 1.4, 'Crit': 2.1, 'MAX DUR': 320, 'DUR': 320, 'Class': 'Weapon', 'Cost': 32000},
    {'Name': 'Skyshard Iron Sword', 'ATK': 3.9, 'SP': 2.0, 'Crit': 1.8, 'MAX DUR': 300, 'DUR': 300, 'Class': 'Weapon', 'Cost': 30000},
    {'Name': 'Shatterfang Phantom Steel', 'ATK': 3.4, 'SP': 1.3, 'Crit': 1.8, 'MAX DUR': 270, 'DUR': 270, 'Class': 'Weapon', 'Cost': 27000},
    {'Name': 'Silveredge Phantom', 'ATK': 4.7, 'SP': 1.6, 'Crit': 1.8, 'MAX DUR': 350, 'DUR': 350, 'Class': 'Weapon', 'Cost': 35000},
    {'Name': 'Dragonbone Saber', 'ATK': 4.4, 'SP': 1.1, 'Crit': 2.3, 'MAX DUR': 325, 'DUR': 325, 'Class': 'Weapon', 'Cost': 32500},
    {'Name': 'Sunblessed Obsidian Sharpsword', 'ATK': 4.8, 'SP': 1.8, 'Crit': 2.3, 'MAX DUR': 360, 'DUR': 360, 'Class': 'Weapon', 'Cost': 36000},
    {'Name': 'Blackglass Sharpsword', 'ATK': 5.0, 'SP': 1.7, 'Crit': 2.1, 'MAX DUR': 420, 'DUR': 420, 'Class': 'Weapon', 'Cost': 42000},
    {'Name': 'Sunblessed Etherium Broadsword', 'ATK': 3.7, 'SP': 1.5, 'Crit': 2.0, 'MAX DUR': 290, 'DUR': 290, 'Class': 'Weapon', 'Cost': 29000},
    {'Name': 'Starforged Obsidian Carver', 'ATK': 3.3, 'SP': 1.5, 'Crit': 1.7, 'MAX DUR': 240, 'DUR': 240, 'Class': 'Weapon', 'Cost': 24000},
    {'Name': 'Whirlwind Saber', 'ATK': 4.2, 'SP': 1.4, 'Crit': 2.2, 'MAX DUR': 320, 'DUR': 320, 'Class': 'Weapon', 'Cost': 32000},
    {'Name': 'Dragonbone Steel Etherium', 'ATK': 4.8, 'SP': 1.2, 'Crit': 2.5, 'MAX DUR': 365, 'DUR': 365, 'Class': 'Weapon', 'Cost': 36500},
    {'Name': 'Frostshard Phantom', 'ATK': 4.8, 'SP': 1.6, 'Crit': 2.0, 'MAX DUR': 355, 'DUR': 355, 'Class': 'Weapon', 'Cost': 35500},
    {'Name': 'Emberglow Damascus Phantom', 'ATK': 3.8, 'SP': 1.0, 'Crit': 2.1, 'MAX DUR': 280, 'DUR': 280, 'Class': 'Weapon', 'Cost': 28000},
    {'Name': 'Emberglow Broadsword', 'ATK': 4.8, 'SP': 1.2, 'Crit': 2.2, 'MAX DUR': 360, 'DUR': 360, 'Class': 'Weapon', 'Cost': 36000},
    {'Name': 'Dragonbone Sword', 'ATK': 3.7, 'SP': 0.9, 'Crit': 2.0, 'MAX DUR': 265, 'DUR': 265, 'Class': 'Weapon', 'Cost': 26500},
    {'Name': 'Sunblessed Steel Saber', 'ATK': 3.0, 'SP': 1.7, 'Crit': 1.7, 'MAX DUR': 220, 'DUR': 220, 'Class': 'Weapon', 'Cost': 22000},
    {'Name': 'Crimson Blade Obsidian', 'ATK': 3.1, 'SP': 1.9, 'Crit': 1.7, 'MAX DUR': 230, 'DUR': 230, 'Class': 'Weapon', 'Cost': 23000},
    {'Name': 'Sunblessed Sharpsword', 'ATK': 3.4, 'SP': 1.8, 'Crit': 1.8, 'MAX DUR': 250, 'DUR': 250, 'Class': 'Weapon', 'Cost': 25000},
    {'Name': 'Sunblessed Damascus', 'ATK': 3.8, 'SP': 1.0, 'Crit': 1.9, 'MAX DUR': 290, 'DUR': 290, 'Class': 'Weapon', 'Cost': 29000},
    {'Name': 'Starforged Damascus', 'ATK': 4.8, 'SP': 1.7, 'Crit': 1.7, 'MAX DUR': 360, 'DUR': 360, 'Class': 'Weapon', 'Cost': 36000},
    {'Name': 'Glintstone Broadsword Damascus', 'ATK': 3.1, 'SP': 1.2, 'Crit': 2.3, 'MAX DUR': 235, 'DUR': 235, 'Class': 'Weapon', 'Cost': 23500},
    {'Name': 'Celestial Broadsword Damascus', 'ATK': 3.8, 'SP': 1.8, 'Crit': 2.2, 'MAX DUR': 300, 'DUR': 300, 'Class': 'Weapon', 'Cost': 30000},
    {'Name': 'Glintstone Saber Cutlass', 'ATK': 3.4, 'SP': 1.2, 'Crit': 2.0, 'MAX DUR': 260, 'DUR': 260, 'Class': 'Weapon', 'Cost': 26000},
    {'Name': 'Dragonbone Obsidian', 'ATK': 4.8, 'SP': 1.4, 'Crit': 1.5, 'MAX DUR': 370, 'DUR': 370, 'Class': 'Weapon', 'Cost': 37000},
    {'Name': 'Netherite Damascus', 'ATK': 4.7, 'SP': 0.9, 'Crit': 2.4, 'MAX DUR': 355, 'DUR': 355, 'Class': 'Weapon', 'Cost': 35500},
    {'Name': 'Crimson Cutlass Phantom', 'ATK': 4.3, 'SP': 1.1, 'Crit': 2.1, 'MAX DUR': 220, 'DUR': 220, 'Class': 'Weapon', 'Cost': 3200},
    {'Name': 'Ghoststeel Broadsword Cleaver', 'ATK': 4.7, 'SP': 1.5, 'Crit': 1.9, 'MAX DUR': 360, 'DUR': 360, 'Class': 'Weapon', 'Cost': 36000},
    {'Name': 'Shatterfang Iron', 'ATK': 4.5, 'SP': 1.5, 'Crit': 2.2, 'MAX DUR': 330, 'DUR': 330, 'Class': 'Weapon', 'Cost': 33000},
    {'Name': 'Mythsteel Carver', 'ATK': 4.2, 'SP': 2.0, 'Crit': 2.3, 'MAX DUR': 315, 'DUR': 315, 'Class': 'Weapon', 'Cost': 31500}
] #average cost ~= 30000
helmets = [
    {'Name': 'Ironhelm', 'DEF': 2.9, 'SP': 1.0, 'MAX DUR': 590, 'DUR': 590, 'Class': 'Helmet', 'Cost': 63000},
    {'Name': 'Steelguard Soulveil', 'DEF': 3.0, 'SP': 0.9, 'MAX DUR': 620, 'DUR': 620, 'Class': 'Helmet', 'Cost': 63000},
    {'Name': 'Dragoncrest Helm', 'DEF': 2.8, 'SP': 1.0, 'MAX DUR': 580, 'DUR': 580, 'Class': 'Helmet', 'Cost': 62000},
    {'Name': 'Stormhelm Soulveil', 'DEF': 2.7, 'SP': 1.0, 'MAX DUR': 550, 'DUR': 550, 'Class': 'Helmet', 'Cost': 61000},
    {'Name': 'Bloodguard Helm', 'DEF': 2.5, 'SP': 1.0, 'MAX DUR': 520, 'DUR': 520, 'Class': 'Helmet', 'Cost': 59000},
    {'Name': 'Skullforge Soulveil', 'DEF': 3.0, 'SP': 0.8, 'MAX DUR': 610, 'DUR': 610, 'Class': 'Helmet', 'Cost': 62000},
    {'Name': 'Nighthelm', 'DEF': 2.6, 'SP': 1.0, 'MAX DUR': 540, 'DUR': 540, 'Class': 'Helmet', 'Cost': 60000},
    {'Name': 'Frostguard Soulveil', 'DEF': 2.9, 'SP': 0.9, 'MAX DUR': 590, 'DUR': 590, 'Class': 'Helmet', 'Cost': 62000},
    {'Name': 'Thunderhelm', 'DEF': 3.0, 'SP': 1.0, 'MAX DUR': 630, 'DUR': 630, 'Class': 'Helmet', 'Cost': 64000},
    {'Name': 'Shadowguard Soulveil', 'DEF': 2.4, 'SP': 1.0, 'MAX DUR': 490, 'DUR': 490, 'Class': 'Helmet', 'Cost': 58000},
    {'Name': 'Firecrest Helm', 'DEF': 2.7, 'SP': 1.0, 'MAX DUR': 560, 'DUR': 560, 'Class': 'Helmet', 'Cost': 61000},
    {'Name': 'Crystalhelm Soulveil', 'DEF': 2.9, 'SP': 1.0, 'MAX DUR': 600, 'DUR': 600, 'Class': 'Helmet', 'Cost': 63000},
    {'Name': 'Boneguard Helm', 'DEF': 2.8, 'SP': 1.0, 'MAX DUR': 580, 'DUR': 580, 'Class': 'Helmet', 'Cost': 62000},
    {'Name': 'Darkhelm Soulveil', 'DEF': 2.3, 'SP': 1.0, 'MAX DUR': 470, 'DUR': 470, 'Class': 'Helmet', 'Cost': 57000},
    {'Name': 'Voidguard Helm', 'DEF': 2.5, 'SP': 0.7, 'MAX DUR': 450, 'DUR': 450, 'Class': 'Helmet', 'Cost': 56000},
    {'Name': 'Stonecrest Soulveil', 'DEF': 3.0, 'SP': 0.6, 'MAX DUR': 580, 'DUR': 580, 'Class': 'Helmet', 'Cost': 60000},
    {'Name': 'Flamehelm', 'DEF': 2.8, 'SP': 1.0, 'MAX DUR': 580, 'DUR': 580, 'Class': 'Helmet', 'Cost': 62000},
    {'Name': 'Ghostguard Soulveil', 'DEF': 2.9, 'SP': 0.9, 'MAX DUR': 590, 'DUR': 590, 'Class': 'Helmet', 'Cost': 62000},
    {'Name': 'Stormguard Helm', 'DEF': 2.7, 'SP': 1.0, 'MAX DUR': 560, 'DUR': 560, 'Class': 'Helmet', 'Cost': 61000},
    {'Name': 'Embercrest Soulveil', 'DEF': 2.6, 'SP': 1.0, 'MAX DUR': 540, 'DUR': 540, 'Class': 'Helmet', 'Cost': 60000},
    {'Name': 'Ironveil Helm', 'DEF': 3.0, 'SP': 1.0, 'MAX DUR': 640, 'DUR': 640, 'Class': 'Helmet', 'Cost': 64000},
    {'Name': 'Frosthelm Soulveil', 'DEF': 2.4, 'SP': 0.8, 'MAX DUR': 480, 'DUR': 480, 'Class': 'Helmet', 'Cost': 56000},
    {'Name': 'Dreadguard Helm', 'DEF': 2.5, 'SP': 1.0, 'MAX DUR': 520, 'DUR': 520, 'Class': 'Helmet', 'Cost': 59000},
    {'Name': 'Phantomhelm Soulveil', 'DEF': 2.3, 'SP': 0.9, 'MAX DUR': 470, 'DUR': 470, 'Class': 'Helmet', 'Cost': 56000},
    {'Name': 'Runecrest Helm', 'DEF': 2.7, 'SP': 1.0, 'MAX DUR': 550, 'DUR': 550, 'Class': 'Helmet', 'Cost': 61000},
    {'Name': 'Steelveil Soulveil', 'DEF': 2.8, 'SP': 0.7, 'MAX DUR': 530, 'DUR': 530, 'Class': 'Helmet', 'Cost': 59000},
    {'Name': 'Ashenhelm', 'DEF': 2.6, 'SP': 1.0, 'MAX DUR': 540, 'DUR': 540, 'Class': 'Helmet', 'Cost': 60000},
    {'Name': 'Spiritguard Soulveil', 'DEF': 2.9, 'SP': 0.9, 'MAX DUR': 590, 'DUR': 590, 'Class': 'Helmet', 'Cost': 62000},
    {'Name': 'Grimcrest Helm', 'DEF': 2.7, 'SP': 1.0, 'MAX DUR': 560, 'DUR': 560, 'Class': 'Helmet', 'Cost': 61000},
    {'Name': 'Shadowhelm Soulveil', 'DEF': 2.8, 'SP': 0.8, 'MAX DUR': 580, 'DUR': 580, 'Class': 'Helmet', 'Cost': 60000}
] #average cost ~= 60000 
chestplates = [
    {'Name': 'Voidcrystal Chestplate', 'DEF': 4.1, 'SP': 1.1, 'MAX DUR': 950, 'DUR': 950, 'Class': 'Chestplate', 'Cost': 60000},
    {'Name': 'Mythristeel Harness', 'DEF': 4.5, 'SP': 1.2, 'MAX DUR': 1020, 'DUR': 1020, 'Class': 'Chestplate', 'Cost': 66000},
    {'Name': 'Phantom Vest', 'DEF': 4.7, 'SP': 1.3, 'MAX DUR': 1080, 'DUR': 1080, 'Class': 'Chestplate', 'Cost': 68000},
    {'Name': 'Gilded Dragonplate', 'DEF': 5.2, 'SP': 1.4, 'MAX DUR': 1180, 'DUR': 1180, 'Class': 'Chestplate', 'Cost': 74000},
    {'Name': 'Nebulaweave Carapace', 'DEF': 4.9, 'SP': 1.5, 'MAX DUR': 1110, 'DUR': 1110, 'Class': 'Chestplate', 'Cost': 72000},
    {'Name': 'Reinforced Barkmail', 'DEF': 5.1, 'SP': 1.6, 'MAX DUR': 1150, 'DUR': 1150, 'Class': 'Chestplate', 'Cost': 75000},
    {'Name': 'Obsidian Coreplate', 'DEF': 5.5, 'SP': 1.7, 'MAX DUR': 1200, 'DUR': 1200, 'Class': 'Chestplate', 'Cost': 80000},
    {'Name': 'Celestial Mantle', 'DEF': 4.3, 'SP': 1.8, 'MAX DUR': 980, 'DUR': 980, 'Class': 'Chestplate', 'Cost': 69000},
    {'Name': 'Boneglass Vestment', 'DEF': 4.6, 'SP': 1.9, 'MAX DUR': 1050, 'DUR': 1050, 'Class': 'Chestplate', 'Cost': 73000},
    {'Name': 'Starlight Laminar', 'DEF': 5.3, 'SP': 1.4, 'MAX DUR': 1170, 'DUR': 1170, 'Class': 'Chestplate', 'Cost': 75000},
    {'Name': 'Ashen Emberplate', 'DEF': 5.0, 'SP': 1.1, 'MAX DUR': 1120, 'DUR': 1120, 'Class': 'Chestplate', 'Cost': 69000},
    {'Name': 'Runeforged Shell', 'DEF': 4.8, 'SP': 1.2, 'MAX DUR': 1080, 'DUR': 1080, 'Class': 'Chestplate', 'Cost': 68000},
    {'Name': 'Frosthide Chestwrap', 'DEF': 5.4, 'SP': 1.3, 'MAX DUR': 1190, 'DUR': 1190, 'Class': 'Chestplate', 'Cost': 75000},
    {'Name': 'Nightmare Husk', 'DEF': 4.4, 'SP': 1.5, 'MAX DUR': 990, 'DUR': 990, 'Class': 'Chestplate', 'Cost': 67000},
    {'Name': 'Thunderbound Vest', 'DEF': 5.7, 'SP': 1.6, 'MAX DUR': 1200, 'DUR': 1200, 'Class': 'Chestplate', 'Cost': 81000},
    {'Name': 'Ebonstone Plate', 'DEF': 4.2, 'SP': 1.7, 'MAX DUR': 970, 'DUR': 970, 'Class': 'Chestplate', 'Cost': 67000},
    {'Name': 'Scorchscale Mail', 'DEF': 5.6, 'SP': 1.8, 'MAX DUR': 1190, 'DUR': 1190, 'Class': 'Chestplate', 'Cost': 82000},
    {'Name': 'Ironbark Breastguard', 'DEF': 4.9, 'SP': 1.9, 'MAX DUR': 1130, 'DUR': 1130, 'Class': 'Chestplate', 'Cost': 76000},
    {'Name': 'Moonshroud Corslet', 'DEF': 5.8, 'SP': 1.3, 'MAX DUR': 1200, 'DUR': 1200, 'Class': 'Chestplate', 'Cost': 81000},
    {'Name': 'Starforged Plating', 'DEF': 4.7, 'SP': 1.4, 'MAX DUR': 1070, 'DUR': 1070, 'Class': 'Chestplate', 'Cost': 71000}
] #average cost ~= 72000
leggings = [
    {"Name": "Shadowfiber Leggings", "DEF": 3.2, "SP": 1.5, "MAX DUR": 900, "DUR": 900, "Class": "Leggings", "Cost": 63000},
    {"Name": "Ironbark Greaves", "DEF": 3.4, "SP": 1.0, "MAX DUR": 920, "DUR": 920, "Class": "Leggings", "Cost": 60000},
    {"Name": "Silkweave Leggings", "DEF": 2.9, "SP": 1.4, "MAX DUR": 750, "DUR": 750, "Class": "Leggings", "Cost": 59000},
    {"Name": "Glacialweave Greaves", "DEF": 2.8, "SP": 1.6, "MAX DUR": 740, "DUR": 740, "Class": "Leggings", "Cost": 60000},
    {"Name": "Moonshadow Leggings", "DEF": 3.0, "SP": 1.3, "MAX DUR": 780, "DUR": 780, "Class": "Leggings", "Cost": 59000},
    {"Name": "Stormsteel Greaves", "DEF": 3.5, "SP": 1.3, "MAX DUR": 930, "DUR": 930, "Class": "Leggings", "Cost": 64000},
    {"Name": "Starwoven Leggings", "DEF": 3.5, "SP": 1.6, "MAX DUR": 950, "DUR": 950, "Class": "Leggings", "Cost": 67000},
    {"Name": "Duskveil Greaves", "DEF": 2.9, "SP": 1.1, "MAX DUR": 730, "DUR": 730, "Class": "Leggings", "Cost": 56000},
    {"Name": "Duskmire Leggings", "DEF": 3.1, "SP": 1.2, "MAX DUR": 800, "DUR": 800, "Class": "Leggings", "Cost": 59000},
    {"Name": "Emberleaf Greaves", "DEF": 3.0, "SP": 1.0, "MAX DUR": 780, "DUR": 780, "Class": "Leggings", "Cost": 56000},
    {"Name": "Frostglow Leggings", "DEF": 2.8, "SP": 1.1, "MAX DUR": 720, "DUR": 720, "Class": "Leggings", "Cost": 55000},
    {"Name": "Crystalmesh Greaves", "DEF": 3.1, "SP": 1.4, "MAX DUR": 810, "DUR": 810, "Class": "Leggings", "Cost": 61000},
    {"Name": "Emberthread Leggings", "DEF": 3.3, "SP": 1.0, "MAX DUR": 870, "DUR": 870, "Class": "Leggings", "Cost": 59000},
    {"Name": "Shadowsteel Greaves", "DEF": 3.5, "SP": 1.2, "MAX DUR": 920, "DUR": 920, "Class": "Leggings", "Cost": 63000},
    {"Name": "Veilshadow Leggings", "DEF": 3.4, "SP": 1.6, "MAX DUR": 940, "DUR": 940, "Class": "Leggings", "Cost": 66000},
    {"Name": "Stormshard Greaves", "DEF": 3.2, "SP": 1.3, "MAX DUR": 880, "DUR": 880, "Class": "Leggings", "Cost": 61000},
    {"Name": "Nightbloom Leggings", "DEF": 2.7, "SP": 1.3, "MAX DUR": 700, "DUR": 700, "Class": "Leggings", "Cost": 56000},
    {"Name": "Soulplate Greaves", "DEF": 3.3, "SP": 1.5, "MAX DUR": 910, "DUR": 910, "Class": "Leggings", "Cost": 64000},
    {"Name": "Stormveil Leggings", "DEF": 3.0, "SP": 1.5, "MAX DUR": 820, "DUR": 820, "Class": "Leggings", "Cost": 61000},
    {"Name": "Frostbane Greaves", "DEF": 3.4, "SP": 1.1, "MAX DUR": 900, "DUR": 900, "Class": "Leggings", "Cost": 61000}
] #average cost ~= 60000 
boots = [ 
    {"Name": "Ashleather Boots", "DEF": 1.8, "SP": 1.7, "MAX DUR": 750, "DUR": 750, "Class": "Boots", "Cost": 51000},
    {"Name": "Moltenhide Sabatons", "DEF": 2.0, "SP": 1.3, "MAX DUR": 780, "DUR": 780, "Class": "Boots", "Cost": 49000},
    {"Name": "Starstitch Treads", "DEF": 1.5, "SP": 2.0, "MAX DUR": 600, "DUR": 600, "Class": "Boots", "Cost": 51000},
    {"Name": "Voidflame Striders", "DEF": 1.9, "SP": 1.4, "MAX DUR": 740, "DUR": 740, "Class": "Boots", "Cost": 49000},
    {"Name": "Dusksilk Walkers", "DEF": 1.6, "SP": 1.9, "MAX DUR": 650, "DUR": 650, "Class": "Boots", "Cost": 51000},
    {"Name": "Thundersoul Stormsteps", "DEF": 2.0, "SP": 1.1, "MAX DUR": 780, "DUR": 780, "Class": "Boots", "Cost": 47000},
    {"Name": "Echowind Voidboots", "DEF": 1.7, "SP": 1.6, "MAX DUR": 700, "DUR": 700, "Class": "Boots", "Cost": 49000},
    {"Name": "Glimmerscale Ashwalkers", "DEF": 1.5, "SP": 1.8, "MAX DUR": 620, "DUR": 620, "Class": "Boots", "Cost": 49000},
    {"Name": "Twilighthide Frostbound", "DEF": 2.0, "SP": 1.2, "MAX DUR": 780, "DUR": 780, "Class": "Boots", "Cost": 49000},
    {"Name": "Frostlace Soulstriders", "DEF": 1.9, "SP": 1.5, "MAX DUR": 750, "DUR": 750, "Class": "Boots", "Cost": 51000},
    {"Name": "Blightiron Boots", "DEF": 1.6, "SP": 1.7, "MAX DUR": 670, "DUR": 670, "Class": "Boots", "Cost": 50000},
    {"Name": "Runetwine Runebinders", "DEF": 2.0, "SP": 1.0, "MAX DUR": 780, "DUR": 780, "Class": "Boots", "Cost": 47000},
    {"Name": "Brightmist Starboots", "DEF": 1.8, "SP": 1.9, "MAX DUR": 740, "DUR": 740, "Class": "Boots", "Cost": 55000},
    {"Name": "Shadowfiber Walkers", "DEF": 1.4, "SP": 2.0, "MAX DUR": 600, "DUR": 600, "Class": "Boots", "Cost": 52000},
    {"Name": "Nightcore Sabatons", "DEF": 1.7, "SP": 1.6, "MAX DUR": 700, "DUR": 700, "Class": "Boots", "Cost": 51000},
    {"Name": "Emberlace Skywalkers", "DEF": 2.0, "SP": 1.3, "MAX DUR": 780, "DUR": 780, "Class": "Boots", "Cost": 51000},
    {"Name": "Netherstep Boots", "DEF": 1.6, "SP": 1.8, "MAX DUR": 680, "DUR": 680, "Class": "Boots", "Cost": 52000},
    {"Name": "Ironshade Warpboots", "DEF": 1.9, "SP": 1.2, "MAX DUR": 750, "DUR": 750, "Class": "Boots", "Cost": 49000},
    {"Name": "Crystalhide Striders", "DEF": 2.0, "SP": 1.1, "MAX DUR": 780, "DUR": 780, "Class": "Boots", "Cost": 49000},
    {"Name": "Duskrune Voidboots", "DEF": 1.5, "SP": 2.0, "MAX DUR": 620, "DUR": 620, "Class": "Boots", "Cost": 53000},
    {"Name": "Thornwoven Treads", "DEF": 1.8, "SP": 1.6, "MAX DUR": 720, "DUR": 720, "Class": "Boots", "Cost": 52000}
] #average cost ~= 50000 
potions = [
    {"Name": "Potion of Healing", "Tier": 1, "Effect": 500, "Cost": 250, "Class": "Potion of Healing"},
    {"Name": "Potion of Strength", "Tier": 1, "Effect": 2, "Cost": 500, "Class": "Potion of Strength"},
    {"Name": "Potion of Defense", "Tier": 1, "Effect": 2, "Cost": 500, "Class": "Potion of Defense"},
]

#========MONSTERS=========
soldiers = {
    "Goblin Recruit": {
        "HP": 2000, 
        "ATK": 200, 
        "DEF": 150, 
        "Crit": 10,
        "SP": 20,
        "EXP": 20, 
        "Weapon": {"Name": "Spiked Club", "ATK": 2, "SP": 1.4, "Crit": 1.5, "MAX DUR": 850, "DUR": 850, "Class": "Weapon"},
        "Left Hand": {"Name": "Reinforced Bark Shield", "DEF": 1.5, "SP": 0.8, "MAX DUR": 900, "DUR": 900, "Class": "Shield"},
        "Helmet": {},
        "Chestplate": {"Name": "Bark Chestplate", "DEF": 1.8, "SP": 1, "MAX DUR": 950, "DUR": 950, "Class": "Chestplate"},
        "Leggings": {},
        "Boots": {"Name": "Bark Boots", "DEF": 1.2, "SP": 1.1, "MAX DUR": 750, "DUR": 750, "Class": "Boots"}
    },
    "Goblin Lieutenant": {
        "HP": 2600, 
        "ATK": 300, 
        "DEF": 150,
        "Crit": 15,
        "SP": 20,
        "EXP": 30,
        "Weapon": {"Name": "Jagged Iron Sword", "ATK": 2.4, "SP": 1, "Crit": 1.7, "MAX DUR": 1200, "DUR": 1200, "Class": "Weapon"},
        "Left Hand": {"Name": "Rusty Steel Shield", "DEF": 1.3, "SP": 0.8, "MAX DUR": 1000, "DUR": 1000, "Class": "Shield"},
        "Helmet": {"Name": "Mythril Helmet", "DEF": 1.5, "SP": 1, "MAX DUR": 1100, "DUR": 1100, "Class": "Helmet"},
        "Chestplate": {"Name": "Scrapmail Vest", "DEF": 2.2, "SP": 0.9, "MAX DUR": 1250, "DUR": 1250, "Class": "Chestplate"},
        "Leggings": {"Name": "Reinforced Leather Greaves", "DEF": 1.5, "SP": 1.4, "MAX DUR": 950, "DUR": 950, "Class": "Boots"},
        "Boots": {}
    },
    "Goblin Archer": {
        "HP": 1900, 
        "ATK": 400, 
        "DEF": 100, 
        "Crit": 10,
        "SP": 50,
        "EXP": 20,
        "Weapon": {"Name": "Short Bow", "ATK": 2, "SP": 2, "Crit": 1.5, "MAX DUR": 700, "DUR": 700, "Class": "Weapon"},
        "Left Hand": {"Name": "Chainmail Shield", "DEF": 1.2, "SP": 0.9, "MAX DUR": 850, "DUR": 850, "Class": "Shield"},
        "Helmet": {"Name": "Leather Helmet", "DEF": 1.3, "SP": 1, "MAX DUR": 800, "DUR": 800, "Class": "Helmet"},
        "Chestplate": {"Name": "Leather Chestplate", "DEF": 1.5, "SP": 0.9, "MAX DUR": 900, "DUR": 900, "Class": "Chestplate"},
        "Leggings": {},
        "Boots": {"Name": "Leather Boots", "DEF": 1.2, "SP": 1.2, "MAX DUR": 700, "DUR": 700, "Class": "Boots"}
    },
    "Troll Grunt": {
        "HP": 2100,
        "ATK": 300,
        "DEF": 200,
        "Crit": 20,
        "SP": 30,
        "EXP": 20,
        "Weapon": {"Name": "Hardened Oak Club", "ATK": 1.5, "SP": 1, "Crit": 1.2, "MAX DUR": 1300, "DUR": 1300, "Class": "Weapon"},
        "Left Hand": {"Name": "Reinforced Leather Shield", "DEF": 1.5, "SP": 1, "MAX DUR": 1150, "DUR": 1150, "Class": "Shield"},
        "Helmet": {},
        "Chestplate": {},
        "Leggings": {},
        "Boots": {}
    }
}
monsters = {    
    "Snow Shaman": {
        "HP": 2600,
        "ATK": 300,
        "DEF": 200,
        "Crit": 20,
        "SP": 25,
        "EXP": 40,
        "Weapon": {"Name": "Permafrost Icereed Staff", "ATK": 2, "SP": 1, "Crit": 2, "Effect": "Freeze", "Chance": 10},
        "Left Hand": {"Name": "Frostbound Talisman", "Effect": "Dodge", "Chance": 30, "Class": "Rune"},
        "Drops": [
            {"Name": "Frostbound Talisman", "Effect": "Dodge", "Chance": 30, "Class": "Rune"},
            {"Name": "Scroll of Endless Winter", "Class": "Scroll"},
        ]
    },
    "Flame Shaman": {
        "HP": 2600,
        "ATK": 300,
        "DEF": 200,
        "Crit": 20,
        "SP": 25,
        "EXP": 40,
        "Weapon": {"Name": "Hellfire Blazebark Staff", "ATK": 3, "SP": 1.5, "Crit": 0.5, "Effect": "Fire", "Chance": 10},
        "Left Hand": {"Name": "Ashenroot Talisman", "Effect": "Dodge", "Chance": 30, "Class": "Rune"},
        "Drops": [
            {"Name": "Ashenroot Talisman", "Effect": "Dodge", "Chance": 30, "Class": "Rune"},
            {"Name": "Scroll of Infernal Blaze", "Class": "Scroll"}
        ]
    }
}
boss = {
    "Troll Elite Commander": {
        "HP": 4800,
        "ATK": 72,
        "DEF": 28,
        "Crit": 10,
        "SP": 14,
        "EXP": 450,
        "Prisms": 1,
        "Weapon": {"Name": "Starforged Etherium Double-Edged Sharpsword", "ATK": 3.6, "SP": 2, "Crit": 3, "MAX DUR": 5000, "DUR": 5000, "Class": "Weapon"},
        "Left Hand": {"Name": "Nethersteel Jagged Shield", "DEF": 2.2, "SP": 3, "MAX DUR": 5500, "DUR": 5500, "Class": "Shield"},
        "Helmet": {"Name": "Stormforged Phantom Iron Helmet", "DEF": 2.8, "SP": 1, "MAX DUR": 4800, "DUR": 4800, "Class": "Helmet"},
        "Chestplate": {"Name": "Voidcrystal Chestplate", "DEF": 3.5, "SP": 1, "MAX DUR": 6000, "DUR": 6000, "Class": "Chestplate"},
        "Leggings": {"Name": "Bloodiron Leggings", "DEF": 2.5, "SP": 2, "MAX DUR": 5200, "DUR": 5200, "Class": "Boots"},
        "Boots": {"Name": "Abyssal Gold Boots", "DEF": 2.0, "SP": 3, "MAX DUR": 5100, "DUR": 5100, "Class": "Boots"}
    },
    "Goblin Sergeant": {
        "HP": 6200,
        "ATK": 78,
        "DEF": 32,
        "Crit": 12,
        "SP": 15,
        "EXP": 700,
        "Prisms": 2,
        "Weapon": {"Name": "Great Damascus Sword", "ATK": 4.2, "SP": 1, "Crit": 3, "MAX DUR": 4600, "DUR": 4600, "Class": "Weapon"},
        "Left Hand": {"Name": "Crusader Round Shield", "DEF": 2.0, "SP": 1.25, "MAX DUR": 4300, "DUR": 4300, "Class": "Shield"},
        "Helmet": {"Name": "Celestial Bronze Helmet", "DEF": 3.2, "SP": 1, "MAX DUR": 4900, "DUR": 4900, "Class": "Helmet"},
        "Chestplate": {"Name": "Celestial Bronze Chestplate", "DEF": 3.8, "SP": 1, "MAX DUR": 5200, "DUR": 5200, "Class": "Chestplate"},
        "Leggings": {"Name": "Admantine Leggings", "DEF": 2.6, "SP": 2, "MAX DUR": 4800, "DUR": 4800, "Class": "Boots"},
        "Boots": {"Name": "Reinforced Feather Boots", "DEF": 2.0, "SP": 3, "MAX DUR": 4700, "DUR": 4700, "Class": "Boots"}
    },
    "Troll Swordsman": {
        "HP": 7500,
        "ATK": 88,
        "DEF": 24,
        "Crit": 16,
        "SP": 22,
        "EXP": 1100,
        "Prisms": 3,
        "Weapon": {"Name": "Ghoststeel Sharpsword", "ATK": 5.2, "SP": 1, "Crit": 5, "MAX DUR": 6000, "DUR": 6000, "Class": "Weapon"},
        "Left Hand": {"Name": "Starsteel Aegis", "DEF": 3.8, "SP": 1, "MAX DUR": 6300, "DUR": 6300, "Class": "Shield"},
        "Helmet": {"Name": "Voidglass Helmet", "DEF": 2.2, "SP": 1, "MAX DUR": 4800, "DUR": 4800, "Class": "Helmet"},
        "Chestplate": {"Name": "Voidglass Chestplate", "DEF": 3.0, "SP": 1, "MAX DUR": 5200, "DUR": 5200, "Class": "Chestplate"},
        "Leggings": {"Name": "Voidglass Leggings", "DEF": 2.4, "SP": 2, "MAX DUR": 5000, "DUR": 5000, "Class": "Boots"},
        "Boots": {"Name": "Voidglass Boots", "DEF": 1.6, "SP": 3, "MAX DUR": 4700, "DUR": 4700, "Class": "Boots"}
    }
}

# ========ENCHANTMENTS=========
sword1_enchants = [
    "Sharpness"
]
sword2_enchants = [ #  "Unbreaking"
    "Sharpness", "Thorns", "Unbreakable"
]
sword3_enchants = [
    "Sharpness", "Thorns", "Unbreaking", "Fire Aspect", "Looting"
]
shield1_enchants = [
    "Protection"
]
shield2_enchants = [ 
    "Protection", "Thorns", "Unbreaking"
]
shield3_enchants = [
    "Protection", "Thorns", "Unbreaking", "Divine Guard"
]
armor1_enchants = [
    "Protection", "Fire Protection"
]
armor2_enchants = [ # Unbreaking
    "Protection", "Fire Protection", "Heartforge", "Unbreaking"
]
armor3_enchants = [
    "Protection", "Fire Protection", "FrostGuard", "Heartforge", "Unbreaking"
]

# ========FISHING=========
tier1_fish = [
    ("Minnow", 1), ("Pond Carp", 2), ("Sunfish", 3), ("Bluegill", 4), ("Goldfish", 5),
    ("Small Fry", 6), ("Silver Shiner", 7), ("Dace", 8), ("Gudgeon", 9), ("Chub", 10),
    ("Fathead Minnow", 11), ("Mosquitofish", 12), ("Topminnow", 13), ("Killifish", 14), ("Sculpin", 15),
    ("Stickelback", 16), ("Blenny", 17), ("Gobies", 18), ("Pike Minnow", 19), ("Rainbow Smelt", 20),
    ("Shiner", 21), ("Whitefish", 22), ("Golden Shiner", 23), ("Silverside", 24), ("Glassfish", 25),
    ("Round Goby", 26), ("Creek Chub", 27), ("Pygmy Sunfish", 28), ("Black Bullhead", 29), ("Brook Stickleback", 30),
    ("Northern Hogsucker", 31), ("Rainbow Darter", 32), ("Johnny Darter", 33), ("Fantail Darter", 34), ("Blacknose Dace", 35),
    ("Longnose Dace", 36), ("Longear Sunfish", 37), ("Pumpkinseed", 38), ("Rock Bass", 39), ("Warmouth", 40),
    ("Tadpole Madtom", 41), ("Slender Madtom", 42), ("Stonecat", 43), ("Margined Madtom", 44), ("Ozark Madtom", 45),
    ("Blackside Darter", 46), ("Logperch", 47), ("Sauger", 48), ("Walleye Pollock", 49), ("Grass Carp", 50)
] # 50
tier2_fish = [
    ("Rainbow Trout", 30), ("Smallmouth Bass", 35), ("Walleye", 40), ("Northern Pike", 45), ("Channel Catfish", 50),
    ("White Bass", 55), ("Yellow Perch", 60), ("Rockfish", 65), ("Crappie", 70), ("Blue Catfish", 75),
    ("Largemouth Bass", 80), ("Brown Trout", 85), ("Lake Trout", 90), ("Brook Trout", 95), ("Yellowtail Snapper", 100),
    ("Gizzard Shad", 105), ("Striped Bass", 110), ("Spotted Bass", 115), ("Flathead Catfish", 120), ("Zander", 125),
    ("Steelhead", 130), ("Red Drum", 135), ("Sheepshead", 140), ("Bluegill Sunfish", 145), ("Pumpkinseed Sunfish", 150),
    ("Bowfin", 155), ("Grass Pickerel", 160), ("Chain Pickerel", 165), ("Paddlefish", 170), ("Tench", 175),
    ("White Perch", 180), ("White Crappie", 185), ("Black Crappie", 190), ("Atlantic Salmon", 195), ("Chinook Salmon", 200),
    ("Coho Salmon", 205), ("Pink Salmon", 210), ("Sockeye Salmon", 215), ("Lake Sturgeon", 220), ("Shovelnose Sturgeon", 225),
    ("Shortnose Sturgeon", 230), ("Gar", 235), ("Bowfin", 240), ("Bowfin", 245), ("Longnose Gar", 250), ("Alligator Gar", 255),
    ("Spotted Gar", 260), ("Atlantic Sturgeon", 265), ("White Sturgeon", 270), ("Paddlefish", 275)
] # 50
tier3_fish = [
    ("Salmon", 200), ("Largemouth Bass", 220), ("Steelhead", 240), ("Brown Trout", 260), ("Blue Catfish", 280),
    ("Muskellunge", 300), ("Arctic Char", 320), ("Golden Dorado", 340), ("Giant Trevally", 360), ("Sturgeon", 380),
    ("Tarpon", 400), ("Atlantic Bluefin Tuna", 420), ("Marlin", 440), ("Swordfish", 460), ("Barracuda", 480),
    ("King Mackerel", 500), ("Sailfish", 520), ("Wahoo", 540), ("Grouper", 560), ("Snapper", 580),
    ("Atlantic Cod", 600), ("Pacific Cod", 620), ("Halibut", 640), ("Pollock", 660), ("Rockfish", 680),
    ("Lingcod", 700), ("Black Drum", 720), ("Red Snapper", 740), ("White Bass", 760), ("Bluefish", 780),
    ("Sheepshead", 800), ("Cobia", 820), ("Tilefish", 840), ("Scup", 860), ("Atlantic Herring", 880),
    ("Pacific Herring", 900), ("Capelin", 920), ("Shad", 940), ("Smelt", 960), ("Menhaden", 980),
    ("Butterfish", 1000), ("Dogfish", 1020), ("Spiny Dogfish", 1040), ("Smooth Dogfish", 1060), ("Brown Bullhead", 1080),
    ("Yellow Bullhead", 1100), ("Black Bullhead", 1120), ("White Catfish", 1140), ("Channel Catfish", 1160), ("Flathead Catfish", 1180)
] # 50
tier4_fish = [
    ("Giant Catfish", 1500), ("Megalodon Tooth", 1550), ("Golden Arowana", 1600), ("Giant Trevally", 1650), ("Arapaima", 1700),
    ("Ocean Sunfish", 1750), ("Giant Grouper", 1800), ("Goliath Grouper", 1850), ("Siberian Sturgeon", 1900), ("White Sturgeon", 1950),
    ("Alligator Gar", 2000), ("Atlantic Blue Marlin", 2050), ("Pacific Blue Marlin", 2100), ("Black Marlin", 2150), ("Striped Marlin", 2200),
    ("Swordfish", 2250), ("Giant Trevally", 2300), ("Mekong Giant Catfish", 2350), ("Giant Freshwater Stingray", 2400), ("Pirarucu", 2450),
    ("Atlantic Goliath Grouper", 2500), ("Pacific Goliath Grouper", 2550), ("Giant Sea Bass", 2600), ("Napoleon Wrasse", 2650), ("Giant Freshwater Pufferfish", 2700),
    ("Oceanic Whitetip Shark", 2750), ("Great White Shark", 2800), ("Tiger Shark", 2850), ("Bull Shark", 2900), ("Hammerhead Shark", 2950),
    ("Mako Shark", 3000), ("Thresher Shark", 3050), ("Goblin Shark", 3100), ("Frilled Shark", 3150), ("Megamouth Shark", 3200),
    ("Wobbegong", 3250), ("Sawfish", 3300), ("Basking Shark", 3350), ("Whale Shark", 3400), ("Manta Ray", 3450),
    ("Giant Manta Ray", 3500), ("Devil Ray", 3550), ("Eagle Ray", 3600), ("Cownose Ray", 3650), ("Blue Spotted Stingray", 3700)
] # 45
tier5_fish = [
    ("Legendary Leviathan", 5000), ("Mythic Kraken", 5200), ("Ancient Dragonfish", 5400), ("Celestial Marlin", 5600), ("Ethereal Angler", 5800),
    ("Phantom Serpent", 6000), ("Void Leviathan", 6200), ("Elder Hydra", 6400), ("Titanic Whale", 6600), ("Oceanic Behemoth", 6800),
    ("Abyssal Horror", 7000), ("Deep Sea Colossus", 7200), ("Kraken's Spawn", 7400), ("Celestial Leviathan", 7600), ("Mythical Sea Dragon", 7800),
    ("Elder Sea Serpent", 8000), ("Ghost Marlin", 8200), ("Phantasmal Swordfish", 8400), ("Spirit Tuna", 8600), ("Wraith Snapper", 8800),
    ("Spectral Grouper", 9000), ("Arcane Catfish", 9200), ("Astral Manta", 9400), ("Void Sturgeon", 9600), ("Mythic Goliath Grouper", 9800),
    ("Legendary Hammerhead", 10000), ("Celestial Shark", 10200), ("Ethereal Mako", 10400), ("Phantom Bull Shark", 10600), ("Spirit Tiger Shark", 10800),
    ("Ancient Sawfish", 11000), ("Ghostly Wobbegong", 11200), ("Mythic Basking Shark", 11400), ("Elder Whale Shark", 11600), ("Titanic Manta Ray", 11800),
    ("Celestial Devil Ray", 12000), ("Ethereal Eagle Ray", 12200), ("Phantasmal Cownose Ray", 12400), ("Wraith Blue Spotted Stingray", 12600), ("Spectral Giant Manta Ray", 12800)
] # 40

# ========GAME FUNCTIONS=========
def clear_last_line():
    sys.stdout.write("\033[F")  # Move cursor up one line
    sys.stdout.write("\033[K")

progress = {
    "start_time": None,
    "duration": None,
    "done": False,
    "item": None
}
def worker(item, duration, string):
    progress["start_time"] = time.time()
    progress["duration"] = duration
    progress["done"] = False
    progress["item"] = item
    while True:
        elapsed = time.time() - progress["start_time"]
        percent = min(100, int((elapsed / duration) * 100))
        remaining = max(0.0, duration - elapsed)

        clear()
        print(f"🛠️ {string} {item}...")
        print(f"Progress: {percent}% [{'=' * (percent // 5)}{' ' * (20 - percent // 5)}]  ⏳ {remaining:.1f}s left")

        if elapsed >= duration:
            break
        time.sleep(0.1)

    progress["done"] = True
    clear()
def start(item, action, lower, upper):
    duration = random.uniform(lower, upper)
    worker(item, duration, action)
def timer_loop(seconds):
    global tournament_active
    start = time.time()
    while time.time() - start < seconds:
        time.sleep(1)
    tournament_active[0] = False
    print("\n🏆 Tournament Over!")

enchant_progress = {
    "start_time": None,
    "duration": None,
    "done": False
}
def enchantment_worker(duration):
    enchant_progress["start_time"] = time.time()
    enchant_progress["duration"] = duration
    enchant_progress["done"] = False
    while True:
        elapsed = time.time() - enchant_progress["start_time"]
        if elapsed >= duration:
            enchant_progress["done"] = True
            break
        time.sleep(0.2)
def start_enchant(duration):
    threading.Thread(target=enchantment_worker, args=(duration,), daemon=True).start()
    print("✨ Enchantment begun! Do your thing while the crystal does its magic... 🧙‍♀️💠")
def check_enchantment():
    if enchant_progress["start_time"] is None:
        print("🧐 Nothing is being enchanted right now!")
        return

    print("📡 Enchantment progress ... (press ENTER to return to town 🏙️)")

    while True:
        if enchant_progress["done"]:
            return 1
        else:
            elapsed = time.time() - enchant_progress["start_time"]
            remaining = enchant_progress["duration"] - elapsed
            percent = int((elapsed / enchant_progress["duration"]) * 100)
            print(f"\r🧪 Enchanting... {percent}% done | {remaining:.1f}s left", end="", flush=True)
            time.sleep(0.00001)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            input()  
            print("\n🚪 You leave the armory and head back to town.")
            break

def load_players(filename="players.json"):
    if os.path.exists(filename):
            if os.path.getsize(filename) == 0:
                with open(filename, "w") as file:
                    json.dump({}, file)
            with open(filename, "r") as file:
                return json.load(file)
    else:
        return {}
def save_players(players, filename="players.json"):
    with open(filename, "w") as file:
        json.dump(players, file, indent=4)

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
def type(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
def fasttype(text, delay=0.005):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def run_arena_style_combat(stats: Dict[str, Any], foe: Dict[str, Any]) -> Tuple[bool, int]:
    return _arena_combat_engine(stats, foe, type, clear, fasttype)

def grant_exp(stats: Dict[str, Any], amount: float) -> None:
    stats["EXP"] = stats.get("EXP", 0) + amount
    while stats["EXP"] >= stats["Max EXP"]:
        over = stats["EXP"] - stats["Max EXP"]
        stats["Lvl"] += 1
        stats["Max EXP"] += 20
        stats["EXP"] = over

def _apply_arena_rewards(stats: Dict[str, Any], won: bool, foe_lvl: int, turns: int) -> None:
    if not won:
        type("You limp away from the arena...")
        time.sleep(0.8)
        clear()
        return
    base_exp = max(25, foe_lvl * 6)
    speed_bonus = max(0, int(35 - turns * 2))
    total_exp = base_exp + speed_bonus
    grant_exp(stats, float(total_exp))
    gold_gain = foe_lvl * 22 + speed_bonus * 4
    stats["Gold"] += gold_gain
    stats["Reputation"] = stats.get("Reputation", 0) + 1
    type(f"Victory spoils: +{total_exp} EXP (speed bonus included), +{gold_gain} gold, +1 reputation.")
    time.sleep(0.9)
    clear()

def build_duel_foe_from_key(enemy_players: Dict[Any, Dict[str, Any]], p_key: Any) -> Dict[str, Any]:
    """Build combat foe dict compatible with arena_combat from an arena challenger entry."""
    foe_lvl_roll = max(1, int(enemy_players[p_key]["lvl"]))
    wroll = random.randint(1, 100)
    if wroll <= 70 - foe_lvl_roll:
        foe_weapon = random.choice(swords)
    else:
        foe_weapon = random.choice(elite_swords)
    arena_shields = [
        {"Name": "Reinforced Bark Shield", "DEF": 1.5, "SP": 0.8, "MAX DUR": 900, "DUR": 900, "Cost": 7000, "Class": "Shield"},
        {"Name": "Rusty Steel Shield", "DEF": 1.3, "SP": 0.8, "MAX DUR": 1000, "DUR": 1000, "Cost": 5000, "Class": "Shield"},
        {"Name": "Chainmail Shield", "DEF": 1.2, "SP": 0.9, "MAX DUR": 850, "DUR": 850, "Cost": 5000, "Class": "Shield"},
        {"Name": "Reinforced Leather Shield", "DEF": 1.5, "SP": 1, "MAX DUR": 1150, "DUR": 1150, "Cost": 9000, "Class": "Shield"},
        {"Name": "Wooden Shield", "DEF": 2, "SP": 1, "MAX DUR": 60, "DUR": 60, "Cost": 14000, "Class": "Shield"},
        {"Name": "Rusted Steel Shield", "DEF": 1.3, "SP": 0.8, "MAX DUR": 1000, "DUR": 1000, "Cost": 4000, "Class": "Shield"},
        {"Name": "Leather Shield", "DEF": 1.5, "SP": 1, "MAX DUR": 1150, "DUR": 1150, "Cost": 8000, "Class": "Shield"}
    ]
    foe_shield = random.choice(arena_shields)
    chestplate_roll = random.randint(1, 100)
    if chestplate_roll <= 70 - foe_lvl_roll:
        foe_chest = random.choice(chestplates)
    else:
        foe_chest = None
    helmet_roll = random.randint(1, 100)
    if helmet_roll <= 70 - foe_lvl_roll:
        foe_helmet = random.choice(helmets)
    else:
        foe_helmet = None
    legging_roll = random.randint(1, 100)
    if legging_roll <= 70 - foe_lvl_roll:
        foe_legging = random.choice(leggings)
    else:
        foe_legging = None
    boot_roll = random.randint(1, 100)
    if boot_roll <= 70 - foe_lvl_roll:
        foe_boot = random.choice(boots)
    else:
        foe_boot = None
    enemyhp = 1700
    enemystr = 150
    enemydef = 70
    enemycrit = 7
    enemysp = 20
    if foe_lvl_roll <= 0:
        buff_times = 1
    else:
        buff_times = foe_lvl_roll
    for _ in range(buff_times):
        bt = random.choice(["HP", "ATK", "DEF", "SP", "CRIT"]).lower()
        if bt == "hp":
            enemyhp += 200
        elif bt == "atk":
            enemystr += 10
        elif bt == "def":
            enemydef += 20
        elif bt == "sp":
            enemysp += 2.5
        elif bt == "crit":
            enemycrit += 0.5
    return {
        "name": enemy_players[p_key]["name"],
        "lvl": enemy_players[p_key]["lvl"],
        "enemyhp": enemyhp,
        "enemystr": enemystr,
        "enemydef": enemydef,
        "enemycrit": enemycrit,
        "enemysp": enemysp,
        "weapon": foe_weapon,
        "shield": foe_shield,
        "helmet": foe_helmet,
        "chestplate": foe_chest,
        "legging": foe_legging,
        "boot": foe_boot,
    }

def roll_random_arena_npc(player_stats: Dict[str, Any]) -> Dict[str, Any]:
    rank = random.randint(player_stats["Rank"] - 1000, player_stats["Rank"] + 1000)
    hi = random.choice(["Yes", "No"])
    prefix = random.choice(prefixes)
    middle = random.choice(middles)
    suffix = random.choice(suffixes)
    if hi == "Yes":
        nid = random.randint(0, 999)
        player_name = f"{prefix}{middle}{suffix}_{nid}"
    else:
        player_name = f"{prefix}{middle} {suffix}"
    lvl = random.randint(max(1, player_stats["Lvl"] - 10), player_stats["Lvl"] + 10)
    challenger = {0: {"name": player_name, "rank": rank, "lvl": lvl}}
    return build_duel_foe_from_key(challenger, 0)

def foe_from_boss_entry(player_stats: Dict[str, Any], boss_title: str, bdata: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "name": boss_title,
        "lvl": max(1, player_stats["Lvl"]),
        "enemyhp": bdata["HP"],
        "enemystr": bdata["ATK"],
        "enemydef": bdata["DEF"],
        "enemycrit": bdata["Crit"],
        "enemysp": bdata["SP"],
        "weapon": copy.deepcopy(bdata["Weapon"]),
        "shield": copy.deepcopy(bdata["Left Hand"]),
        "helmet": copy.deepcopy(bdata["Helmet"]),
        "chestplate": copy.deepcopy(bdata["Chestplate"]),
        "legging": copy.deepcopy(bdata["Leggings"]),
        "boot": copy.deepcopy(bdata["Boots"]),
    }

def adventure() -> None:
    global stats
    start("Adventure", "Seeking riches in Rotfang Depths", 3, 6)
    clear()
    rotfang_depths()

def rotfang_depths() -> None:
    global stats
    type("Cold wind rises from Rotfang Depths. Bosses guarding Celestium Prisms stir below.\n")
    time.sleep(0.35)
    names = list(boss.keys())
    for i, n in enumerate(names, start=1):
        prism_ct = boss[n].get("Prisms", 1)
        type(f"{i}. {n} (~{boss[n]['EXP']} EXP · {prism_ct} prism(s))")
        time.sleep(0.05)
    pick = int(input("Choose a foe (number), or 0 to leave: "))
    clear()
    if pick == 0:
        type("You climb back toward town.\n")
        time.sleep(0.4)
        clear()
        return
    title = names[pick - 1]
    bdata = boss[title]
    type(f"You drop into the depths to challenge {title}!")
    time.sleep(0.85)
    clear()
    foe = foe_from_boss_entry(stats, title, bdata)
    won, turns = run_arena_style_combat(stats, foe)
    if won:
        prisms = bdata.get("Prisms", 1)
        stats["Celestium Prism"] = stats.get("Celestium Prism", 0) + prisms
        boss_exp = float(bdata.get("EXP", 400))
        grant_exp(stats, boss_exp + max(50, stats["Lvl"] * 5))
        gold_bonus = boss_exp + turns * 3
        stats["Gold"] += int(gold_bonus)
        stats["Reputation"] = stats.get("Reputation", 0) + 2
        type(f"{title} falls! Celestium Prisms gained: +{prisms}. Bonus gold: +{int(gold_bonus)}.")
        time.sleep(0.9)
    else:
        type("You barely escape Rotfang Depths alive...")
        time.sleep(0.9)
    clear()

def chat(text):
    for char in text:
        delay = random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07])
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()
def quest():
    print("    _______                    ___________      ________   ___________")
    print("   /       \\    |          |  |                /                |")
    print("  /         \\   |          |  |               /                 |")
    print(" |           |  |          |  |___________   /__________        |")
    print(" |           |  |          |  |                        /        |")
    print("  \\        \\\\   \\          /  |                       /         |")
    print("   \\_______ \\\\   \\________/   |___________   ________/          |")
    print("\n|----------|")
    time.sleep(random.uniform(0.5, 3))
    clear()
    print("    _______                    ___________      ________   ___________")
    print("   /       \\    |          |  |                /                |")
    print("  /         \\   |          |  |               /                 |")
    print(" |           |  |          |  |___________   /__________        |")
    print(" |           |  |          |  |                        /        |")
    print("  \\        \\\\   \\          /  |                       /         |")
    print("   \\_______ \\\\   \\________/   |___________   ________/          |")
    print("\n|===-------|")
    time.sleep(random.uniform(0.5, 3))
    clear()
    print("    _______                    ___________      ________   ___________")
    print("   /       \\    |          |  |                /                |")
    print("  /         \\   |          |  |               /                 |")
    print(" |           |  |          |  |___________   /__________        |")
    print(" |           |  |          |  |                        /        |")
    print("  \\        \\\\   \\          /  |                       /         |")
    print("   \\_______ \\\\   \\________/   |___________   ________/          |")
    print("\n|=====-----|")
    time.sleep(random.uniform(0.5, 3))
    clear()
    print("    _______                    ___________      ________   ___________")
    print("   /       \\    |          |  |                /                |")
    print("  /         \\   |          |  |               /                 |")
    print(" |           |  |          |  |___________   /__________        |")
    print(" |           |  |          |  |                        /        |")
    print("  \\        \\\\   \\          /  |                       /         |")
    print("   \\_______ \\\\   \\________/   |___________   ________/          |")
    print("\n|=======---|")
    time.sleep(random.uniform(0.5, 5))
    clear()
    print("    _______                    ___________      ________   ___________")
    print("   /       \\    |          |  |                /                |")
    print("  /         \\   |          |  |               /                 |")
    print(" |           |  |          |  |___________   /__________        |")
    print(" |           |  |          |  |                        /        |")
    print("  \\        \\\\   \\          /  |                       /         |")
    print("   \\_______ \\\\   \\________/   |___________   ________/          |")
    print("\n|==========|")
    time.sleep(random.uniform(0.5, 2))
    clear()
def welcome() -> Dict[str, Any]:
    os.system('git fetch')
    os.system('git checkout origin/main -- players.json')
    players = load_players()
    clear()
    name = " "
    clear()
    response = int(input("Register or Login (Type 1 for register, 2 for login): "))
    clear()
    if response == 1:
        hi = random.choice(["Yes", "No"])
        prefix = random.choice(prefixes)
        middle = random.choice(middles)
        suffix = random.choice(suffixes)
        if hi == "Yes":
            id = random.randint(0, 999)
            name = f"{prefix}{middle}{suffix}_{id}"
        else:
            name = f"{prefix}{middle} {suffix}"

        print(f"Name: {name}")
        type(f"{name}, welcome to Quest!")
        print()
        type("Pick a class:")
        type("1. Warrior (Medium HP, Medium STR, Medium SP, High Reputation)")
        type("2. Thief (Low HP, Medium STR, High SP, Low Reputation)")
        type("3. Berserker (High HP, High STR, Low SP, Medium Reputation)")
        your_class = input("Which class: ").strip()
        clear()
        if your_class == "1" or your_class.lower() == "warrior":
            player_stats = {
                "Name": name,
                "Lvl": 1,
                "Rank": 10000,
                "Max EXP": 20,
                "EXP": 0,
                "Gold": 50,
                "Diamond": 1,
                "Dragonite": 0,
                "Celestium Prism": 0,
                "HP": 1700,
                "STR": 80,
                "SP": 20,
                "Crit": 7,
                "DEF": 70,
                "Reputation": 5,
                "Weapon": {"Name": "Wooden Sword", "ATK": 4, "SP": 1, "Crit": 1.5, "DUR": 60, "Class": "Weapon", "Cost": 400},
                "Left Hand": {"Name": "Wooden Shield", "DEF": 2, "SP": 1, "DUR": 60, "Class": "Shield", "Cost": 400},
                "Helmet": {},
                "Chestplate": {},
                "Leggings": {},
                "Boots": {},
                "Backpack": [
                    {"Name": "Potion of Healing", "Tier": 1, "Effect": 500, "Class": "Potion of Healing", "Cost": 200}
                ]
            }
            #start("Account", "Creating", 6, 12)
        elif your_class == "2" or your_class.lower() == "thief":
            player_stats = {
                "Name": name,
                "Lvl": 1,
                "Rank": 10000,
                "Max EXP": 20,
                "EXP": 0,
                "Gold": 100,
                "Diamond": 1,
                "Dragonite": 0,
                "Celestium Prism": 0,
                "HP": 1300,
                "STR": 60,
                "SP": 40,
                "Crit": 5,
                "DEF": 50,
                "Reputation": 1,
                "Weapon": {"Name": "Dagger", "ATK": 3, "SP": 1.2, "Crit": 1, "DUR": 100, "Class": "Weapon", "Cost": 400},
                "Left Hand": {"Name": "Leather Shield", "DEF": 1.5, "SP": 1.1, "DUR": 50, "Class": "Shield", "Cost": 400},
                "Helmet": {},
                "Chestplate": {},
                "Leggings": {},
                "Boots": {},
                "Backpack": [
                    {"Name": "Potion of Healing", "Tier": 1, "Effect": 500, "Class": "Potion of Healing", "Cost": 200},
                    {"Name": "Potion of Strength", "Tier": 1, "Effect": 1.5, "Class": "Potion of Strength", "Cost": 200}
                ]
            }
            #start("Account", "Creating", 6, 12)
        elif your_class == "3" or your_class.lower() == "berserker":
            player_stats = {
                "Name": name,
                "Lvl": 1,
                "Rank": 10000,
                "Max EXP": 20,
                "EXP": 0,
                "Gold": 0,
                "Diamond": 1,
                "Dragonite": 0,
                "Celestium Prism": 100000,
                "HP": 2100,
                "STR": 110,
                "SP": 10,
                "Crit": 10,
                "DEF": 100,
                "Reputation": 3,
                "Weapon": {"Name": "Great Axe", "ATK": 5, "SP": 0.8, "Crit": 2, "DUR": 120, "Class": "Weapon", "Cost": 400},
                "Left Hand": {"Name": "Rusted Steel Shield", "DEF": 2, "SP": 0.5, "DUR": 70, "Class": "Shield", "Cost": 400},
                "Helmet": {},
                "Chestplate": {},
                "Leggings": {},
                "Boots": {},
                "Backpack": [
                    {"Name": "Potion of Healing", "Tier": 1, "Effect": 500, "Class": "Potion of Healing", "Cost": 200}
                ]
            }
            #start("Account", "Creating", 6, 12)
        else:
            type("Invalid choice! Defaulting to Warrior.")
            player_stats = {
                "Name": name,
                "Lvl": 1,
                "Rank": 10000,
                "Max EXP": 20,
                "EXP": 0,
                "Gold": 50,
                "Diamond": 1,
                "Dragonite": 0,
                "Celestium Prism": 0,
                "HP": 1700,
                "STR": 80,
                "SP": 20,
                "Crit": 7,
                "DEF": 70,
                "Reputation": 5,
                "Weapon": {"Name": "Wooden Sword", "ATK": 4, "SP": 1, "Crit": 1.5, "DUR": 60, "Class": "Weapon", "Cost": 400},
                "Left Hand": {"Name": "Wooden Shield", "DEF": 2, "SP": 1, "DUR": 60, "Class": "Shield", "Cost": 400},
                "Helmet": {},
                "Chestplate": {},
                "Leggings": {},
                "Boots": {},
                "Backpack": [
                    {"Name": "Potion of Healing", "Tier": 1, "Effect": 500, "Class": "Potion of Healing", "Cost": 200}
                ]
            }
            #start("Account", "Creating", 6, 12)
        return player_stats

    elif response == 2:
        name = input("Enter your name: ")
        clear()
        if name in players:
            type(f"Welcome back, {name}! \n")
            time.sleep(0.5)
            clear()
            #start("Player Stats", "Loading", 2, 5)
            clear()
            return players[name]
        else:
            type("Invalid name! Creating a new account. Defaulting to Warrior.")
            time.sleep(1)
            player_stats = {
                "Name": name,
                "Lvl": 1,
                "Rank": 10000,
                "Max EXP": 20,
                "EXP": 0,
                "Gold": 50,
                "Diamond": 1,
                "Dragonite": 0,
                "Celestium Prism": 0,
                "HP": 1700,
                "STR": 80,
                "SP": 20,
                "Crit": 7,
                "DEF": 70,
                "Reputation": 5,
                "Weapon": {"Name": "Wooden Sword", "ATK": 4, "SP": 1, "Crit": 1.5, "DUR": 60, "Class": "Weapon", "Cost": 400},
                "Left Hand": {"Name": "Wooden Shield", "DEF": 2, "SP": 1, "DUR": 60, "Class": "Shield", "Cost": 400},
                "Helmet": {},
                "Chestplate": {},
                "Leggings": {},
                "Boots": {},
                "Backpack": [
                    {"Name": "Potion of Healing", "Tier": 1, "Effect": 500, "Class": "Potion of Healing", "Cost": 200}
                ]
            }
            #start("Account", "Creating", 6, 12)
            return player_stats
    else:
        type("Invalid choice! Creating a new account. Defaulting to Warrior.")
        player_stats = {
            "Name": name,
            "Lvl": 1,
            "Rank": 10000,
            "Max EXP": 20,
            "EXP": 0,
            "Gold": 50,
            "Diamond": 1,
            "Dragonite": 0,
            "Celestium Prism": 0,
            "HP": 1700,
            "STR": 80,
            "SP": 20,
            "Crit": 7,
            "DEF": 70,
            "Reputation": 5,
            "Weapon": {"Name": "Wooden Sword", "ATK": 4, "SP": 1, "Crit": 1.5, "DUR": 60, "Class": "Weapon", "Cost": 400},
            "Left Hand": {"Name": "Wooden Shield", "DEF": 2, "SP": 1, "DUR": 60, "Class": "Shield", "Cost": 400},
            "Helmet": {},
            "Chestplate": {},
            "Leggings": {},
            "Boots": {},
            "Backpack": [
                {"Name": "Potion of Healing", "Tier": 1, "Effect": 500, "Class": "Potion of Healing", "Cost": 200}
            ]
        }
        #start("Account", "Creating", 6, 12)
        return player_stats



# =========VARIABLES=========
players = load_players()
block = 0
stats = welcome()
players[stats["Name"]] = stats
save_players(players)
option = 0
sword = None
shield = None
enchantment = False
enchanting_name = ""
enchants = ""
enchant_num = 0
enchant = 0
chestplate = 0
tournament_active = [False]

def arena():
    enemy_players = {}
    your_players = {}
    start("Arena", "Entering the", 1, 2.5)
    clear()
    type("Welcome to the arena!\n")
    time.sleep(0.5)
    type("Here you can fight against other players and gain EXP, Gold, and Reputation!\n")
    time.sleep(0.5)
    type("The less turns you take to kill the other player, the more EXP and Gold you get!\n")
    time.sleep(0.5)
    clear()
    type("Game Modes: \n")
    time.sleep(0.1)
    type("\t1. Duels\n")
    time.sleep(0.1)
    type("\t2. Duel Clash\n")
    time.sleep(0.1)
    gamemode = int(input("Which game mode would you like to play: "))
    clear()
    if gamemode == 1:
        start("Arena", "Sharpening blades for", 2, 3.6)
        clear()
        foe = roll_random_arena_npc(stats)
        type(f"You face {foe['name']} (Lvl {foe['lvl']})!\n")
        time.sleep(0.85)
        clear()
        won, turns = run_arena_style_combat(stats, foe)
        _apply_arena_rewards(stats, won, foe["lvl"], turns)
        return

    elif gamemode == 2:
        yesorno = input("Start tutorial? (yes/no): ").lower()
        clear()
        if yesorno == "yes":
            description = """
            ======================================
                      ⚔️ DUEL CLASH ⚔️
            ======================================

            Overview:
            Your squad cheers you on as you duel each challenger from the enemy roster — one duel at a time.

            How It Works:
            - Two teams parade while you represent your faction in the cage.
            - Opponents from the opposing roster rotate in randomized order until you lose or wipe their bench.
            - Each victory scores for your backers; losing a duel stops the clash run.
            - Between rounds there is only the roar of the crowd — conserve potions wisely.

            Victory Condition:
            Defeat everyone on their roster without being knocked out to claim a sweep bonus.

            ======================================
            """
            fasttype(description)
            hi = int(input("Press 1 to continue: "))
            clear()
            if hi == 1:
                time.sleep(0)
            else:
                time.sleep(0)
        if yesorno == "no":
            time.sleep(1)
        type("Your Team: ")
        type("=====================================")
        for _ in range(4):
            times = random.randint(0, 5)
            for j in range(times):
                dots = "." * ((j % 3) + 1)
                print(dots.ljust(3), end='\r')
                time.sleep(0.4)
            print("   ", end='\r')
            rank = random.randint(stats["Rank"] - 1000, stats["Rank"] + 1000)
            hi = random.choice(["Yes", "No"])
            prefix = random.choice(prefixes)
            middle = random.choice(middles)
            suffix = random.choice(suffixes)
            if hi == "Yes":
                pid = random.randint(0, 999)
                player_name = f"{prefix}{middle}{suffix}_{pid}"
            else:
                player_name = f"{prefix}{middle} {suffix}"
            ID = random.randint(0, 100000)
            lvl = random.randint(max(1, stats["Lvl"] - 10), stats["Lvl"] + 10)
            your_players[ID] = {"name": player_name, "rank": rank, "lvl": lvl}
            print("---------------------------------------------------------------------")
            print(f"{player_name} | Lvl: {lvl} | ID: {ID} | Rank: {rank}")
            print("---------------------------------------------------------------------\n")
            time.sleep(0.5)
        type("=====================================\n")
        type("Opponent's Team: ")
        type("=====================================")
        for _ in range(5):
            times = random.randint(0, 5)
            for j in range(times):
                dots = "." * ((j % 3) + 1)
                print(dots.ljust(3), end='\r')
                time.sleep(0.4)
            print("   ", end='\r')
            rank = random.randint(stats["Rank"] - 1000, stats["Rank"] + 1000)
            hi = random.choice(["Yes", "No"])
            prefix = random.choice(prefixes)
            middle = random.choice(middles)
            suffix = random.choice(suffixes)
            if hi == "Yes":
                pid = random.randint(0, 999)
                player_name = f"{prefix}{middle}{suffix}_{pid}"
            else:
                player_name = f"{prefix}{middle} {suffix}"
            ID = random.randint(0, 100000)
            lvl = random.randint(max(1, stats["Lvl"] - 10), stats["Lvl"] + 10)
            enemy_players[ID] = {"name": player_name, "rank": rank, "lvl": lvl}
            print("---------------------------------------------------------------------")
            print(f"{player_name} | Lvl: {lvl} | ID: {ID} | Rank: {rank}")
            print("---------------------------------------------------------------------\n")
            time.sleep(0.5)
        type("=====================================\n")
        start("Match", "Starting", 4, 10)
        clear()
        enemy_order = list(enemy_players.keys())
        random.shuffle(enemy_order)
        wins = 0
        sweep = True
        for duel_idx, opp_key in enumerate(enemy_order, start=1):
            type(f"Duel Clash — round {duel_idx} of {len(enemy_order)}.\n")
            foe = build_duel_foe_from_key(enemy_players, opp_key)
            type(f"You clash with {foe['name']} (Lvl {foe['lvl']})!\n")
            time.sleep(0.85)
            clear()
            won, turns = run_arena_style_combat(stats, foe)
            if won:
                wins += 1
                type(f"Ladder score: your squad {wins} — {(len(enemy_order) - wins)} foes still itching to fight.")
                _apply_arena_rewards(stats, True, foe["lvl"], turns)
            else:
                sweep = False
                _apply_arena_rewards(stats, False, foe["lvl"], turns)
                break
        if sweep and wins == len(enemy_order):
            bonus = 850 + stats["Lvl"] * 50
            stats["Gold"] += bonus
            stats["Reputation"] = stats.get("Reputation", 0) + 4
            type(f"Sweep secured! Sponsor bonus gold +{bonus} and prestige +4.\n")
            time.sleep(0.9)
            clear()

    else:
        print("Invalid game mode!")
        time.sleep(1)
        clear()


def npc_fishing(player):
    global tournament_active
    while tournament_active[0]:
        lure_cnt = random.randint(80, 500)
        if lure_cnt <= 0:
            continue
        else:
            for i in range(lure_cnt):
                lure_cnt -= 1
                wait_time = random.randint(1, 6) 
                time.sleep(wait_time)
                rarity = random.randint(1, 100)
                if rarity <= 60:
                    fish = random.randint(1, 50)
                    value = tier1_fish[fish - 1][1]
                elif rarity <= 80:
                    fish = random.randint(1, 50)
                    value = tier2_fish[fish - 1][1]
                elif rarity <= 87:
                    fish = random.randint(1, 50)
                    value = tier3_fish[fish - 1][1]
                elif rarity <= 98:
                    fish = random.randint(1, 45)
                    value = tier4_fish[fish - 1][1]
                else:
                    fish = random.randint(1, 40)
                    value = tier5_fish[fish - 1][1]
                player["total_value"] += value
def fishing():
    broke = False
    value = 0
    rank = 0
    global tournament_active
    type("Warning ⚠️: You cannot come out of the tournament until it ends. ")
    warning = input("Are you sure you want to go fishing(yes/no): ").lower()
    clear()
    if warning == "yes":
        stats["Gold"] -= 1000
        tournament_active = [True]
        type("Welcome to the World Fishing Tournament at Sapphire Docks.")
        time.sleep(1)
        clear()
        tutorial = input("Enter tutorial? Type yes or no: ").lower()
        clear()
        if tutorial == "yes":
            type("The is a 2 minute tournament where you catch fish and get points based on the size of the fish. The higher the tier, the more points you get. ")
            time.sleep(0.5)
            type("There are 5 tiers of fish. Tier 1 is the easiest and Tier 5 is the hardest. ")
            time.sleep(0.5)
            type("There are 5 players in each tournament. First place would be rewarded with rare loot, rare items, one free enchantment, and 10 levels. Second place would be rewarded with common loot, items, and 8 levels. Third place would gain 20% of their current gold and 5 levels. Last place would lose 10% gold, and potentially one of their items. ")
            time.sleep(0.5)
            type("4th place recieve 5% of their current gold and 30% of their Max EXP.")
            hi = input("Press Enter to continue: ")
            if hi is not None:
                time.sleep(0)
            else:
                time.sleep(0)
        clear()
        type("First, you need to gear up.")
        time.sleep(1)
        clear()
        rod = {}
        lure = {}
        print("Here are your options: \n")
        time.sleep(0.5)
        print("\t1. *Beginner Pack* | Cost: 500 Gold")
        time.sleep(0.1)
        print("\t\tBeginner’s Rod")
        time.sleep(0.1)
        print("\t\tBeginner's Lure | Count: 25\n")
        time.sleep(0.1)
        print("\t2. *Noob Slayer Starter Kit* | Cost: 5000 Gold")
        time.sleep(0.1)
        print("\t\tSloppy Stick Rod")
        time.sleep(0.1)
        print("\t\tFlimsy Flop Lure | Count: 40\n")
        time.sleep(0.1)
        print("\t3. *Legendary Loony Lunker Loot* | Cost: 10000 Gold")
        time.sleep(0.1)
        print("\t\tDragon’s Tongue Rod")
        time.sleep(0.1)
        print("\t\tNuclear Nibble Lure | Count: 80\n")
        time.sleep(0.1)
        pack = int(input("Which pack do you want to buy ( 1, 2, 3 ): "))
        clear()
        if pack == 1:
            if stats["Gold"] >= 500:
                stats["Gold"] -= 500
                rod = {"Name": "Beginner’s Rod", "LCK": 1}
                lure = {"Name": "Beginner's Lure", "Count": 25, "LCK": 1}
            else:
                broke = True
        if pack == 2:
            if stats["Gold"] >= 5000:
                stats["Gold"] -= 5000
                rod = {"Name": "Sloppy Stick Rod", "LCK": 2}
                lure = {"Name": "Flimsy Flop Lure", "Count": 40, "LCK": 2}
            else:
                broke = True
        if pack == 3:
            if stats["Gold"] >= 10000:
                stats["Gold"] -= 10000
                rod = {"Name": "Dragon’s Tongue Rod", "LCK": 3}
                lure = {"Name": "Nuclear Nibble Lure", "Count": 80, "LCK": 3}
            else:
                broke = True
        if broke:
            print("You don't have enough money to buy this pack!")
            time.sleep(1.5)
        else:
            print(f"You have {lure['Count']} lures.")
            add = input("Do you want to buy more lure(yes/no): ")
            clear()
            if add == "yes":
                cnt = int(input("How many multipliers do you want to buy(Each one doubles your lure): "))
                clear()
                cost = 100
                for i in range(cnt):
                    cost *= 2
                if cost > stats["Gold"]:
                    print("You don't have enough money to buy this!")
                    time.sleep(1)
                    clear()
                    broke = True
                else:
                    buy = input(f"It will cost you {cost} gold. Are you sure you want to buy(yes/no): ")
                    if buy == "yes":
                        for i in range(cnt):
                            lure["Count"] *= 2
                        print(f"You now have {lure['Count']} lures.")
            if broke:
                print("You don't have enough money to buy this pack!")
                time.sleep(1.5)
            else:
                players = []
                clear()
                for i in range(5):
                    prefix = random.choice(prefixes)
                    middle = random.choice(middles)
                    suffix = random.choice(suffixes)
                    player_name = f"{prefix}{middle}{suffix}"
                    players.append({"name": player_name, "total_value": 0})
                    print("Opponent: ", player_name)
                    time.sleep(0.1)
                clear()
                time.sleep(1)
                print("Ready?")
                time.sleep(1)
                clear()
                print("Set")
                time.sleep(1)
                clear()
                print("Fish!")
                clear()
                for p in players:
                    threading.Thread(target=npc_fishing, args=(p,), daemon=True).start()
                threading.Thread(target=timer_loop, args=(120, )).start()

                while tournament_active[0]:
                    print("Your lure: ", lure["Count"])
                    fish = input("Type 1 to cast your line | Type 2 to view ranking (Tho i suggest not waste time): ")
                    if fish == "1":
                        if lure["Count"] == 0:
                            print("You are out of lures!")
                            time.sleep(1)
                            clear()
                            continue
                        rarity = random.randint(1, 100)
                        if rarity <= 60 - (((rod["LCK"] - 1) * 5) + (lure["LCK"] - 1) * 5):
                            fish = random.randint(1, 50)
                            fish_name = tier1_fish[fish - 1][0]
                            fish_value = tier1_fish[fish - 1][1]
                        elif rarity <= 80 - (((rod["LCK"] - 1) * 5) + (lure["LCK"] - 1) * 5):
                            fish = random.randint(1, 50)
                            fish_name = tier2_fish[fish - 1][0]
                            fish_value = tier2_fish[fish - 1][1]
                        elif rarity <= 87 - (((rod["LCK"] - 1) * 5) + (lure["LCK"] - 1) * 5):
                            fish = random.randint(1, 50)
                            fish_name = tier3_fish[fish - 1][0]
                            fish_value = tier3_fish[fish - 1][1]
                        elif rarity <= 98 - (((rod["LCK"] - 1) * 5) + (lure["LCK"] - 1) * 5):
                            fish = random.randint(1, 45)
                            fish_name = tier4_fish[fish - 1][0]
                            fish_value = tier4_fish[fish - 1][1]
                        else:
                            fish = random.randint(1, 40)
                            fish_name = tier5_fish[fish - 1][0]
                            fish_value = tier5_fish[fish - 1][1]
                        lure["Count"] -= 1
                        type(f"You caught a {fish_name} worth {fish_value} points!")
                        time.sleep(1)
                        clear()
                        value += fish_value
                        print("Your Points: ", value)
                        time.sleep(1)
                        clear()
                    elif fish == "2":
                        for p in players:
                            print(f"{p['name']}: {p['total_value']} gold")
                        input("Press Enter to continue: ")
                        clear()
                players_with_you = players + [{"name": "You", "total_value": value}]
                ranked = sorted(players_with_you, key=lambda x: x["total_value"], reverse=True)
                for i in range(0, 5):
                    if ranked[i]["name"] == "You":
                        rank = i + 1
                if rank == 1:
                    type("You got first place!!!")
                    time.sleep(1)
                    clear()
                    type("Your loot: ")
                    time.sleep(0.1)
                    print("\t1 Celestium Prism")
                    time.sleep(0.1)
                    item = random.choice(["weapon", "helmet", "chestplate", "leggings", "boots"])
                    if item == "weapon":
                        item = random.choice(elite_swords)
                    elif item == "helmet":
                        item = random.choice(helmets)
                    elif item == "chestplate":
                        item = random.choice(chestplates)
                    elif item == "leggings":
                        item = random.choice(leggings)
                    elif item == "boots":
                        item = random.choice(boots)
                    print(f"\t{item}")
                    time.sleep(0.1)
                    print("\t50000 Gold")
                    time.sleep(0.1)
                    print("\t10 Levels")
                    time.sleep(4.5)
                    stats["Celestium Prism"] += 1
                    stats["Backpack"].append(item)
                    stats["Gold"] += 50000
                    stats["Lvl"] += 10
                    stats["Max EXP"] += 200
                elif rank == 2:
                    type("You got second place!!!")
                    time.sleep(1)
                    clear()
                    type("Your loot: ")
                    time.sleep(0.1)
                    print("\t10000 Gold")
                    time.sleep(0.1)
                    item = random.choice(["weapon", "helmet", "chestplate", "leggings", "boots"])
                    if item == "weapon":
                        item = random.choice(swords)
                    elif item == "helmet":
                        item = random.choice(helmets)
                    elif item == "chestplate":
                        item = random.choice(chestplates)
                    elif item == "leggings":
                        item = random.choice(leggings)
                    elif item == "boots":
                        item = random.choice(boots)
                    print(f"\t{item}")
                    time.sleep(0.1)
                    print("\t8 Levels")
                    time.sleep(3)
                    stats["Gold"] += 10000
                    stats["Backpack"].append(item)
                    stats["Lvl"] += 8
                    stats["Max EXP"] += 160
                elif rank == 3:
                    type("You got third place!!!")
                    time.sleep(1)
                    clear()
                    type("Your loot: ")
                    time.sleep(0.1)
                    print(f"\t{stats['Gold'] * 0.2} Gold")
                    time.sleep(0.1)
                    print("\t5 Levels")
                    time.sleep(2)
                    stats["Gold"] *= 0.2
                    stats["Lvl"] += 5
                    if "Max EXP" not in stats:
                        stats["Max EXP"] = 20  # Initialize with default value
                    stats["Max EXP"] += 100
                elif rank == 4:
                    type("You got fourth place!!!")
                    time.sleep(1)
                    clear()
                    type("Your loot: ")
                    time.sleep(0.1)
                    print(f"\t{stats['Gold'] * 0.05} Gold")
                    time.sleep(0.1)
                    print(f"\t{stats['Max EXP'] * 0.3} EXP")
                    time.sleep(2)
                    stats["Gold"] *= 0.05
                    stats["EXP"] += stats["Max EXP"] * 0.3
                    if stats["EXP"] >= stats["Max EXP"]:
                        stats["Lvl"] += 1
                        stats["Max EXP"] += 20
                        stats["EXP"] -= stats["Max EXP"]
                        type("Level up!!!")
                        up = input("What do you want to improve(HP, ATK, DEF, SP, CRIT): ").lower()
                        if up == "hp":
                            stats["HP"] += 200
                        elif up == "atk":
                            stats["STR"] += 10
                        elif up == "def":
                            stats["DEF"] += 20
                        elif up == "sp":
                            stats["SP"] += 2.5
                        elif up == "crit":
                            stats["Crit"] += 0.5
                else:
                    type("You lost...")
                    time.sleep(1)
                    clear()
                    type(f"You lost {stats['Gold'] * 0.1} Gold")
                    time.sleep(1)
                    stats['Gold'] -= stats['Gold'] * 0.1
                    chance = random.randint(1, 100)
                    if chance <= 25:
                        if stats["Backpack"] != []:
                            item = random.choice(stats["Backpack"])
                            type(f"You lost {item}")
                            stats["Backpack"].remove(item)
                    time.sleep(1)
                    clear()

    else:
        type("Exiting the tournament...")
        time.sleep(1)

def shop():
    type("Welcome to the shop!")
    time.sleep(1)
    clear()
    start("Shop", "Loading", 3, 7.5)
    print("\n")
    print("1. Buy")
    time.sleep(0.5)
    print("2. Sell")
    time.sleep(0.5)
    print("\n")
    shop = input("What would you like to do: ").lower()
    clear()
    if shop == "2" or shop == "sell":
        for index, item in enumerate(stats["Backpack"], start=1):
            print(f"Item {index}:")
            for key, value in item.items():
                print(f"   {key}: {value}")
        sell = input("What would you like to sell(Type 1 if you want to leave) (Capitalization counts): ")
        clear()
        if sell == "1":
            pass
        else:
            found = False
            for item in stats["Backpack"]:
                if item.get("Name") == sell:
                    found = True
                    break
            if found:
                print(f"🎉 {sell} found!")
                cost = 0
                for item in stats["Backpack"]:
                    if item["Name"] == sell:
                        cost = item["Cost"]
                        break
                lower = cost / 20
                upper = cost / 10
                cost_range = random.uniform(lower, upper)
                print(cost_range)
                time.sleep(1)
                clear()
                for item in stats["Backpack"]:
                    if item.get("Name") == sell:
                        print(f"📦 Stats for {sell}:")
                        time.sleep(0.1)
                        for key, value in item.items():
                            time.sleep(0.1)
                            print(f"   {key}: {value}")
                        break
                price = int(input(f"Enter the price you want to sell {sell} for: "))
                cost = 0
                for item in stats["Backpack"]:
                    if item["Name"] == sell:
                        cost = item["Cost"]
                        break
                if price > cost + cost_range:
                    print(f"The shopkeeper sells {sell} for {cost / 2} gold because you put a price that is higher than the range. 😭😭😭 Caught in 4K moments 👀")
                    time.sleep(2)
                    clear()
                    stats["Gold"] += cost / 2
                    stats["Backpack"] = [
                        item for item in stats["Backpack"] if item["Name"] != sell
                    ]
                else:
                    print(f"The shopkeeper sells {sell} for {price} gold. 🎉🎉🎉")
                    time.sleep(1)
                    clear()
                    stats["Gold"] += price
                    stats["Backpack"] = [
                        item for item in stats["Backpack"] if item["Name"] != sell
                    ]
            else:
                print(f"{sell} not found!")
                time.sleep(1)
                clear()
    elif shop == "1" or shop == "buy": 
        print("1. Normal/Recruit Swords\n")
        time.sleep(0.1)
        print("2. Elite Swords\n")
        time.sleep(0.1)
        print("3. Potions\n")
        time.sleep(0.1)
        print("4. Armor\n")
        time.sleep(0.1)
        section = input("Which section would you like to go to: ").lower()
        clear()
        if section == "1" or section == "normal" or section == "recruit" or section == "normal/recruit" or section == "2" or section == "elite" or section == "elite swords":
            start("Swords", "Loading", 3, 7.5)
        if section == "1" or section == "normal" or section == "recruit" or section == "normal/recruit":
            for i in swords:
                start(i["Name"], "Analysing", 1, 2)
                print("\n\n")
                print("Name: ", i["Name"], "\n")
                time.sleep(0.25)
                print("ATK Mutiplier: ", i["ATK"], "\n")
                time.sleep(0.25)
                print("SP Mutiplier: ", i["SP"], "\n")
                time.sleep(0.25)
                print("Crit Mutiplier: ", i["Crit"], "\n")
                time.sleep(0.25)
                print("\tCost:", i["Cost"], "\n")
                time.sleep(0.25)
                print("\n\n")
                time.sleep(0.25)
                purchase = input("Would you like to buy this sword(yes/no/type 1 if you want to leaave the shop): ").lower()
                clear()
                if purchase == "yes":
                    start(i["Name"], "Purchasing", 1, 3)
                    poor = False
                    if stats["Gold"] >= i["Cost"]:
                        stats["Gold"] -= i["Cost"]
                        stats["Backpack"].append(i)
                        type("Purchase Successful!")
                        time.sleep(1)
                        clear()
                    else:
                        type("You do not have enough gold to buy this sword!💀💀💀💀💀👀👀👀😩😩😩😩🥺🥺🥺🥺🥺🥺")
                        time.sleep(1)
                        poor = True
                        break
                    if not poor:
                        start(i["Name"], "Inserting", 3, 5)
                        clear()
                        break
                elif purchase == "no":
                    continue
                else:
                    break

        if section == "2" or section == "elite" or section == "elite swords":
            for sword in elite_swords:
                start(sword["Name"], "Analysing", 2, 4)
                clear()
                print("\n\n")
                print("Name: ", sword["Name"], "\n")
                time.sleep(0.25)
                print("ATK Mutiplier: ", sword["ATK"], "\n")
                time.sleep(0.25)
                print("SP Mutiplier: ", sword["SP"], "\n")
                time.sleep(0.25)
                print("Crit Mutiplier: ", sword["Crit"], "\n")
                time.sleep(0.25)
                print("\tCost:", sword["Cost"], "\n")
                time.sleep(0.25)
                print("\n\n")
                time.sleep(0.25)
                purchase = input("Would you like to buy this sword(yes/no/type 1 if you want to leave the shop): ").lower()
                clear()
                if purchase == "yes":
                    start(sword["Name"], "Purchasing", 1, 2)
                    poor = False
                    if stats["Gold"] >= sword["Cost"]:
                        stats["Gold"] -= sword["Cost"]
                        stats["Backpack"].append(sword)
                        type("Purchase Successful!")
                        time.sleep(1)
                        clear()
                    else:
                        type("You do not have enough gold to buy this sword!💀💀💀💀💀👀👀👀😩😩😩😩🥺🥺🥺🥺🥺🥺")
                        time.sleep(1)
                        poor = True
                        break
                    if not poor:
                        start(sword["Name"], "Inserting", 1, 3)
                        break
                elif sword == "no":
                    continue
                else:
                    break

        if section == "3" or section == "potions":
            tier = 1
            start("Potions", "Loading", 3, 7.5)
            start("Potions", "Analysing", 3, 7.5)
            clear()
            for i in potions:
                print("\n")
                print("Name: ", i["Name"], "\n")
                time.sleep(0.125)
                print("Effect: ", i["Effect"], "\n")
                time.sleep(0.125)
                print("Tier: ", i["Tier"], "\n")
                time.sleep(0.125)
                print("\tCost: ", i["Cost"], "\n")
                time.sleep(0.125)
                print("\n")
                time.sleep(0.125)
            potion = input("Enter which potion you want to purchase(Type 1 to leave): ")
            small_words = {'and', 'or', 'the', 'of', 'in', 'on', 'at', 'to', 'for', 'by', 'with', 'a', 'an'}
            words = potion.split()
            result = []
            for i, word in enumerate(words):
                if i == 0 or i == len(words) - 1 or word.lower() not in small_words:
                    result.append(word.capitalize())
                else:
                    result.append(word.lower())

            title_cased = ' '.join(result)
            potion = title_cased
            if potion == "1":
                 pass
            else:
                for i in potions:
                    start(potion, "Searching", 1, 2)
                    clear()
                    effect = 0
                    cost = 0
                    if potion == i["Name"]:
                        print("Potion Found!🎯")
                        time.sleep(1)
                        clear()
                        if potion == "Potion of Healing":
                            type("The higher the tier, the more effective it is but the more it costs.")
                            time.sleep(0.5)
                            tier = int(input("Enter the tier of the potion you want to purchase(1, 2, 3, etc): "))
                            print()
                            time.sleep(0.5)
                            print("Potion of Healing at Tier ", tier, " costs ", i["Cost"] + ((tier - 1) * 50), "and heals for", i["Effect"] + ((tier - 1) * 100))
                            cost = (tier - 1) * 50
                            effect = (tier - 1) * 100
                            time.sleep(2)
                            clear()
                        else:
                            type("The higher the tier, the more effective it is but the more it costs.")
                            time.sleep(0.5)
                            tier = int(input("Enter the tier of the potion you want to purchase(1, 2, 3, etc): "))
                            print()
                            time.sleep(0.5)
                            print("Potion of ", potion, " at Tier ", tier, " costs ", i["Cost"] + ((tier - 1) * 25), "and increases your ", potion, " by", i["Effect"] + ((tier - 1) * 0.1))
                            cost = (tier - 1) * 25
                            effect = (tier - 1) * 0.1
                            time.sleep(2)
                        time.sleep(0.65)
                        clear()
                        start(potion, "Purchasing", 1, 2)
                        clear()
                        poor = False
                        if stats["Gold"] >= i["Cost"] + ((tier - 1) * 50):
                            stats["Gold"] -= i["Cost"] + ((tier - 1) * 50)
                            stats["Backpack"].append(i)
                            i["Effect"] += effect
                            i["Tier"] = tier
                            i["Cost"] += cost
                            type("Purchase Successful!")
                            time.sleep(1)
                            clear()
                        else:
                            type("You do not have enough gold to buy this potion!💀💀💀💀💀👀👀👀😩😩😩😩🥺🥺🥺🥺🥺🥺")
                            time.sleep(1)
                            poor = True
                            break
                        if not poor:
                            start(potion, "Inserting", 1, 3)
                            clear()
                            type("Insertion Completed!")
                            time.sleep(1)
                            clear()
                            break
                    else:
                        print(potion, " was not found!😭😭😭")
                        time.sleep(2)
                        break

        if section == "4" or section == "armor":
            print("1. Helmets\n")
            time.sleep(0.1)
            print("2. Chestplates\n")
            time.sleep(0.1)
            print("3. Leggings\n")
            time.sleep(0.1)
            print("4. Boots\n")
            time.sleep(0.1)
            armor = input("What would you like to buy: ").lower()
            clear()
            if armor == "1" or armor == "helmets":
                start("Helmets", "Loading", 3, 7.5)
                clear()
                for i in helmets:
                    start(i["Name"], "Analysing", 2, 4)
                    clear()
                    print("\n\n")
                    print("Name: ", i["Name"], "\n")
                    time.sleep(0.25)
                    print("DEF Mutiplier: ", i["DEF"], "\n")
                    time.sleep(0.25)
                    print("SP Mutiplier: ", i["SP"], "\n")
                    time.sleep(0.25)
                    print("\tCost:", i["Cost"], "\n")
                    time.sleep(0.25)
                    print("\n\n")
                    time.sleep(0.25)
                    purchase = input("Would you like to buy this helmet(yes/no/type 1 if you want to leave shop): ").lower()
                    clear()
                    if purchase == "yes":
                        start(i["Name"], "Purchasing", 1, 2)
                        poor = False
                        if stats["Gold"] >= i["Cost"]:
                            stats["Gold"] -= i["Cost"]
                            stats["Backpack"].append(i)
                            type("Purchase Successful!")
                            time.sleep(1)
                            clear()
                        else:
                            type("You do not have enough gold to buy this helmet!💀💀💀💀💀👀👀👀😩😩😩😩🥺🥺🥺🥺🥺🥺")
                            time.sleep(1)
                            poor = True
                            break
                        if not poor:
                            start(i["Name"], "Inserting", 1, 3)
                            clear()
                            type("Insertion Completed!")
                            time.sleep(1)
                            clear()
                            break
                    elif purchase == "no":
                        continue
                    else:
                        break
            if armor == "2" or armor == "chestplates":
                start("Chestplates", "Loading", 3, 7.5)
                clear()
                for i in chestplates:
                    start(i["Name"], "Analysing", 2, 3)
                    clear()
                    print("\n\n")
                    print("Name: ", i["Name"], "\n")
                    time.sleep(0.25)
                    print("DEF Mutiplier: ", i["DEF"], "\n")
                    time.sleep(0.25)
                    print("SP Mutiplier: ", i["SP"], "\n")
                    time.sleep(0.25)
                    print("\tCost:", i["Cost"], "\n")
                    time.sleep(0.25)
                    print("\n\n")
                    time.sleep(0.25)
                    purchase = input("Would you like to buy this Chestplate(yes/no/type 1 if you want to leave shop): ").lower()
                    clear()
                    if purchase == "yes":
                        start(i["Name"], "Purchasing", 1, 2)
                        poor = False
                        if stats["Gold"] >= i["Cost"]:
                            stats["Gold"] -= i["Cost"]
                            stats["Backpack"].append(i)
                            type("Purchase Successful!")
                            time.sleep(1)
                            clear()
                        else:
                            type("You do not have enough gold to buy this chestplate!💀💀💀💀💀👀👀👀😩😩😩😩🥺🥺🥺🥺🥺🥺")
                            time.sleep(1)
                            poor = True
                            break
                        if not poor:
                            start(i["Name"], "Inserting", 1, 3)
                            clear()
                            type("Insertion Completed!")
                            time.sleep(1)
                            clear()
                            break
                    elif purchase == "no":
                        continue
                    else:
                        break
            if armor == "3" or armor == "leggings":
                start("Leggings", "Loading", 3, 7.5)
                clear()
                for i in leggings:
                    start(i["Name"], "Analysing", 2, 3)
                    clear()
                    print("\n\n")
                    print("Name: ", i["Name"], "\n")
                    time.sleep(0.25)
                    print("DEF Mutiplier: ", i["DEF"], "\n")
                    time.sleep(0.25)
                    print("SP Mutiplier: ", i["SP"], "\n")
                    time.sleep(0.25)
                    print("\tCost:", i["Cost"], "\n")
                    time.sleep(0.25)
                    print("\n\n")
                    time.sleep(0.25)
                    purchase = input("Would you like to buy this legging(yes/no/type 1 if you want to leave shop): ").lower()
                    clear()
                    if purchase == "yes":
                        start(i["Name"], "Purchasing", 1, 2)
                        poor = False
                        if stats["Gold"] >= i["Cost"]:
                            stats["Gold"] -= i["Cost"]
                            stats["Backpack"].append(i)
                            type("Purchase Successful!")
                            time.sleep(1)
                            clear()
                        else:
                            type("You do not have enough gold to buy this legging!💀💀💀💀💀👀👀👀😩😩😩😩🥺🥺🥺🥺🥺🥺")
                            time.sleep(1)
                            poor = True
                            break
                        if not poor:
                            start(i["Name"], "Inserting", 1, 3)
                            clear()
                            break
                    elif purchase == "no":
                        continue
                    else:
                        break
            if armor == "4" or armor == "boots":
                start("Boots", "Loading", 3, 7.5)
                clear()
                for i in boots:
                    start(i["Name"], "Analysing", 2, 3)
                    clear()
                    print("\n\n")
                    print("Name: ", i["Name"], "\n")
                    time.sleep(0.25)
                    print("DEF Mutiplier: ", i["DEF"], "\n")
                    time.sleep(0.25)
                    print("SP Mutiplier: ", i["SP"], "\n")
                    time.sleep(0.25)
                    print("\tCost:", i["Cost"], "\n")
                    time.sleep(0.25)
                    print("\n\n")
                    time.sleep(0.25)
                    purchase = input("Would you like to buy this boot(yes/no/type 1 if you want to leave shop): ").lower()
                    clear()
                    if purchase == "yes":
                        start(i["Name"], "Purchasing", 1, 2)
                        poor = False
                        if stats["Gold"] >= i["Cost"]:
                            stats["Gold"] -= i["Cost"]
                            stats["Backpack"].append(i)
                            type("Purchase Successful!")
                            time.sleep(1)
                            clear()
                        else:
                            type("You do not have enough gold to buy this boot!💀💀💀💀💀👀👀👀😩😩😩😩🥺🥺🥺🥺🥺🥺")
                            time.sleep(1)
                            poor = True
                            break
                        if not poor:
                            start(i["Name"], "Inserting", 1, 3)
                            clear()
                            type("Insertion Completed!")
                            time.sleep(1)
                            clear()
                            break
                    elif purchase == "no":
                        continue
                    else:
                        break   

def goldspire_market(): 
    if stats["Lvl"] <= 24:
        type("You need to be level 25 to enter the Goldspire Market!")
        time.sleep(2)
    else:
        type("Welcome to the Goldspire Market!")
        time.sleep(1)
        clear()
        start("Goldspire Market", "Loading", 1, 4)
        clear()
        type("Here you can trade for exclusive items and trade with other players!")
        print()
        time.sleep(0.5)
        type("\t1. Browse our exclusive items")
        print()
        time.sleep(0.1)
        type("\t2. World Trading")
        print()
        time.sleep(0.1)
        choice = int(input("Enter your choice (a number): "))
        clear()
        if choice == 1:
            print("Exclusive items: ")
            time.sleep(0.1)
            print("*****************************")
            time.sleep(0.1)
            print("1. Titan’s Heartplate\n")
            time.sleep(0.1)
            print("2. Dragonbone Bulwark\n")
            time.sleep(0.1)
            print("3. Crownbreaker Halberd\n")
            time.sleep(0.1)
            print("4. Heart of the Colossus")
            time.sleep(0.1)
            print("*****************************")
            type("Warning ⚠️: Your original chestplate/weapon will be replaced with the new one. \n")
            item = int(input("Enter the number of the item you want to buy(Type 1 if to leave): "))
            clear()
            if item == 1:
                if stats["Dragonite"] < 3 or stats["Gold"] < 10000000 or stats["Diamond"] < 5:
                    type("You do not have enough dragonite, gold, diamond to buy this item!")
                    time.sleep(1.5)
                    clear()
                else:
                    type("Titan’s Heartplate")
                    time.sleep(0.1)
                    print("*****************************")
                    time.sleep(0.1)
                    print("DEF: 10")
                    time.sleep(0.1)
                    print("SP: 1.5")
                    time.sleep(0.1)
                    print("Cost: 3 Dragonite, 5 Diamond, 10000000 Gold")
                    time.sleep(0.1)
                    print("*****************************")
                    buy = input("Do you want to buy this item(yes/no): ").lower()
                    clear()
                    if buy == "yes":
                        start("Titan’s Heartplate", "Purchasing", 1, 3)
                        clear()
                        stats["Dragonite"] -= 3
                        stats["Gold"] -= 10000000
                        stats["Diamond"] -= 5
                        stats["Chestplate"] = {"Name": "Titan’s Heartplate", "ATK": 5, "DEF": 6, "SP": 3, "MAX DUR": 100000000000, "DUR": 100000000000}
                    else:
                        pass
            elif item == 2:
                if stats["Dragonite"] < 1 or stats["Gold"] < 50000000 or stats["Diamond"] < 3:
                    type("You do not have enough dragonite, gold, diamond to buy this item!")
                    time.sleep(1.5)
                    clear()
                else:
                    type("Dragonbone Bulwark")
                    time.sleep(0.1)
                    print("*****************************")
                    time.sleep(0.1)
                    print("DEF: 8")
                    time.sleep(0.1)
                    print("ATK: 5")
                    time.sleep(0.1)
                    print("SP: 5")
                    time.sleep(0.1)
                    print("Cost: 2 Dragonite, 3 Diamond, 50000000 Gold")
                    time.sleep(0.1)
                    print("*****************************")
                    buy = input("Do you want to buy this item(yes/no): ").lower()
                    clear()
                    if buy == "yes":
                        start("Dragonbone Bulwark", "Purchasing", 1, 3)
                        clear()
                        stats["Dragonite"] -= 1
                        stats["Gold"] -= 50000000
                        stats["Diamond"] -= 3
                        stats["Chestplate"] = {"Name": "Dragonbone Bulwark", "ATK": 5, "DEF": 8, "SP": 5, "MAX DUR": 100000000000, "DUR": 100000000000}
                    else:
                        pass
            elif item == 3:
                if stats["Dragonite"] < 5 or stats["Gold"] < 2000000 or stats["Diamond"] < 10:
                    type("You do not have enough dragonite, gold, diamond to buy this item!")
                    time.sleep(1.5)
                    clear()
                else:
                    type("Crownbreaker Halberd")
                    time.sleep(0.1)
                    print("*****************************")
                    time.sleep(0.1)
                    print("ATK: 10")
                    time.sleep(0.1)
                    print("SP: 1.5")
                    time.sleep(0.1)
                    print("Cost: 5 Dragonite, 10 Diamond, 2000000 Gold")
                    time.sleep(0.1)
                    print("*****************************")
                    buy = input("Do you want to buy this item(yes/no): ").lower()
                    clear()
                    if buy == "yes":
                        start("Crownbreaker Halberd", "Purchasing", 1, 3)
                        clear()
                        stats["Dragonite"] -= 5
                        stats["Gold"] -= 2000000
                        stats["Diamond"] -= 10
                        stats["Weapon"] = {"Name": "Crownbreaker Halberd", "ATK": 10, "DEF": 5, "SP": 2, "MAX DUR": 100000000000, "DUR": 100000000000}
                    else:
                        pass
            else:
                if stats["Dragonite"] < 15 or stats["Gold"] < 1000000000 or stats["Diamond"] < 30:
                    type("You do not have enough dragonite, gold, diamond to buy this item!")
                    time.sleep(1.5)
                    clear()
                else:
                    type("Heart of the Colossus")
                    time.sleep(0.1)
                    print("*****************************")
                    time.sleep(0.1)
                    print("ATK: 10")
                    time.sleep(0.1)
                    print("DEF: 10")
                    time.sleep(0.1)
                    print("SP: 10")
                    time.sleep(0.1)
                    print("Cost: 15 Dragonite, 30 Diamond, 1000000000 Gold")
                    time.sleep(0.1)
                    print("*****************************")
                    buy = input("Do you want to buy this item(yes/no): ").lower()
                    clear()
                    if buy == "yes":
                        start("Heart of the Colossus", "Purchasing", 1, 3)
                        clear()
                        stats["Dragonite"] -= 15
                        stats["Gold"] -= 1000000000
                        stats["Diamond"] -= 30
                        stats["Weapon"] = {"Name": "Heart of the Colossus", "ATK": 10, "DEF": 10, "SP": 10, "MAX DUR": 100000000000, "DUR": 100000000000}

        else:
            option1 = 0
            while option1 != 1:
                print("World Trading:\n")
                time.sleep(0.1)
                all_players = {}
                for _ in range(5):
                    status = random.choice(["In Main Menu", "In Shop", "Repairing", "Enchanting", "Reviewing tips cause hes a nooooooob."])
                    times = random.randint(0, 5)

                    for i in range(times):
                        dots = "." * ((i % 3) + 1)  
                        print(dots.ljust(3), end='\r')  
                        time.sleep(0.4)

                    print("   ", end='\r')

                    hi = random.choice(["Yes", "No"])
                    prefix = random.choice(prefixes)
                    middle = random.choice(middles)
                    suffix = random.choice(suffixes)
                    if hi == "Yes":
                        id = random.randint(0, 999)
                        player_name = f"{prefix}{middle}{suffix}_{id}"
                    else:
                        player_name = f"{prefix}{middle} {suffix}"
                    ID = random.randint(0, 100000)
                    lvl = random.randint(stats["Lvl"] - 10, stats["Lvl"] + 10)

                    all_players[ID] = {
                        "name": player_name,
                        "status": status,
                        "lvl": lvl
                    }

                    print("---------------------------------------------------------------------")
                    print(f"{player_name} | Lvl: {lvl} | ID: {ID} | Status: {status}")
                    print("---------------------------------------------------------------------\n")
                    time.sleep(0.5)

                player = int(input("Enter the ID of the player you want to trade with(Type 1 if to leave): "))
                chestplate = 0
                trade_finish = 0
                diamondss = 0
                dragonites = 0
                clear()
                time.sleep(0.5)
                if player == 1:
                    break
                if player in all_players:
                    if all_players[player]["status"] == "In Main Menu":
                        print("Player is in the main menu. Max: 5 seconds")
                        type("Requesting trade...")
                        accept = random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Expire", "Expire"])
                        if accept == "No":
                            time.sleep(random.uniform(0, 2))
                        elif accept == "Yes":
                            time.sleep(random.uniform(0, 2))
                        else:
                            time.sleep(5)
                        clear()
                    elif all_players[player]["status"] == "In Shop":
                        print(f"Player {all_players[player]['name']} is in the shop.")
                        type("It might take longer for the player to accept your trade because they are shopping. Max: 10 seconds")
                        type("Requesting trade...")
                        accept = random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Expire", "Expire"])
                        if accept == "No":
                            time.sleep(random.uniform(3, 6))
                        elif accept == "Yes":
                            time.sleep(random.uniform(4, 7))
                        elif accept == "Expire":
                            time.sleep(10)
                        clear()
                    elif all_players[player]["status"] == "Repairing":
                        print(f"Player {all_players[player]['name']} is repairing.")
                        type("It might take longer for the player to accept your trade because they are repairing. Max: 12 seconds")
                        type("Requesting trade...")
                        accept = random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Expire", "Expire"])
                        if accept == "No":
                            time.sleep(random.uniform(4, 7))
                        elif accept == "Yes":
                            time.sleep(random.uniform(5, 10))
                        elif accept == "Expire":
                            time.sleep(12)
                        clear()
                    elif all_players[player]["status"] == "Enchanting":
                        print(f"Player {all_players[player]['name']} is enchanting. Max: 6 seconds")
                        type("Requesting trade...")
                        accept = random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Expire", "Expire"])
                        if accept == "No":
                            time.sleep(random.uniform(0, 3))
                        elif accept == "Yes":
                            time.sleep(random.uniform(1, 4))
                        elif accept == "Expire":
                            time.sleep(6)
                        clear()
                    else:
                        print(f"Player {all_players[player]['name']} is reviewing tips. Max: 10 seconds")
                        type("Requesting trade...")
                        accept = random.choice(["Yes", "Yes", "Yes", "Yes", "Yes", "No", "No", "Expire", "Expire"])
                        if accept == "No":
                            time.sleep(random.uniform(3, 6))
                        elif accept == "Yes":
                            time.sleep(random.uniform(4, 7))
                        elif accept == "Expire":
                            time.sleep(10)
                        clear()

                    if accept == "Yes" or accept == "No" or accept == "Expire":
                        chat("Trade accepted!")
                        time.sleep(1)
                        clear()
                        chance = random.choice([1, 2, 3])
                        if chance == 1:
                            chat(f"Hello, {stats['Name']}")
                        elif chance == 2:
                            chat(f"How are you doing, {stats['Name']}?")
                        elif chance == 3:
                            chat(f"Nice to meet you, {stats['Name']}")
                        response = input("\nType anything to continue: ")
                        clear_last_line()
                        print(f"\t\t\t\t\t\t{response}\n")
                        chance = random.choice([1, 2])
                        if chance == 1:
                            chat("Cool! I recieved a message that you wanted to trade with me. ")
                        elif chance == 2:
                            chat("I'm glad you wanted to trade with me! Hope you have decent loot!")
                        response = input("\nType anything to continue: ")
                        clear_last_line()
                        print(f"\t\t\t\t\t\t{response}\n")
                        chance = random.choice([1, 2, 3, 4])
                        if chance == 1:
                            chat("Alright well let's get started. I need to go grind in the Rotfang depths for some Celestium Prisms. ")
                        elif chance == 2:
                            chat("Here, have a look at my inventory. Make it quick. I need to go repair my armor before I go destroy some noobs in the arena.")
                        elif chance == 3:
                            chat("Whoooooo! let's get started on this tradin' ")
                        elif chance == 4:
                            chat("😿Meow")
                        clear()
                        chance = random.choice([1, 3, 4])
                        if chance == 1:
                            weapons = all_players[player]["lvl"] // 15
                        elif chance == 3:
                            weapons = all_players[player]["lvl"] // 15 + 1
                        else:
                            weapons = 0

                        chance = random.choice([1, 3, 4])
                        if chance == 1:
                            shields_num = all_players[player]["lvl"] // 25 
                        elif chance == 3:
                            shields_num = all_players[player]["lvl"] // 25 + 1
                        else:
                            shields_num = 0

                        chance = random.choice([1, 3, 4])
                        if chance == 1:
                            helmets_num = all_players[player]["lvl"] // 30
                        elif chance == 3:
                            helmets_num = all_players[player]["lvl"] // 30 + 1
                        else:
                            helmets_num = 0

                        chance = random.choice([1, 3, 4])
                        if chance == 1:
                            chestplate = all_players[player]["lvl"] // 30 
                        elif chance == 3:
                            chance = random.choice([1, 2])
                            if chance == 1:
                                chestplate = all_players[player]["lvl"] // 30 + 1
                            if chance == 2:
                                chestplate = all_players[player]["lvl"] // 30
                        else:
                            chestplate = 0

                        chance = random.choice([1, 3, 4])
                        if chance == 1:
                            legging = all_players[player]["lvl"] // 30 
                        elif chance == 3:
                            legging = all_players[player]["lvl"] // 30 + 1
                        else:
                            legging = 0

                        chance = random.choice([1, 3, 4])
                        if chance == 1:
                            boots_num = all_players[player]["lvl"] // 30 
                        elif chance == 3:
                            boots_num = all_players[player]["lvl"] // 30 + 1
                        else:
                            boots_num = 0
                        if all_players[player]["lvl"] < 40:
                            diamonds = 0
                            dragonite = 0
                        else:
                            diamonds = random.randint(1 + all_players[player]["lvl"] // 40, 3 + all_players[player]["lvl"] // 40)
                            dragonite = random.randint(0 + all_players[player]["lvl"] // 50, 2 + all_players[player]["lvl"] // 50)

                        items = []
                        for i in range(weapons):
                            rarity = random.randint(-150, 100)
                            if rarity <= 95 - ((all_players[player]["lvl"] // 10) * 2):
                                item = random.choice(swords)
                            else:
                                item = random.choice(elite_swords)
                            items.append(item)

                        shields = [
                            {"Name": "Reinforced Bark Shield", "DEF": 1.5, "SP": 0.8, "MAX DUR": 900, "DUR": 900, "Cost": 7000, "Class": "Shield"},
                            {"Name": "Rusty Steel Shield", "DEF": 1.3, "SP": 0.8, "MAX DUR": 1000, "DUR": 1000, "Cost": 5000, "Class": "Shield"}, 
                            {"Name": "Chainmail Shield", "DEF": 1.2, "SP": 0.9, "MAX DUR": 850, "DUR": 850, "Cost": 5000, "Class": "Shield"},
                            {"Name": "Reinforced Leather Shield", "DEF": 1.5, "SP": 1, "MAX DUR": 1150, "DUR": 1150, "Cost": 9000, "Class": "Shield"},
                            {"Name": "Wooden Shield", "DEF": 2, "SP": 1, "MAX DUR": 60, "DUR": 60, "Cost": 14000, "Class": "Shield"},
                            {"Name": "Rusted Steel Shield", "DEF": 1.3, "SP": 0.8, "MAX DUR": 1000, "DUR": 1000, "Cost": 4000, "Class": "Shield"},
                            {"Name": "Leather Shield", "DEF": 1.5, "SP": 1, "MAX DUR": 1150, "DUR": 1150, "Cost": 8000, "Class": "Shield"}
                        ]
                        for i in range(shields_num):
                            item = random.choice(shields)
                            items.append(item)

                        for i in range(helmets_num):
                            item = random.choice(helmets)
                            items.append(item)

                        for i in range(chestplate):
                            item = random.choice(chestplates)
                            items.append(item)

                        for i in range(legging):
                            item = random.choice(leggings)
                            items.append(item)

                        for i in range(boots_num):
                            item = random.choice(boots)
                            items.append(item)

                        type(f"{all_players[player]['name']}'s inventory: ")
                        print("Diamonds: ", diamonds)
                        print("Dragonite: ", dragonite)
                        for item in items:
                            print(f"Item: {item['Name']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   ATK/DEF: {item.get('ATK', item.get('DEF'))}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   SP: {item['SP']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   Crit: {item.get('Crit', 'N/A')}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   DUR: {item['DUR']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   Class: {item['Class']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   Cost: {item['Cost']}")
                            time.sleep(random.uniform(0, 0.3))
                        print("\n")
                        type(f"{stats['Name']}'s inventory: ")
                        for item in stats["Backpack"]:
                            if item.get("Class") == "Potion of Healing" or item.get("Class") == "Potion of Strength" or item.get("Class") == "Potion of Defense":
                                print(f"Item: {item['Name']}")
                                time.sleep(random.uniform(0, 0.3))
                                print(f"   Effect: {item['Effect']}")
                                time.sleep(random.uniform(0, 0.3))
                                print(f"   Class: {item['Class']}")
                                time.sleep(random.uniform(0, 0.3))
                                print(f"   Cost: {item['Cost']}")
                                time.sleep(random.uniform(0, 0.3))
                                continue
                            print(f"Item: {item['Name']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   ATK/DEF: {item.get('ATK', item.get('DEF'))}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   SP: {item['SP']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   Crit: {item.get('Crit', 'N/A')}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   DUR: {item['DUR']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   Class: {item['Class']}")
                            time.sleep(random.uniform(0, 0.3))
                            print(f"   Cost: {item['Cost']}")
                            time.sleep(random.uniform(0, 0.3))

                        response = input("Type anything to continue: ")
                        clear()
                        chat("Do you know what you want to trade? ")
                        response = input("Type anything to continue: ")
                        clear_last_line()
                        print("\t\t\t\t\t\t", response)
                        chat("Cool!")
                        trade = input("Type the item you want to trade with: ")
                        gift = input("Type the item you want to trade for: ")
                        found = False
                        found1 = False
                        clear()
                        for item in stats["Backpack"]:
                            if item.get("Name") == trade:
                                found = True
                                for i in items:
                                    if i.get("Name") == gift:
                                        found1 = True
                                        cost1 = 0
                                        cost2 = 0
                                        if gift == "Diamonds" or gift == "Diamond":
                                            diamondss = int(input("How many diamonds do you want to trade with: "))
                                            clear()
                                            cost2 = diamondss * 10000
                                        elif gift == "Dragonite" or gift == "Dragonites":
                                            dragonites = int(input("How many dragonites do you want to trade with: "))
                                            clear()
                                            cost2 = dragonites * 100000
                                        if trade == "Diamonds" or trade == "Diamond":
                                            diamondss = int(input("How many diamonds do you want to trade with: "))
                                            clear()
                                            if diamondss > stats["Diamonds"]:
                                                print("You do not have enough diamonds!")
                                                time.sleep(1)
                                                clear()
                                                break
                                            else:
                                                cost1 = diamondss * 10000
                                        elif trade == "Dragonite" or trade == "Dragonites":
                                            dragonites = int(input("How many dragonites do you want to trade with: "))
                                            clear()
                                            if dragonites > stats["Dragonite"]:
                                                print("You do not have enough dragonites!")
                                                time.sleep(1)
                                                clear()
                                                break
                                            else:
                                                cost1 = dragonites * 100000

                                        else:
                                            cost1 = item["Cost"]
                                            cost2 = i["Cost"]
                                        range1 = random.uniform(cost2 / 20, cost2 / 10)
                                        if cost2 - cost1 > range1:
                                            type("U trying to scam me. Geeeeet ouuuuuut.")
                                            time.sleep(1)
                                            clear()
                                            break
                                        elif cost2 * 2 <= cost1:
                                            type("You are scamming yourself.")
                                            break
                                        else:
                                            type("Nice! Trade accepted!")
                                            trade_finish = 1
                                            if gift == "Diamonds" or gift == "Diamond":
                                                stats["Diamonds"] += diamondss
                                            elif gift == "Dragonite" or gift == "Dragonites":
                                                stats["Dragonite"] += dragonites
                                            for item in stats["Backpack"]:
                                                if item.get("Name") == trade:
                                                    stats["Backpack"].remove(item)
                                                    stats["Backpack"].append(i)
                                                    break
                        if trade_finish == 1:
                            break

                        if not found or not found1:
                            print("Items not found!")
                            time.sleep(1)
                            break

                else:
                    print("Player not found!")
                    time.sleep(1)
                    clear() 

def starlight_armory():
    global enchantment
    global enchanting_name
    global enchants
    global enchant_num
    global enchant
    enchanting = check_enchantment()
    if enchantment:
        if enchanting == 1:
            print("Your enchantment is complete! You will be directed back to the main menu.")
            time.sleep(1)
            clear()
            multiplier = 0
            if enchant_num == "I":
                multiplier = 1
            elif enchant_num == "II":
                multiplier = 2
            elif enchant_num == "III":
                multiplier = 3
            elif enchant_num == "IV":
                multiplier = 4
            else:
                multiplier = 5
            item_to_find = enchanting_name
            for item in stats["Backpack"]:
                if item.get("Name") == item_to_find:
                    item["Name"] += f" | {enchants} {enchant_num}"
                    if item.get("Class") == "Weapon":
                        if enchants == "Sharpness":
                            item["ATK"] += 0.2 * multiplier
                        elif enchants == "Thorns":
                            item["ATK"] += 0.35 * multiplier
                        elif enchants == "Unbreaking":
                            item["MAX DUR"] += 100 * multiplier
                            item["DUR"] += 100 * multiplier
                        elif enchants == "Fire Aspect":
                            stats["Weapon"]["Tier"] = multiplier
                            pass
                        elif enchants == "Looting":
                            pass
                        break
                    elif item.get("Class") == "Shield":
                        if enchants == "Protection":
                            item["DEF"] += 0.2 * multiplier
                        elif enchants == "Thorns":
                            pass
                        elif enchants == "Unbreaking":
                            item["MAX DUR"] += 100 * multiplier
                            item["DUR"] += 100 * multiplier
                        elif enchants == "Divine Guard":
                            pass
                        break 
                    else:
                        if enchants == "Protection":
                            item["DEF"] += 0.2 * multiplier
                        elif enchants == "Fire Protection":
                            pass
                        elif enchants == "Heartforge":
                            pass
                        elif enchants == "Unbreaking":
                            item["MAX DUR"] += 100 * multiplier
                            item["DUR"] += 100 * multiplier
                        elif enchants == "FrostGuard":
                            pass

            enchanting = 0
            enchantment = False
        elif enchanting == 0:
            check_enchantment()
    else:
        if stats["Celestium Prism"] == 0:
            type("You don't have a Celestium Prism! Obtain Celetsium Prisms by defeating bosses in the Rotfang Depths!")
            time.sleep(2)
            clear()
        else:
            type("Welcome to the Starlight Armory!")
            time.sleep(1)
            clear()
            type("You step through the grand archway of the Starlight Armory, and instantly the air hums with a shimmering energy — like the whole room is wrapped in a glowing nebula. A celestial scent of ozone and magic lingers, tickling your senses and stirring the thrill of untapped potential. This is no mere armory... this is the forge of destinies, where stars align to craft heroes. 🌟⚔️🌙")
            hi = input("Type anything to continue: ")
            if hi is not None:
                pass
            else: 
                pass
            clear()
            print("Celestium Prisms: ", stats["Celestium Prism"], "\n")
            time.sleep(0.1)
            for idx, item in enumerate(stats["Backpack"], 1):
                print(f"Item {idx}:")
                time.sleep(0.15)
                for k, v in item.items():
                    print(f"  {k}: {v}")
                    time.sleep(0.15)
                print()
                time.sleep(0.15)
            item = input("Enter the class of the item you want to enchant(Type 1 if you want to leave): ").lower()
            clear()
            if item == "1":
                pass
            else:
                num1 = random.choice(["I", "I", "I", "I", "I", "I", "I", "I", "II", "II", "II", "III", "III", "IV"])
                num2 = random.choice(["I", "I", "I", "II", "II", "II", "II", "II", "III", "III", "III", "III", "IV", "V"])
                num3 = random.choice(["II", "II", "II", "III", "III", "III", "III", "IV", "IV", "V"])
                if item == "weapon":
                    print("⚔️ Weapons in Backpack:\n")
                    weapon_count = 1
                    for item in stats["Backpack"]:
                        if item.get("Class") == "Weapon":
                            print(f"Weapon {weapon_count}:")
                            for k, v in item.items():
                                print(f"  {k}: {v}")
                            print()
                            weapon_count += 1
                    weapon = input("Enter the name of the weapon you want to enchant(Type 1 if you want to leave): ")
                    if weapon == "1":
                        pass
                    else:
                        found = False
                        for item in stats["Backpack"]:
                            if item.get("Name") == weapon and item.get("Class") == "Weapon":
                                found = True
                                break
                        if found:
                            start(weapon, "Searching", 1, 2)
                            clear()
                            type(f"🎉 {weapon} found!")
                            time.sleep(1)
                            clear()
                            lvl25_enchant = random.choice(sword1_enchants)
                            lvl60_enchant = random.choice(sword2_enchants)
                            lvl100_enchant = random.choice(sword3_enchants)
                            print("_________________________\n")
                            time.sleep(0.2)
                            print("Lvl 25 Enchant: ", lvl25_enchant, num1)
                            print("\t Cost: 1 Celestium Prism", "\n")
                            time.sleep(0.2)
                            print("_________________________\n\n")
                            time.sleep(0.2)
                            print("_________________________\n")
                            time.sleep(0.2)
                            print("Lvl 60 Enchant: ", lvl60_enchant, num2)
                            print("\t Cost: 2 Celestium Prism", "\n")
                            time.sleep(0.2)
                            print("_________________________\n\n")
                            time.sleep(0.2)
                            print("_________________________\n")
                            time.sleep(0.2)
                            print("Lvl 100 Enchant: ", lvl100_enchant, num3)
                            print("\t Cost: 3 Celestium Prism", "\n")
                            time.sleep(0.2)
                            print("_________________________\n\n")
                            enchant = int(input("Enter the level of the enchant you want to apply(25 | 60 | 100 | Type 1 if you want to leave): "))
                            if enchant == 1:
                                pass
                            else: 
                                if stats["Lvl"] < enchant:
                                    print("You do not have the level to enchant this weapon!")
                                    time.sleep(1)
                                    clear()
                                    pass
                                else:
                                    enchanting_name = weapon
                                    enchants = lvl25_enchant
                                    enchant_num = num1
                                    duration = random.uniform(240, 420)
                                    enchantment = True
                                    if enchant == 25:
                                        if enchantment:
                                            start("Enchantment", "Starting", 1, 2)
                                            print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                            time.sleep(2)
                                            stats["Celestium Prism"] -= 1
                                        start_enchant(duration)
                                    elif enchant == 60:
                                        if enchantment:
                                            start("Enchantment", "Starting", 1, 2)
                                            print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                            time.sleep(2)
                                            stats["Celestium Prism"] -= 2
                                        start_enchant(duration)
                                    elif enchant == 100:
                                        if enchantment:
                                            start("Enchantment", "Starting", 1, 2)
                                            print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                            time.sleep(2)
                                            stats["Celestium Prism"] -= 2
                                        start_enchant(duration)
                        else:
                            print(f"😭 {weapon} not found!")
                            time.sleep(1)
                            clear()
                            pass
                elif item == "shield":
                    print("⚔️ Shields in Backpack:\n")
                    weapon_count = 1
                    for item in stats["Backpack"]:
                        if item.get("Class") == "Shield":
                            print(f"Shield {weapon_count}:")
                            for k, v in item.items():
                                print(f"  {k}: {v}")
                            print()
                            weapon_count += 1
                    shield = input("Enter the name of the shield you want to enchant(Type 1 if you want to leave): ")
                    if shield == "1":
                        pass
                    else:
                        found = False
                        for item in stats["Backpack"]:
                            if item.get("Name") == shield and item.get("Class") == "Shield":
                                found = True
                                break
                        if found:
                            start(shield, "Searching", 1, 2)
                            clear()
                            type(f"🎉 {shield} found!")
                            time.sleep(1)
                            clear()
                            lvl25_enchant = random.choice(shield1_enchants)
                            lvl60_enchant = random.choice(shield2_enchants)
                            lvl100_enchant = random.choice(shield3_enchants)
                            print("_________________________\n")
                            time.sleep(0.2)
                            print("Lvl 25 Enchant: ", lvl25_enchant, num1)
                            print("\t Cost: 1 Celestium Prism", "\n")
                            time.sleep(0.2)
                            print("_________________________\n\n")
                            time.sleep(0.2)
                            print("_________________________\n")
                            time.sleep(0.2)
                            print("Lvl 60 Enchant: ", lvl60_enchant, num2)
                            print("\t Cost: 2 Celestium Prism", "\n")
                            time.sleep(0.2)
                            print("_________________________\n\n")
                            time.sleep(0.2)
                            print("_________________________\n")
                            time.sleep(0.2)
                            print("Lvl 100 Enchant: ", lvl100_enchant, num3)
                            print("\t Cost: 3 Celestium Prism", "\n")
                            time.sleep(0.2)
                            print("_________________________\n\n")
                            enchant = int(input("Enter the level of the enchant you want to apply(25 | 60 | 100 | Type 1 if you want to leave): "))
                            if enchant == 1:
                                pass
                            else: 
                                if stats["Lvl"] < enchant:
                                    print("You do not have the level to enchant this shield!")
                                    time.sleep(1)
                                    clear()
                                    pass
                                else:
                                    enchanting_name = shield
                                    enchants = lvl25_enchant
                                    enchant_num = num1
                                    duration = random.uniform(240, 420)
                                    enchantment = True
                                    if enchant == 25:
                                        if enchantment:
                                            start("Enchantment", "Starting", 1, 2)
                                            print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                            time.sleep(2)
                                            stats["Celestium Prism"] -= 1
                                        start_enchant(duration)
                                    elif enchant == 60:
                                        if enchantment:
                                            start("Enchantment", "Starting", 1, 2)
                                            print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                            time.sleep(2)
                                            stats["Celestium Prism"] -= 2
                                        start_enchant(duration)
                                    elif enchant == 100:
                                        if enchantment:
                                            start("Enchantment", "Starting", 1, 2)
                                            print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                            time.sleep(2)
                                            stats["Celestium Prism"] -= 2
                                        start_enchant(duration)
                        else:
                            print(f"😭 {shield} not found!")
                            time.sleep(1)
                            clear()
                            pass
                else:
                    if item == "helmet":
                        print("⚔️ Helmets in Backpack:\n")
                        weapon_count = 1
                        for item in stats["Backpack"]:
                            if item.get("Class") == "Helmet":
                                print(f"Helmet {weapon_count}:")
                                for k, v in item.items():
                                    print(f"  {k}: {v}")
                                print()
                                weapon_count += 1
                        helmet = input("Enter the name of the helmet you want to enchant(Type 1 if you want to leave): ")
                        if helmet == "1":
                            pass
                        else:
                            found = False
                            for item in stats["Backpack"]:
                                if item.get("Name") == helmet and item.get("Class") == "Helmet":
                                    found = True
                                    break
                            if found:
                                start(helmet, "Searching", 1, 2)
                                clear()
                                lvl25_enchant = random.choice(armor1_enchants)
                                lvl60_enchant = random.choice(armor2_enchants)
                                lvl100_enchant = random.choice(armor3_enchants)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 25 Enchant: ", lvl25_enchant, num1)
                                print("\t Cost: 1 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 60 Enchant: ", lvl60_enchant, num2)
                                print("\t Cost: 2 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 100 Enchant: ", lvl100_enchant, num3)
                                print("\t Cost: 3 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                enchant = int(input("Enter the level of the enchant you want to apply(25 | 60 | 100 | Type 1 if you want to leave): "))
                                if enchant == 1:
                                    pass
                                else: 
                                    if stats["Lvl"] < enchant:
                                        print("You do not have the level to enchant this helmet!")
                                        time.sleep(1)
                                        clear()
                                        pass
                                    else:
                                        enchanting_name = helmet
                                        enchants = lvl25_enchant
                                        enchant_num = num1
                                        duration = random.uniform(240, 420)
                                        enchantment = True
                                        if enchant == 25:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 1
                                            start_enchant(duration)
                                        elif enchant == 60:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                                        elif enchant == 100:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                            else:
                                print(f"😭 {helmet} not found!")
                                time.sleep(1)
                                clear()
                                pass
                    elif item == "chestplate":
                        print("⚔️ Chestplates in Backpack:\n")
                        weapon_count = 1
                        for item in stats["Backpack"]:
                            if item.get("Class") == "Chestplate":
                                print(f"Chestplate {weapon_count}:")
                                for k, v in item.items():
                                    print(f"  {k}: {v}")
                                print()
                                weapon_count += 1
                        chestplate = input("Enter the name of the helmet you want to enchant(Type 1 if you want to leave): ")
                        if chestplate == "1":
                            pass
                        else:
                            found = False
                            for item in stats["Backpack"]:
                                if item.get("Name") == chestplate and item.get("Class") == "Chestplate":
                                    found = True
                                    break
                            if found:
                                start(chestplate, "Searching", 1, 2)
                                clear()
                                lvl25_enchant = random.choice(armor1_enchants)
                                lvl60_enchant = random.choice(armor2_enchants)
                                lvl100_enchant = random.choice(armor3_enchants)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 25 Enchant: ", lvl25_enchant, num1)
                                print("\t Cost: 1 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 60 Enchant: ", lvl60_enchant, num2)
                                print("\t Cost: 2 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 100 Enchant: ", lvl100_enchant, num3)
                                print("\t Cost: 3 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                enchant = int(input("Enter the level of the enchant you want to apply(25 | 60 | 100 | Type 1 if you want to leave): "))
                                if enchant == 1:
                                    pass
                                else: 
                                    if stats["Lvl"] < enchant:
                                        print("You do not have the level to enchant this chestplate!")
                                        time.sleep(1)
                                        clear()
                                        pass
                                    else:
                                        enchanting_name = chestplate
                                        enchants = lvl25_enchant
                                        enchant_num = num1
                                        duration = random.uniform(240, 420)
                                        enchantment = True
                                        if enchant == 25:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 1
                                            start_enchant(duration)
                                        elif enchant == 60:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                                        elif enchant == 100:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                            else:
                                print(f"😭 {chestplate} not found!")
                                time.sleep(1)
                                clear()
                                pass
                    elif item == "leggings":
                        print("⚔️ Leggings in Backpack:\n")
                        weapon_count = 1
                        for item in stats["Backpack"]:
                            if item.get("Class") == "Leggings":
                                print(f"Legging {weapon_count}:")
                                for k, v in item.items():
                                    print(f"  {k}: {v}")
                                print()
                                weapon_count += 1
                        legging = input("Enter the name of the helmet you want to enchant(Type 1 if you want to leave): ")
                        if legging == "1":
                            pass
                        else:
                            found = False
                            for item in stats["Backpack"]:
                                if item.get("Name") == legging and item.get("Class") == "Leggings":
                                    found = True
                                    break
                            if found:
                                start(legging, "Searching", 1, 2)
                                clear()
                                lvl25_enchant = random.choice(armor1_enchants)
                                lvl60_enchant = random.choice(armor2_enchants)
                                lvl100_enchant = random.choice(armor3_enchants)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 25 Enchant: ", lvl25_enchant, num1)
                                print("\t Cost: 1 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 60 Enchant: ", lvl60_enchant, num2)
                                print("\t Cost: 2 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 100 Enchant: ", lvl100_enchant, num3)
                                print("\t Cost: 3 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                enchant = int(input("Enter the level of the enchant you want to apply(25 | 60 | 100 | Type 1 if you want to leave): "))
                                if enchant == 1:
                                    pass
                                else: 
                                    if stats["Lvl"] < enchant:
                                        print("You do not have the level to enchant this legging!")
                                        time.sleep(1)
                                        clear()
                                        pass
                                    else:
                                        enchanting_name = legging
                                        enchants = lvl25_enchant
                                        enchant_num = num1
                                        duration = random.uniform(240, 420)
                                        enchantment = True
                                        if enchant == 25:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 1
                                            start_enchant(duration)
                                        elif enchant == 60:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                                        elif enchant == 100:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                            else:
                                print(f"😭 {legging} not found!")
                                time.sleep(1)
                                clear()
                                pass
                    elif item == "boots":
                        print("⚔️ Boots in Backpack:\n")
                        weapon_count = 1
                        for item in stats["Backpack"]:
                            if item.get("Class") == "Boot":
                                print(f"Boot {weapon_count}:")
                                for k, v in item.items():
                                    print(f"  {k}: {v}")
                                print()
                                weapon_count += 1
                        boot = input("Enter the name of the helmet you want to enchant(Type 1 if you want to leave): ")
                        if boot == "1":
                            pass
                        else:
                            found = False
                            for item in stats["Backpack"]:
                                if item.get("Name") == boot and item.get("Class") == "Boots":
                                    found = True
                                    break
                            if found:
                                start(boot, "Searching", 1, 2)
                                clear()
                                lvl25_enchant = random.choice(armor1_enchants)
                                lvl60_enchant = random.choice(armor2_enchants)
                                lvl100_enchant = random.choice(armor3_enchants)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 25 Enchant: ", lvl25_enchant, num1)
                                print("\t Cost: 1 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 60 Enchant: ", lvl60_enchant, num2)
                                print("\t Cost: 2 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                time.sleep(0.2)
                                print("_________________________\n")
                                time.sleep(0.2)
                                print("Lvl 100 Enchant: ", lvl100_enchant, num3)
                                print("\t Cost: 3 Celestium Prism", "\n")
                                time.sleep(0.2)
                                print("_________________________\n\n")
                                enchant = int(input("Enter the level of the enchant you want to apply(25 | 60 | 100 | Type 1 if you want to leave): "))
                                if enchant == 1:
                                    pass
                                else: 
                                    if stats["Lvl"] < enchant:
                                        print("You do not have the level to enchant this boot!")
                                        time.sleep(1)
                                        clear()
                                        pass
                                    else:
                                        enchanting_name = boot
                                        enchants = lvl25_enchant
                                        enchant_num = num1
                                        duration = random.uniform(240, 420)
                                        enchantment = True
                                        if enchant == 25:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 1
                                            start_enchant(duration)
                                        elif enchant == 60:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                                        elif enchant == 100:
                                            if enchantment:
                                                start("Enchantment", "Starting", 1, 2)
                                                print("You will be directed back to the main menu. To check the enchantment progress, go to the Starlight Armory again.")
                                                time.sleep(2)
                                                stats["Celestium Prism"] -= 2
                                            start_enchant(duration)
                            else:
                                print(f"😭 {boot} not found!")
                                time.sleep(1)
                                clear()
                                pass

def obsidian_anvil():
    type("Welcome to the Obsidian Anvil!")
    time.sleep(0.7)
    clear()
    level = 0
    if stats["Diamond"] == 0:
        type("You don't have diamonds! Obtain Diamonds by mining in Crimson Depths!")
        time.sleep(2)
        clear()
    else:
        for item in stats["Backpack"]:
            print("Item details:")
            for key, value in item.items():
                print(f"  {key}: {value}")
            print()
        item = input("Enter the name of the item you want to repair(Capitalization counts!): ")
        clear()
        found = False
        for i in stats["Backpack"]:
            if i.get("Name") == item:
                found = True
                break
        if found:
            if stats["Diamond"] == 1:
                print("You can only do a level 1 repair! Cost: 1 Diamond | (20% repair)")
                time.sleep(0.2)
                hi = input("Type yes or no: ")
                if hi == "yes":
                    level = 1
                    stats["Diamond"] -= 1
                elif hi == "no":
                    pass
            elif stats["Diamond"] == 2:
                print("-------------------------")
                time.sleep(0.2)
                print("Level 1 Repair (20% repair)| Cost: 1 Diamond")
                time.sleep(0.2)
                print("-------------------------")
                time.sleep(0.2)
                print("Level 2 Repair (50% repair)| Cost: 2 Diamonds")
                time.sleep(0.2)
                print("-------------------------")
                time.sleep(0.2)
                hi = int(input("Enter the level of the repair you want to do | Type 0 to leave: "))
                if hi == 0:
                    pass
                else:
                    level = hi
                    stats["Diamond"] -= level
            else:
                print("-------------------------")
                time.sleep(0.2)
                print("Level 1 Repair (20% repair)| Cost: 1 Diamond")
                time.sleep(0.2)
                print("-------------------------")
                time.sleep(0.2)
                print("Level 2 Repair (50% repair)| Cost: 2 Diamonds")
                time.sleep(0.2)
                print("-------------------------")
                time.sleep(0.2)
                print("Level 3 Repair (100% repair)| Cost: 3 Diamonds")
                time.sleep(0.2)
                print("------------------------")
                time.sleep(0.2)
                hi = int(input("Enter the level of the repair you want to do | Type 0 to leave: "))
                if hi == 0:
                    pass
                else:
                    level = hi
                    stats["Diamond"] -= level
            clear()
            times = 15
            times1 = 25
            start("Repairing", "", times + (level * 5), times1 + (level * 5))
            for i in stats["Backpack"]:
                if i.get("Name") == item:
                    if level == 3:
                        i["DUR"] = i["MAX DUR"]
                    elif level == 2:
                        if i["DUR"] + (i["MAX DUR"] * 0.5) > i["MAX DUR"]:
                            i["DUR"] = i["MAX DUR"]
                        else:
                            i["DUR"] += i["MAX DUR"] * 0.5
                    elif level == 1:
                        if i["DUR"] + (i["MAX DUR"] * 0.2) > i["MAX DUR"]:
                            i["DUR"] = i["MAX DUR"]
                        else:
                            i["DUR"] += i["MAX DUR"] * 0.2
                    break
        else:
            type("Item not found!!")
            time.sleep(1)
            clear()

def tavern():
    type("Welcome to the tavern!")
    time.sleep(0.2)
    type("Here you can name your sword and play mini games to earn gold!")
    time.sleep(1)
    clear()
    choice = input("What would you like to do( 1. Name sword | 2. Gamble | Type 1 if you want to leave): ").lower()
    clear()
    if choice == "1":
        for index, item in enumerate(stats["Backpack"], start=1):
            print(f"Item {index}:")
            for key, value in item.items():
                print(f"   {key}: {value}")
        sword = input("Which sword would you like to name(Type 1 if you want to leave | Capitalization counts): ")
        found = False
        for item in stats["Backpack"]:
            if item.get("Name") == sword:
                found = True
                break
        if not found:
            type("Sword not found!")
            time.sleep(1)
            clear()
        else:
            name = input("What would you like to name your sword: ")
            for item in stats["Backpack"]:
                if item.get("Name") == sword:
                    item["Name"] = name
                    break
            type(f"Your sword is now named {name}!")
            time.sleep(1)
            clear()
    elif choice == "2":
        print()

def view_stats():
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"{key}:")
            if value:
                for k, v in value.items():
                    print(f"  {k}: {v}")
            print()
        elif isinstance(value, list):
            print(f"{key}:")
            for idx, item in enumerate(value, 1):
                print(f"  Item {idx}:")
                for k, v in item.items():
                    print(f"    {k}: {v}")
            print()
        else:
            print(f"{key}: {value}\n")
    hi = input("Type anything to continue: ")
    if hi is not None:
        pass
    else: 
        pass

def change_loadout():
    print("------------------------")
    time.sleep(0.3)
    print("Weapon: ", stats["Weapon"])
    time.sleep(0.3)
    print("Left Hand: ", stats["Left Hand"])
    time.sleep(0.3)
    print("------------------------\n")
    time.sleep(0.3)
    print("Backpack:")
    time.sleep(0.3)
    print(*stats["Backpack"], sep = "\n")
    time.sleep(0.3)
    choice = input("\nEnter what you want to change(Weapon/Left Hand): ").lower()
    clear()
    if choice == "weapon":
        var = 0
        var1 = 0
        while var == 0:
            sword = input("What weapon would you like to equip(Type 1 if you want to leave): ")
            if sword == "1":
                var1 = 1
                break
            found = False
            for item in stats["Backpack"]:
                if "Name" in item and "Class" in item:
                    if item["Name"] == sword and item["Class"] == "Weapon":
                        found = True
                        break
            print(f"Searching for {sword}...")
            time.sleep(random.uniform(0, 4))
            if found:
                print("🎯 Weapon found!")
            else:
                print("No such weapon in the backpack!")
                time.sleep(1)
                break
            time.sleep(0.5)
            print(f"Equiping {sword}...")
            time.sleep(random.uniform(0, 3))
            for i in range(len(stats["Backpack"])):
                item = stats["Backpack"][i]
                if item["Name"] == sword and item["Class"] == "Weapon":
                    stats["Backpack"][i], stats["Weapon"] = stats["Weapon"], stats["Backpack"][i]
                    print(f"You equipped {sword}!")
                    break
            time.sleep(2)
            break
        if var1 == 1:
            pass
    else:
        var = 0
        var1 = 0
        while var == 0:
            shield = input("What item would you like to equip(Type 1 if you want to leave): ")
            if shield == "1":
                var1 = 1
                break
            found = False
            for item in stats["Backpack"]:
                if "Name" in item and "Class" in item:
                    if item["Name"] == shield:
                        found = True
                        break
            print(f"Searching for {shield}...")
            time.sleep(random.uniform(0, 4))
            if found:
                print("🎯 Item found!")
            else:
                print("No such item in the backpack!")
                time.sleep(1)
                break
            time.sleep(0.5)
            print(f"Equiping {shield}...")
            time.sleep(random.uniform(0, 3))
            for i in range(len(stats["Backpack"])):
                item = stats["Backpack"][i]
                if item["Name"] == shield:
                    stats["Backpack"][i], stats["Left Hand"] = stats["Left Hand"], stats["Backpack"][i]
                    print(f"You equipped {shield}!")
                    break
            time.sleep(2)
            break
        if var1 == 1:
            pass          

def change_loadout_armor():
    print("------------------------")
    time.sleep(0.1)
    print("Helmet: ", stats["Helmet"])
    time.sleep(0.1)
    print("\nChestplate: ", stats["Chestplate"])
    time.sleep(0.1)
    print("\nLeggings: ", stats["Leggings"])
    time.sleep(0.1)
    print("\nBoots: ", stats["Boots"])
    time.sleep(0.1)
    print("------------------------\n")
    time.sleep(0.1)
    print("Backpack:")
    time.sleep(0.1)
    print(*stats["Backpack"], sep = "\n")
    time.sleep(0.3)
    choice = input("\nEnter the piece of armor you want to change (Type 1 to leave): ").lower()
    clear()
    if choice == "1":
        pass
    elif choice == "helmet":
        var = 0
        var1 = 0
        while var == 0:
            helmet = input("What helmet would you like to equip(Type 1 if you want to leave): ")
            if helmet == "1":
                var1 = 1
                break
            found = False
            for item in stats["Backpack"]:
                if "Name" in item and "Class" in item and item["Name"] == helmet and item["Class"] == "Helmet":
                    found = True
                    break
            clear()
            print(f"Searching for {helmet}...")
            time.sleep(random.uniform(0, 4))
            if found:
                print("🎯 Helmet found!")
                clear()
            else:
                print("No such helmet in the backpack!")
                time.sleep(1)
                break
            time.sleep(0.5)
            print(f"Equiping {helmet}...")
            time.sleep(random.uniform(0, 3))
            for i in range(len(stats["Backpack"])):
                if "Name" in stats["Backpack"][i] and "Class" in stats["Backpack"][i] and stats["Backpack"][i]["Name"] == helmet and stats["Backpack"][i]["Class"] == "Helmet":
                    stats["Backpack"][i], stats["Helmet"] = stats["Helmet"], stats["Backpack"][i]
                    print(f"You equipped {helmet}!")
                    break
            time.sleep(2)
            break
        if var1 == 1:
            pass
    elif choice == "chestplate":
        var = 0
        var1 = 0
        while var == 0:
            chestplate = input("What chestplate would you like to equip(Type 1 if you want to leave): ")
            if chestplate == "1":
                var1 = 1
                break
            found = False
            for item in stats["Backpack"]:
                if "Name" in item and "Class" in item:
                    if item["Name"] == chestplate and item["Class"] == "Chestplate":
                        found = True
                        break
            clear()
            print(f"Searching for {chestplate}...")
            time.sleep(random.uniform(0, 4))
            if found:
                print("🎯 Chestplate found!")
                clear()
            else:
                print("No such chestplate in the backpack!")
                time.sleep(1)
                break
            time.sleep(0.5)
            print(f"Equiping {chestplate}...")
            time.sleep(random.uniform(0, 3))
            for i in range(len(stats["Backpack"])):
                if "Name" in stats["Backpack"][i] and "Class" in stats["Backpack"][i] and stats["Backpack"][i]["Name"] == chestplate and stats["Backpack"][i]["Class"] == "Chestplate":
                    stats["Backpack"][i], stats["Chestplate"] = stats["Chestplate"], stats["Backpack"][i]
                    print(f"You equipped {chestplate}!")
                    break
            time.sleep(2)
            break
        if var1 == 1:
            pass
    elif choice == "leggings":
        var = 0
        var1 = 0
        while var == 0:
            leggings = input("What leggings would you like to equip(Type 1 if you want to leave): ")
            if leggings == "1":
                var1 = 1
                break
            found = False
            for item in stats["Backpack"]:
                if "Name" in item and "Class" in item:
                    if item["Name"] == leggings and item["Class"] == "Leggings":
                        found = True
                        break
            clear()
            print(f"Searching for {leggings}...")
            time.sleep(random.uniform(0, 4))
            if found:
                print("🎯 Leggings found!")
                clear()
            else:
                print("No such leggings in the backpack!")
                time.sleep(1)
                break
            time.sleep(0.5)
            print(f"Equiping {leggings}...")
            time.sleep(random.uniform(0, 3))
            for i in range(len(stats["Backpack"])):
                if "Name" in stats["Backpack"][i] and "Class" in stats["Backpack"][i] and stats["Backpack"][i]["Name"] == leggings and stats["Backpack"][i]["Class"] == "Leggings":
                    stats["Backpack"][i], stats["Leggings"] = stats["Leggings"], stats["Backpack"][i]
                    print(f"You equipped {leggings}!")
                    break
            time.sleep(2)
            break
        if var1 == 1:
            pass
    elif choice == "boots":
        var = 0
        var1 = 0
        while var == 0:
            boots = input("What boots would you like to equip(Type 1 if you want to leave): ")
            if boots == "1":
                var1 = 1
                break
            found = False
            for item in stats["Backpack"]:
                if "Name" in item and "Class" in item:
                    if item["Name"] == boots and item["Class"] == "Boots":
                        found = True
                        break
            clear()
            print(f"Searching for {boots}...")
            time.sleep(random.uniform(0, 4))
            if found:
                print("🎯 Boots found!")
                clear()
            else:
                print("No such boots in the backpack!")
                time.sleep(1)
                break
            time.sleep(0.5)
            print(f"Equiping {boots}...")
            time.sleep(random.uniform(0, 3))
            for i in range(len(stats["Backpack"])):
                if "Name" in stats["Backpack"][i] and "Class" in stats["Backpack"][i] and stats["Backpack"][i]["Name"] == boots and stats["Backpack"][i]["Class"] == "Boots":
                    stats["Backpack"][i], stats["Boots"] = stats["Boots"], stats["Backpack"][i]
                    print(f"You equipped {boots}!")
                    break
            time.sleep(2)
            break
        if var1 == 1:
            pass

def tips():
    print("***********************")
    time.sleep(0.1)
    type("1. Combat Tips\n")
    time.sleep(0.1)
    type("2. Shop/Normal Tips\n")
    time.sleep(0.1)
    type("3. Enchanting Tips")
    time.sleep(0.1)
    print("***********************")
    time.sleep(0.1)
    option1 = int(input("What would you like to do? "))
    clear()
    if option1 == 1:
        print("Combat Tips\n")    
        time.sleep(0.1)
        print("1. Your shield has a chance to block all enemy DM for that turn\n")
        time.sleep(0.1)
        print("2. Recommended: Keep best shield in left hand\n")
        time.sleep(0.1)
        print("3. You can use Shield Bash to attack enemy(s)\n")
        time.sleep(0.1)
        print("4. If you have a weapon in both hands, you can attack two times but the second time does 3/4 DM.\n")
        time.sleep(0.1)
        print("5. If you use a potion/magic runes or artifacts in your left hand to heal or cast spells, you use up your turn so choose wisely.\n")
        time.sleep(0.1)
        print("6. Warning: You can't put scrolls in any of your hands.\n")
        time.sleep(0.1)
        print("7. In battle, you can use the hacking technique to insta-kill the enemy or guarantee a critical hit. But beware the consquences. If you get caught trying to insta-kill then the enemy does NOT die and it will have 2x DM 1.5x HP and 1.5x DEF. If you lose that battle, you will lose EXP pointss, gold, and potentially your equipment. If you get caught trying to get critical hits, you will not succeed and for the rest of the battle you will NOT have any crits and you will have 0.5x SP and DEF.\n")
        hi = input("Type anything to continue: ")
        if hi is not None:
            print("")
        clear()
    if option1 == 2:
        print("Shop/Normal Tips\n")
        time.sleep(0.1)
        print("1. You can sell items in your backpack to the shopkeeper.\n")
        time.sleep(0.1)
        print("2. Warning: When you sell an item, the shopkeeper will ask you the price of the item. If you put a price that is higher than the range, then the shopkeeper will automatically sell the item for 1/2 the price it is actually worth.\n")
        type("EX:")
        print("\tI have a wooden sword that is worth 100 gold. If the range is 30 gold and I put a price of 150 gold, then because 150 > 130, the shopkeeper will sell it for 50 gold (1/2 of 100 gold).")
        time.sleep(0.1)
        print("3. Caution: If you put a price that is lower than its worth, then the shopkeeper will automatically sell the item for the price you put\n")
        time.sleep(0.1)
        print("4. When you rage quit the game, pls look at the goodbye message. It is very funny.💀💀💀")
        hi = input("Type anything to continue: ")
        if hi is not None:
            print("")
        clear()
    if option1 == 3:
        print("Enchanting Tips\n")
        time.sleep(0.1)
        print("1. You can enchant weapons, shields, and armor.\n")
        time.sleep(0.1)
        print("2. You can enchant an item to a certain level (25, 60, 100). The higher the level, the better the enchantment.\n")
        time.sleep(0.1)
        print("3. You need Celestium Prisms to enchant items. You can get Celestium Prisms by defeating bosses in the Rotfang Depths.\n")
        time.sleep(0.1)
        print("4. You can check the progress of your enchantment by going to the Starlight Armory.\n")
        time.sleep(0.1)
        print("5. You can only enchant one item at a time.\n")
        time.sleep(0.1)
        print("6. You can only enchant items that are in your backpack.\n")
        time.sleep(0.1)
        print("7. Previous enchants are not lost when you enchant again.\n")
        hi = input("Type anything to continue: ")
        if hi is not None:
            print("")

#MAIN MENU
while option != 14:
    os.system('git add players.json')
    os.system('git commit -m "player save"')
    os.system('git push')
    players = load_players()
    players[stats["Name"]] = stats
    save_players(players)
    clear()
    print("------------------------")
    time.sleep(0.1)
    print("1. Arena\n")
    time.sleep(0.1)
    print("2. Adventure\n")
    time.sleep(0.1)
    print("3. The Sapphire Docks\n")
    time.sleep(0.1)
    print("4. Shop\n")
    time.sleep(0.1)
    print("5. Goldspire Market\n")
    time.sleep(0.1)
    print("6. Starlight Armory\n")
    time.sleep(0.1)
    print("7. Obsidian Anvil\n")
    time.sleep(0.1)
    print("8. Tavern\n")
    time.sleep(0.1)
    print("9. View Stats/Inventory\n")
    time.sleep(0.1)
    print("10. Change Loadout / Weapons\n")
    time.sleep(0.1)
    print("11. Change Loadout / Armor\n")
    time.sleep(0.1)
    print("12. Tips\n")
    time.sleep(0.1)
    print("13. AI Chat\n")
    time.sleep(0.1)
    print("14. Rage Quit")
    time.sleep(0.1)
    print("------------------------")
    time.sleep(0.1)
    option = int(input("What would you like to do? "))
    clear()
    if option == 1:
        arena()
    if option == 2:
        adventure()
    if option == 3:
        fishing()
    if option == 4:
        shop()
    if option == 5:
        goldspire_market()
    if option == 6:
        starlight_armory()
    if option == 7:
        obsidian_anvil()
    if option == 8:
        tavern()
    if option == 9:
        view_stats()
    if option == 10:
        change_loadout()
    if option == 11:
        change_loadout_armor()
    if option == 12:
        tips()
    if option == 13:
        _unused_chat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "UNUSED.py")
        if not os.path.isfile(_unused_chat_path):
            print("AI Chat skipped: UNUSED.py is missing beside the game.")
            hi = input("Press Enter to return: ")
            if hi is not None:
                time.sleep(0)
        else:
            try:
                spec = importlib.util.spec_from_file_location("rpg_unused_chat", _unused_chat_path)
                if spec is None or spec.loader is None:
                    raise RuntimeError("Could not load UNUSED.py")
                unused_mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(unused_mod)
                unused_mod.chatbot(stats)
            except Exception as err:
                print(f"AI Chat unavailable ({err}). Ensure gpt4all and model path inside UNUSED.py are valid.")
                hi = input("Press Enter to return: ")
                if hi is not None:
                    time.sleep(0)
        clear()
    if option == 14:
        type(" BYEEEE")
        for i in range(10000000000000000000000000000000000000000000000):
            print("*" * i) 
