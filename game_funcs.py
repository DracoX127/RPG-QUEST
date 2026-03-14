from name_data import prefixes, middles, suffixes
from typing import Dict, Any
import threading
import select
import platform
import random
import json
import time
import sys
import os
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