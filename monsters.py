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
        "HP": 20000,
        "ATK": 1500,
        "DEF": 1000,
        "Crit": 50,
        "SP": 50,
        "EXP": 5000,
        "Weapon": {"Name": "Starforged Etherium Double-Edged Sharpsword", "ATK": 10, "SP": 2, "Crit": 3, "MAX DUR": 5000, "DUR": 5000, "Class": "Weapon"},
        "Left Hand": {"Name": "Nethersteel Jagged Shield", "DEF": 5, "SP": 3, "MAX DUR": 5500, "DUR": 5500, "Class": "Shield"},
        "Helmet": {"Name": "Stormforged Phantom Iron Helmet", "DEF": 7, "SP": 1, "MAX DUR": 4800, "DUR": 4800, "Class": "Helmet"},
        "Chestplate": {"Name": "Voidcrystal Chestplate", "DEF": 10, "SP": 1, "MAX DUR": 6000, "DUR": 6000, "Class": "Chestplate"},
        "Leggings": {"Name": "Bloodiron Leggings", "DEF": 7, "SP": 2, "MAX DUR": 5200, "DUR": 5200, "Class": "Boots"},
        "Boots": {"Name": "Abyssal Gold Boots", "DEF": 5, "SP": 3, "MAX DUR": 5100, "DUR": 5100, "Class": "Boots"}
    },
    "Goblin Sergeant": {
        "HP": 20000, 
        "ATK": 5000, 
        "DEF": 3000, 
        "Crit": 100,
        "SP": 0,
        "EXP": 5000,
        "Weapon": {"Name": "Great Damascus Sword", "ATK": 6, "SP": 1, "Crit": 3, "MAX DUR": 4600, "DUR": 4600, "Class": "Weapon"},
        "Left Hand": {"Name": "Crusader Round Shield", "DEF": 2, "SP": 1.25, "MAX DUR": 4300, "DUR": 4300, "Class": "Shield"},
        "Helmet": {"Name": "Celestial Bronze Helmet", "DEF": 7, "SP": 1, "MAX DUR": 4900, "DUR": 4900, "Class": "Helmet"},
        "Chestplate": {"Name": "Celestial Bronze Chestplate", "DEF": 8, "SP": 1, "MAX DUR": 5200, "DUR": 5200, "Class": "Chestplate"},
        "Leggings": {"Name": "Admantine Leggings", "DEF": 7, "SP": 2, "MAX DUR": 4800, "DUR": 4800, "Class": "Boots"},
        "Boots": {"Name": "Reinforced Feather Boots", "DEF": 5, "SP": 3, "MAX DUR": 4700, "DUR": 4700, "Class": "Boots"}
    },
    "Troll Swordsman": {
        "HP": 20000,
        "ATK": 10000,
        "DEF": 0,
        "Crit": 0,
        "SP": 0,
        "EXP": 5000,
        "Weapon": {"Name": "Ghoststeel Sharpsword", "ATK": 20, "SP": 1, "Crit": 5, "MAX DUR": 6000, "DUR": 6000, "Class": "Weapon"},
        "Left Hand": {"Name": "Starsteel Aegis", "DEF": 15, "SP": 1, "MAX DUR": 6300, "DUR": 6300, "Class": "Shield"},
        "Helmet": {"Name": "Voidglass Helmet", "DEF": 4, "SP": 1, "MAX DUR": 4800, "DUR": 4800, "Class": "Helmet"},
        "Chestplate": {"Name": "Voidglass Chestplate", "DEF": 6, "SP": 1, "MAX DUR": 5200, "DUR": 5200, "Class": "Chestplate"},
        "Leggings": {"Name": "Voidglass Leggings", "DEF": 4, "SP": 2, "MAX DUR": 5000, "DUR": 5000, "Class": "Boots"},
        "Boots": {"Name": "Voidglass Boots", "DEF": 2, "SP": 3, "MAX DUR": 4700, "DUR": 4700, "Class": "Boots"}
    }
}