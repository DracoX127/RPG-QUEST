import random
import time
import json
import os
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

from ui import (
    console, type, event, section, announcement, menu_panel, info_panel,
    stats_table, equip_card, inventory_table, small_title, separator,
    input_prompt, int_prompt, confirm_prompt, clear, auto_style
)
from effects import (
    dialogue, rainbow_text, burst_particles, flash_screen, shake_screen,
    level_up_effect, loot_popup, victory_fanfare, boss_entrance,
    damage_popup, screen_title, animated_loading, voice_say
)

# ============================================================
#  QUEST SYSTEM
# ============================================================

QUESTS: Dict[str, Dict[str, Any]] = {
    "first_blood": {
        "name": "First Blood",
        "description": "Defeat 5 enemies in Crimson Fields",
        "type": "kill",
        "target": "soldiers",
        "count": 5,
        "rewards": {"Gold": 500, "EXP": 100, "Diamond": 1},
        "dialog_start": "New adventurer! Prove your worth by slaying 5 goblins.",
        "dialog_complete": "Well done! You've earned your first rewards.",
        "speaker": "warrior",
    },
    "shaman_hunt": {
        "name": "Shaman Hunt",
        "description": "Defeat 3 shamans in Rotfang Depths",
        "type": "kill",
        "target": "monsters",
        "count": 3,
        "min_lvl": 20,
        "rewards": {"Gold": 2000, "EXP": 500, "Celestium Prism": 1},
        "dialog_start": "The shamans grow too powerful. Thin their ranks!",
        "dialog_complete": "The Rotfang Depths are safer thanks to you.",
        "speaker": "mage",
    },
    "boss_slayer": {
        "name": "Boss Slayer",
        "description": "Defeat any boss in the Boss Arena",
        "type": "kill",
        "target": "boss",
        "count": 1,
        "min_lvl": 50,
        "rewards": {"Gold": 10000, "EXP": 2000, "Dragonite": 2, "Celestium Prism": 3},
        "dialog_start": "A true hero must face the mightiest foes!",
        "dialog_complete": "You are a legend among adventurers!",
        "speaker": "boss",
    },
    "fish_monger": {
        "name": "Fish Monger",
        "description": "Catch 10 fish in a single tournament",
        "type": "fish",
        "count": 10,
        "rewards": {"Gold": 1500, "EXP": 300},
        "dialog_start": "The sea calls to you! Show us your fishing skills!",
        "dialog_complete": "Master angler! The fish fear your name.",
        "speaker": "merchant",
    },
    "rich_adventurer": {
        "name": "Rich Adventurer",
        "description": "Accumulate 100,000 gold",
        "type": "gold",
        "count": 100000,
        "rewards": {"Gold": 5000, "EXP": 1000, "Diamond": 5},
        "dialog_start": "Gold makes the world go round! Get rich!",
        "dialog_complete": "You're swimming in gold! Fantastic!",
        "speaker": "merchant",
    },
    "enchanter": {
        "name": "Enchanter Apprentice",
        "description": "Enchant 3 items at the Starlight Armory",
        "type": "enchant",
        "count": 3,
        "rewards": {"Gold": 3000, "EXP": 600, "Celestium Prism": 2},
        "dialog_start": "The magic of enchantment awaits you!",
        "dialog_complete": "Your enchanting skills are growing strong!",
        "speaker": "mage",
    },
    "gear_up": {
        "name": "Gear Up",
        "description": "Equip a full set of armor (helmet, chestplate, leggings, boots)",
        "type": "gear",
        "count": 4,
        "rewards": {"Gold": 2000, "EXP": 400, "Diamond": 2},
        "dialog_start": "You can't face dangers without proper protection!",
        "dialog_complete": "Now you're ready for anything!",
        "speaker": "warrior",
    },
}

class QuestTracker:
    def __init__(self, stats: Dict[str, Any]):
        self.stats = stats
        if "quests" not in self.stats:
            self.stats["quests"] = {}
        if "quest_progress" not in self.stats:
            self.stats["quest_progress"] = {}

    def get_available(self) -> List[str]:
        available = []
        for qid, qdata in QUESTS.items():
            if qid in self.stats["quests"]:
                continue
            min_lvl = qdata.get("min_lvl", 1)
            if self.stats.get("Lvl", 1) >= min_lvl:
                available.append(qid)
        return available

    def get_active(self) -> List[str]:
        return [qid for qid in self.stats.get("quests", {})
                if not self.stats["quests"][qid].get("completed")]

    def accept(self, qid: str) -> bool:
        if qid not in QUESTS:
            return False
        if qid in self.stats["quests"]:
            return False
        min_lvl = QUESTS[qid].get("min_lvl", 1)
        if self.stats.get("Lvl", 1) < min_lvl:
            return False
        self.stats["quests"][qid] = {"completed": False, "progress": 0}
        self.stats["quest_progress"][qid] = 0
        qdata = QUESTS[qid]
        dialogue(qdata["dialog_start"], qdata.get("speaker", "narrator"))
        return True

    def progress(self, qid: str, amount: int = 1) -> None:
        if qid not in self.stats.get("quests", {}):
            return
        if self.stats["quests"][qid].get("completed"):
            return
        self.stats["quests"][qid]["progress"] = self.stats["quests"][qid].get("progress", 0) + amount
        self.stats["quest_progress"][qid] = self.stats["quests"][qid]["progress"]

    def progress_type(self, quest_type: str, target: Optional[str] = None, amount: int = 1) -> None:
        for qid in self.get_active():
            qdata = QUESTS[qid]
            if qdata["type"] != quest_type:
                continue
            if target and qdata.get("target") and qdata["target"] != target:
                continue
            self.progress(qid, amount)
            self._check_complete(qid)

    def _check_complete(self, qid: str) -> bool:
        qdata = QUESTS[qid]
        progress = self.stats["quests"][qid].get("progress", 0)
        if progress >= qdata["count"]:
            self.stats["quests"][qid]["completed"] = True
            return True
        return False

    def claim(self, qid: str) -> bool:
        if qid not in self.stats.get("quests", {}):
            return False
        if not self.stats["quests"][qid].get("completed"):
            return False
        if self.stats["quests"][qid].get("claimed"):
            return False
        qdata = QUESTS[qid]
        for reward_key, reward_val in qdata["rewards"].items():
            if reward_key == "Gold":
                self.stats["Gold"] = self.stats.get("Gold", 0) + reward_val
            elif reward_key == "EXP":
                from RPG_QUEST_2 import grant_exp
                grant_exp(self.stats, reward_val)
            else:
                self.stats[reward_key] = self.stats.get(reward_key, 0) + reward_val
        self.stats["quests"][qid]["claimed"] = True
        dialogue(qdata["dialog_complete"], qdata.get("speaker", "narrator"))
        rainbow_text(f"QUEST COMPLETE: {qdata['name']}!")
        return True

    def display(self) -> None:
        section("QUESTS")
        active = self.get_active()
        available = self.get_available()
        if active:
            console.print("[bold yellow]Active Quests:[/bold yellow]")
            for qid in active:
                qdata = QUESTS[qid]
                prog = self.stats["quests"][qid].get("progress", 0)
                total = qdata["count"]
                bar_filled = int((prog / total) * 15)
                bar = f"[{'█' * bar_filled}{'░' * (15 - bar_filled)}]"
                console.print(f"  [bold cyan]{qdata['name']}[/bold cyan]")
                console.print(f"    {qdata['description']}")
                console.print(f"    {bar} {prog}/{total}")
                if prog >= total:
                    console.print("    [bold green]✓ Ready to claim![/bold green]")
                console.print()
        if available:
            console.print("[bold yellow]Available Quests:[/bold yellow]")
            for qid in available:
                qdata = QUESTS[qid]
                console.print(f"  [bold cyan]{qdata['name']}[/bold cyan]")
                console.print(f"    {qdata['description']}")
                console.print(f"    [dim]Rewards: {', '.join(f'{v} {k}' for k, v in qdata['rewards'].items())}[/dim]")
                console.print()
        if not active and not available:
            console.print("  [dim italic]No quests available[/dim italic]")

    def menu(self) -> None:
        while True:
            clear()
            self.display()
            console.print()
            console.print("[bold yellow]Options:[/bold yellow]")
            console.print("  1. Accept a quest")
            console.print("  2. Claim rewards")
            console.print("  3. Return")
            choice = int_prompt("Choice: ")
            clear()
            if choice == 1:
                available = self.get_available()
                if not available:
                    type("No quests available.", style="dim")
                    time.sleep(1)
                    continue
                for i, qid in enumerate(available, 1):
                    qdata = QUESTS[qid]
                    console.print(f"  {i}. [bold cyan]{qdata['name']}[/bold cyan] - {qdata['description']}")
                pick = int_prompt("Accept quest number (0 to cancel): ")
                if 1 <= pick <= len(available):
                    qid = available[pick - 1]
                    if self.accept(qid):
                        type(f"Quest accepted: {QUESTS[qid]['name']}!")
                    else:
                        type("Failed to accept quest.")
                time.sleep(1)
            elif choice == 2:
                claimed = False
                for qid in list(self.stats.get("quests", {}).keys()):
                    if self.stats["quests"][qid].get("completed") and not self.stats["quests"][qid].get("claimed"):
                        self.claim(qid)
                        claimed = True
                if not claimed:
                    type("No quests ready to claim.")
                time.sleep(1)
            elif choice == 3:
                break

# ============================================================
#  SKILL TREE
# ============================================================

SKILLS: Dict[str, Dict[str, Any]] = {
    "warrior": {
        "name": "Warrior",
        "abilities": {
            "power_strike": {
                "name": "Power Strike",
                "description": "Deal 2x damage with a 30% chance",
                "cost": {"Gold": 1000, "Lvl": 5},
                "effect": {"mult_damage": 2.0, "chance": 30},
                "icon": "⚔",
            },
            "shield_wall": {
                "name": "Shield Wall",
                "description": "50% chance to block all damage",
                "cost": {"Gold": 2500, "Lvl": 10},
                "effect": {"block_chance_bonus": 30},
                "icon": "🛡",
            },
            "war_cry": {
                "name": "War Cry",
                "description": "Boost STR by 50% for 3 turns",
                "cost": {"Gold": 5000, "Lvl": 20},
                "effect": {"str_mult": 1.5, "turns": 3},
                "icon": "🔊",
            },
            "executioner": {
                "name": "Executioner",
                "description": "5% chance to instantly kill normal enemies",
                "cost": {"Gold": 10000, "Lvl": 35},
                "effect": {"insta_kill_chance": 5},
                "icon": "💀",
            },
            "berserker_rage": {
                "name": "Berserker Rage",
                "description": "Below 25% HP, deal 3x damage",
                "cost": {"Gold": 20000, "Lvl": 50},
                "effect": {"low_hp_mult": 3.0, "low_hp_threshold": 0.25},
                "icon": "🔥",
            },
        }
    },
    "thief": {
        "name": "Thief",
        "abilities": {
            "backstab": {
                "name": "Backstab",
                "description": "Guaranteed crit on first attack",
                "cost": {"Gold": 1000, "Lvl": 5},
                "effect": {"first_crit": True},
                "icon": "🗡",
            },
            "evasion": {
                "name": "Evasion",
                "description": "25% chance to dodge any attack",
                "cost": {"Gold": 2500, "Lvl": 10},
                "effect": {"dodge_chance": 25},
                "icon": "💨",
            },
            "pickpocket": {
                "name": "Pickpocket",
                "description": "50% extra gold from victories",
                "cost": {"Gold": 5000, "Lvl": 20},
                "effect": {"gold_mult": 1.5},
                "icon": "💰",
            },
            "shadow_step": {
                "name": "Shadow Step",
                "description": "Attack twice in one turn (30% chance)",
                "cost": {"Gold": 10000, "Lvl": 35},
                "effect": {"double_attack_chance": 30},
                "icon": "🌑",
            },
            "assassinate": {
                "name": "Assassinate",
                "description": "10% chance to instantly kill any enemy",
                "cost": {"Gold": 20000, "Lvl": 50},
                "effect": {"insta_kill_chance": 10},
                "icon": "🔪",
            },
        }
    },
    "berserker": {
        "name": "Berserker",
        "abilities": {
            "heavy_blow": {
                "name": "Heavy Blow",
                "description": "1.5x damage, -20% accuracy",
                "cost": {"Gold": 1000, "Lvl": 5},
                "effect": {"mult_damage": 1.5, "accuracy_penalty": 20},
                "icon": "👊",
            },
            "bloodlust": {
                "name": "Bloodlust",
                "description": "Kills restore 20% HP",
                "cost": {"Gold": 2500, "Lvl": 10},
                "effect": {"kill_heal": 0.2},
                "icon": "🩸",
            },
            "unstoppable": {
                "name": "Unstoppable",
                "description": "Ignore 50% of enemy DEF",
                "cost": {"Gold": 5000, "Lvl": 20},
                "effect": {"def_penetration": 0.5},
                "icon": "💪",
            },
            "enrage": {
                "name": "Enrage",
                "description": "Below 50% HP, +100% ATK, -50% DEF",
                "cost": {"Gold": 10000, "Lvl": 35},
                "effect": {"enrage_atk": 2.0, "enrage_def": 0.5},
                "icon": "😡",
            },
            "colossus_smash": {
                "name": "Colossus Smash",
                "description": "3x damage, 50% stun chance",
                "cost": {"Gold": 20000, "Lvl": 50},
                "effect": {"mult_damage": 3.0, "stun_chance": 50},
                "icon": "🌋",
            },
        }
    }
}

class SkillTree:
    def __init__(self, stats: Dict[str, Any]):
        self.stats = stats
        if "skills" not in self.stats:
            self.stats["skills"] = {}
        self.class_name = self._detect_class()

    def _detect_class(self) -> str:
        weapon = self.stats.get("Weapon", {}).get("Name", "")
        hp = self.stats.get("HP", 0)
        sp = self.stats.get("SP", 0)
        if sp >= 40:
            return "thief"
        elif hp > 1900:
            return "berserker"
        return "warrior"

    def get_learned(self) -> List[str]:
        return [aid for aid, data in self.stats.get("skills", {}).items() if data.get("learned")]

    def can_learn(self, ability_id: str) -> bool:
        class_data = SKILLS.get(self.class_name)
        if not class_data or ability_id not in class_data.get("abilities", {}):
            return False
        if ability_id in self.stats.get("skills", {}):
            return False
        ab = class_data["abilities"][ability_id]
        for req_key, req_val in ab["cost"].items():
            if req_key == "Gold" and self.stats.get("Gold", 0) < req_val:
                return False
            if req_key == "Lvl" and self.stats.get("Lvl", 1) < req_val:
                return False
        return True

    def learn(self, ability_id: str) -> bool:
        if not self.can_learn(ability_id):
            return False
        class_data = SKILLS[self.class_name]
        ab = class_data["abilities"][ability_id]
        for req_key, req_val in ab["cost"].items():
            if req_key == "Gold":
                self.stats["Gold"] -= req_val
        if "skills" not in self.stats:
            self.stats["skills"] = {}
        self.stats["skills"][ability_id] = {"learned": True}
        rainbow_text(f"★ LEARNED: {ab['icon']} {ab['name']}!")
        burst_particles(10, "bold magenta")
        return True

    def display(self) -> None:
        section(f"SKILL TREE - {self.class_name.upper()}")
        class_data = SKILLS.get(self.class_name)
        if not class_data:
            console.print("[dim]No skills available for your class[/dim]")
            return
        for aid, ab in class_data["abilities"].items():
            learned = aid in self.get_learned()
            can = self.can_learn(aid)
            status = "[bold green]✓ LEARNED[/bold green]" if learned else (
                "[bold yellow]CAN LEARN[/bold yellow]" if can else "[dim]LOCKED[/dim]"
            )
            costs = ", ".join(f"{v} {k}" for k, v in ab["cost"].items())
            console.print(f"  {ab['icon']} [bold cyan]{ab['name']}[/bold cyan] - {status}")
            console.print(f"    {ab['description']}")
            if not learned:
                console.print(f"    [dim]Cost: {costs}[/dim]")
            console.print()

    def menu(self) -> None:
        while True:
            clear()
            self.display()
            console.print()
            console.print("[bold yellow]Options:[/bold yellow]")
            console.print("  1. Learn a skill")
            console.print("  2. Return")
            choice = int_prompt("Choice: ")
            clear()
            if choice == 1:
                class_data = SKILLS.get(self.class_name)
                if not class_data:
                    time.sleep(1)
                    continue
                ab_list = [(aid, ab) for aid, ab in class_data["abilities"].items()
                          if self.can_learn(aid)]
                if not ab_list:
                    type("No skills available to learn.")
                    time.sleep(1)
                    continue
                for i, (aid, ab) in enumerate(ab_list, 1):
                    console.print(f"  {i}. {ab['icon']} [bold cyan]{ab['name']}[/bold cyan] - {ab['description']}")
                pick = int_prompt("Learn skill number (0 to cancel): ")
                if 1 <= pick <= len(ab_list):
                    aid = ab_list[pick - 1][0]
                    if self.learn(aid):
                        type("Skill learned!")
                    else:
                        type("Failed to learn skill.")
                time.sleep(1)
            elif choice == 2:
                break

# ============================================================
#  ACHIEVEMENT SYSTEM
# ============================================================

ACHIEVEMENTS: Dict[str, Dict[str, Any]] = {
    "first_steps": {
        "name": "First Steps",
        "description": "Reach level 5",
        "condition": lambda s: s.get("Lvl", 1) >= 5,
        "rewards": {"Gold": 500},
    },
    "adventurer": {
        "name": "Adventurer",
        "description": "Reach level 25",
        "condition": lambda s: s.get("Lvl", 1) >= 25,
        "rewards": {"Gold": 2500, "Diamond": 3},
    },
    "veteran": {
        "name": "Veteran",
        "description": "Reach level 50",
        "condition": lambda s: s.get("Lvl", 1) >= 50,
        "rewards": {"Gold": 10000, "Dragonite": 2, "Celestium Prism": 2},
    },
    "legend": {
        "name": "Legend",
        "description": "Reach level 100",
        "condition": lambda s: s.get("Lvl", 1) >= 100,
        "rewards": {"Gold": 50000, "Dragonite": 10, "Celestium Prism": 10},
    },
    "rich": {
        "name": "Money Bags",
        "description": "Accumulate 50,000 gold",
        "condition": lambda s: s.get("Gold", 0) >= 50000,
        "rewards": {"Gold": 5000},
    },
    "millionaire": {
        "name": "Millionaire",
        "description": "Accumulate 1,000,000 gold",
        "condition": lambda s: s.get("Gold", 0) >= 1000000,
        "rewards": {"Gold": 100000, "Dragonite": 5},
    },
    "gear_collector": {
        "name": "Gear Collector",
        "description": "Own 10 items in backpack",
        "condition": lambda s: len(s.get("Backpack", [])) >= 10,
        "rewards": {"Gold": 2000},
    },
    "hoarder": {
        "name": "Hoarder",
        "description": "Own 50 items in backpack",
        "condition": lambda s: len(s.get("Backpack", [])) >= 50,
        "rewards": {"Gold": 10000, "Diamond": 5},
    },
    "enchanter": {
        "name": "Enchanter",
        "description": "Enchant 5 items",
        "condition": lambda s: s.get("enchants_done", 0) >= 5,
        "rewards": {"Gold": 5000, "Celestium Prism": 3},
    },
    "fisher": {
        "name": "Fisher King",
        "description": "Win a fishing tournament",
        "condition": lambda s: s.get("fishing_wins", 0) >= 1,
        "rewards": {"Gold": 3000},
    },
}

class AchievementTracker:
    def __init__(self, stats: Dict[str, Any]):
        self.stats = stats
        if "achievements" not in self.stats:
            self.stats["achievements"] = {}

    def check_all(self) -> List[str]:
        unlocked = []
        for aid, adata in ACHIEVEMENTS.items():
            if aid in self.stats.get("achievements", {}):
                continue
            if adata["condition"](self.stats):
                self._unlock(aid)
                unlocked.append(aid)
        return unlocked

    def _unlock(self, aid: str) -> None:
        self.stats["achievements"][aid] = True
        adata = ACHIEVEMENTS[aid]
        for reward_key, reward_val in adata.get("rewards", {}).items():
            if reward_key == "Gold":
                self.stats["Gold"] = self.stats.get("Gold", 0) + reward_val
            else:
                self.stats[reward_key] = self.stats.get(reward_key, 0) + reward_val
        rainbow_text(f"🏆 ACHIEVEMENT UNLOCKED: {adata['name']}!")
        event(f"Reward: {', '.join(f'{v} {k}' for k,v in adata.get('rewards',{}).items())}", "loot")
        burst_particles(15, "bold yellow")
        time.sleep(0.5)

    def display(self) -> None:
        section("ACHIEVEMENTS")
        unlocked = 0
        for aid, adata in ACHIEVEMENTS.items():
            if aid in self.stats.get("achievements", {}):
                unlocked += 1
                console.print(f"  [bold green]✓[/bold green] [bold cyan]{adata['name']}[/bold cyan] - {adata['description']}")
            else:
                console.print(f"  [dim]✗[/dim] [dim white]{adata['name']}[/dim white] - [dim]{adata['description']}[/dim]")
        console.print(f"\n  [bold yellow]Unlocked: {unlocked}/{len(ACHIEVEMENTS)}[/bold yellow]")

# ============================================================
#  CRAFTING SYSTEM
# ============================================================

RECIPES: Dict[str, Dict[str, Any]] = {
    "iron_sword": {
        "name": "Iron Sword",
        "type": "Weapon",
        "ingredients": {"Diamond": 2, "Gold": 500},
        "result": {"Name": "Iron Shortsword", "ATK": 1.7, "SP": 1.0, "Crit": 1.0, "MAX DUR": 85, "DUR": 85, "Class": "Weapon", "Cost": 12000},
        "skill": 1,
    },
    "steel_armor": {
        "name": "Steel Chestplate",
        "type": "Chestplate",
        "ingredients": {"Diamond": 5, "Gold": 2000},
        "result": {"Name": "Reinforced Steel Chestplate", "DEF": 4.5, "SP": 1.2, "MAX DUR": 950, "DUR": 950, "Class": "Chestplate", "Cost": 30000},
        "skill": 2,
    },
    "potion_heal_2": {
        "name": "Greater Healing Potion",
        "type": "Potion",
        "ingredients": {"Gold": 300},
        "result": {"Name": "Potion of Healing", "Tier": 2, "Effect": 1000, "Class": "Potion of Healing", "Cost": 500},
        "skill": 1,
    },
    "potion_str_2": {
        "name": "Greater Strength Potion",
        "type": "Potion",
        "ingredients": {"Gold": 500},
        "result": {"Name": "Potion of Strength", "Tier": 2, "Effect": 3, "Class": "Potion of Strength", "Cost": 800},
        "skill": 1,
    },
    "dragon_sword": {
        "name": "Dragonbone Sword",
        "type": "Weapon",
        "ingredients": {"Diamond": 10, "Dragonite": 3, "Gold": 10000},
        "result": {"Name": "Dragonbone Carver", "ATK": 4.2, "SP": 1.3, "Crit": 2.1, "MAX DUR": 300, "DUR": 300, "Class": "Weapon", "Cost": 28000},
        "skill": 3,
    },
    "celestial_chest": {
        "name": "Celestial Chestplate",
        "type": "Chestplate",
        "ingredients": {"Diamond": 15, "Dragonite": 5, "Celestium Prism": 2, "Gold": 50000},
        "result": {"Name": "Celestial Forged Chestplate", "DEF": 7.0, "SP": 1.8, "MAX DUR": 1500, "DUR": 1500, "Class": "Chestplate", "Cost": 80000},
        "skill": 4,
    },
    "mythic_blade": {
        "name": "Mythic Blade",
        "type": "Weapon",
        "ingredients": {"Diamond": 25, "Dragonite": 10, "Celestium Prism": 5, "Gold": 100000},
        "result": {"Name": "Mythic Starforged Blade", "ATK": 8.0, "SP": 2.0, "Crit": 4.0, "MAX DUR": 800, "DUR": 800, "Class": "Weapon", "Cost": 150000},
        "skill": 5,
    },
}

class CraftingSystem:
    def __init__(self, stats: Dict[str, Any]):
        self.stats = stats
        if "crafting_skill" not in self.stats:
            self.stats["crafting_skill"] = 1

    def can_craft(self, recipe_id: str) -> Tuple[bool, str]:
        recipe = RECIPES.get(recipe_id)
        if not recipe:
            return False, "Recipe not found"
        if self.stats.get("crafting_skill", 1) < recipe["skill"]:
            return False, f"Need crafting skill level {recipe['skill']} (have {self.stats.get('crafting_skill', 1)})"
        for ing_key, ing_val in recipe["ingredients"].items():
            if ing_key == "Gold":
                if self.stats.get("Gold", 0) < ing_val:
                    return False, f"Need {ing_val} gold (have {self.stats.get('Gold', 0)})"
            else:
                if self.stats.get(ing_key, 0) < ing_val:
                    return False, f"Need {ing_val} {ing_key} (have {self.stats.get(ing_key, 0)})"
        return True, "Ready to craft!"

    def craft(self, recipe_id: str) -> bool:
        can, msg = self.can_craft(recipe_id)
        if not can:
            type(msg, style="bold red")
            return False
        recipe = RECIPES[recipe_id]
        for ing_key, ing_val in recipe["ingredients"].items():
            if ing_key == "Gold":
                self.stats["Gold"] -= ing_val
            else:
                self.stats[ing_key] -= ing_val
        result = dict(recipe["result"])
        self.stats["Backpack"].append(result)
        self.stats["crafting_skill"] = self.stats.get("crafting_skill", 1) + 0.1
        rainbow_text(f"🔨 CRAFTED: {result['Name']}!")
        burst_particles(10, "bold orange")
        return True

    def display(self) -> None:
        section(f"CRAFTING (Skill: {self.stats.get('crafting_skill', 1):.1f})")
        for rid, recipe in RECIPES.items():
            can, msg = self.can_craft(rid)
            status = "[bold green]✔[/bold green]" if can else f"[dim]✘[/dim]"
            ingredients = ", ".join(f"{v} {k}" for k, v in recipe["ingredients"].items())
            result_name = recipe["result"]["Name"]
            console.print(f"  {status} [bold cyan]{recipe['name']}[/bold cyan] (Skill {recipe['skill']})")
            console.print(f"    → [bold white]{result_name}[/bold white]")
            console.print(f"    [dim]Materials: {ingredients}[/dim]")
            if not can:
                console.print(f"    [dim red]{msg}[/dim red]")
            console.print()

    def menu(self) -> None:
        while True:
            clear()
            self.display()
            console.print()
            console.print("[bold yellow]Options:[/bold yellow]")
            console.print("  1. Craft an item")
            console.print("  2. Return")
            choice = int_prompt("Choice: ")
            clear()
            if choice == 1:
                craftable = [rid for rid in RECIPES if self.can_craft(rid)[0]]
                if not craftable:
                    type("Nothing can be crafted with your current materials.")
                    time.sleep(1)
                    continue
                for i, rid in enumerate(craftable, 1):
                    recipe = RECIPES[rid]
                    console.print(f"  {i}. [bold cyan]{recipe['name']}[/bold cyan] → {recipe['result']['Name']}")
                pick = int_prompt("Craft item number (0 to cancel): ")
                if 1 <= pick <= len(craftable):
                    rid = craftable[pick - 1]
                    if self.craft(rid):
                        type("Item crafted successfully!", style="bold green")
                    else:
                        type("Crafting failed!", style="bold red")
                time.sleep(1)
            elif choice == 2:
                break

# ============================================================
#  GAMBLING MINI-GAMES
# ============================================================

def dice_game(stats: Dict[str, Any]) -> None:
    """Play dice against the house."""
    clear()
    screen_title("🎲 DICE GAME", "Roll higher than the house to win!")
    bet = int_prompt("Your bet (0 to leave): ")
    if bet <= 0:
        return
    if bet > stats.get("Gold", 0):
        type("You don't have enough gold!", style="bold red")
        time.sleep(1)
        return
    stats["Gold"] -= bet
    player_roll = random.randint(1, 6) + random.randint(1, 6)
    house_roll = random.randint(1, 6) + random.randint(1, 6)
    for i in range(3):
        console.print(f"[bold cyan]Rolling...{'.' * (i+1)}[/bold cyan]")
        time.sleep(0.3)
    console.print(f"\n[bold yellow]You rolled:[/bold yellow] [bold white]{player_roll}[/bold white]")
    time.sleep(0.5)
    console.print(f"[bold red]House rolled:[/bold red] [bold white]{house_roll}[/bold white]")
    time.sleep(0.5)
    if player_roll > house_roll:
        winnings = bet * 2
        stats["Gold"] += winnings
        rainbow_text(f"🎉 YOU WIN! +{winnings} gold!")
        burst_particles(10, "bold yellow")
    elif player_roll == house_roll:
        stats["Gold"] += bet
        type("Tie! Your bet is returned.", style="bold white")
    else:
        type(f"You lost {bet} gold.", style="bold red")
    time.sleep(1)

def slot_machine(stats: Dict[str, Any]) -> None:
    """Slot machine gambling."""
    clear()
    screen_title("🎰 SLOT MACHINE", "Match three symbols to win big!")
    symbols = ["🍒", "🔔", "💎", "7️⃣", "🍀", "⭐"]
    payouts = {
        ("🍒", "🍒", "🍒"): 5,
        ("🔔", "🔔", "🔔"): 10,
        ("💎", "💎", "💎"): 25,
        ("7️⃣", "7️⃣", "7️⃣"): 50,
        ("🍀", "🍀", "🍀"): 100,
        ("⭐", "⭐", "⭐"): 200,
    }
    bet = int_prompt("Your bet (0 to leave): ")
    if bet <= 0:
        return
    if bet > stats.get("Gold", 0):
        type("Not enough gold!", style="bold red")
        time.sleep(1)
        return
    stats["Gold"] -= bet
    result = []
    for _ in range(3):
        console.print("[bold cyan]Spinning...[/bold cyan]")
        time.sleep(0.3)
        clear()
        result.append(random.choice(symbols))
        console.print(f"[bold yellow]{' | '.join(result + ['?'] * (3 - len(result)))}[/bold yellow]")
    console.print()
    key = tuple(result)
    if key in payouts:
        multiplier = payouts[key]
        winnings = bet * multiplier
        stats["Gold"] += winnings
        rainbow_text(f"🎉 JACKPOT! {multiplier}x! +{winnings} gold!")
        burst_particles(20, "bold yellow")
    else:
        type("No match. Better luck next time!", style="dim")
    time.sleep(1)

def blackjack(stats: Dict[str, Any]) -> None:
    """Simple blackjack game."""
    clear()
    screen_title("🃏 BLACKJACK", "Get 21 without going over!")
    bet = int_prompt("Your bet (0 to leave): ")
    if bet <= 0:
        return
    if bet > stats.get("Gold", 0):
        type("Not enough gold!", style="bold red")
        time.sleep(1)
        return
    stats["Gold"] -= bet

    def draw():
        return random.randint(1, 11)

    player = [draw(), draw()]
    house = [draw(), draw()]
    console.print(f"\n[bold cyan]Your hand:[/bold cyan] {player[0]} + {player[1]} = [bold white]{sum(player)}[/bold white]")
    console.print(f"[bold red]House shows:[/bold red] {house[0]} + ?")
    while sum(player) < 21:
        choice = input_prompt("Hit or stand? (h/s): ").lower()
        if choice == "h":
            card = draw()
            player.append(card)
            console.print(f"[bold cyan]You drew: {card}[/bold cyan]")
            console.print(f"[bold white]Total: {sum(player)}[/bold white]")
        else:
            break
    if sum(player) > 21:
        type("Bust! You lose.", style="bold red")
        time.sleep(1)
        return
    while sum(house) < 17:
        house.append(draw())
    console.print(f"\n[bold red]House hand:[/bold red] {' + '.join(str(c) for c in house)} = [bold white]{sum(house)}[/bold white]")
    time.sleep(0.5)
    if sum(house) > 21 or sum(player) > sum(house):
        winnings = bet * 2
        stats["Gold"] += winnings
        rainbow_text(f"🎉 YOU WIN! +{winnings} gold!")
    elif sum(player) == sum(house):
        stats["Gold"] += bet
        type("Push! Your bet is returned.", style="bold white")
    else:
        type(f"You lost {bet} gold.", style="bold red")
    time.sleep(1)

# ============================================================
#  EXPANDED MONSTERS
# ============================================================

ADDITIONAL_MONSTERS: Dict[str, Dict[str, Any]] = {
    "Fire Elemental": {
        "HP": 3000,
        "ATK": 400,
        "DEF": 100,
        "Crit": 15,
        "SP": 40,
        "EXP": 60,
        "Weapon": {"Name": "Inferno Blast", "ATK": 3, "SP": 1.5, "Crit": 2.5, "MAX DUR": 999, "DUR": 999, "Class": "Weapon"},
        "Left Hand": {"Name": "Ember Aura", "Effect": "Fire Shield", "Chance": 20, "Class": "Rune"},
        "Helmet": {},
        "Chestplate": {},
        "Leggings": {},
        "Boots": {},
        "Drops": [{"Name": "Ember Essence", "Class": "Scroll"}, {"Name": "Scroll of Infernal Blaze", "Class": "Scroll"}],
    },
    "Ice Wraith": {
        "HP": 2800,
        "ATK": 350,
        "DEF": 150,
        "Crit": 25,
        "SP": 50,
        "EXP": 55,
        "Weapon": {"Name": "Frozen Scepter", "ATK": 2.5, "SP": 1.8, "Crit": 3.0, "MAX DUR": 999, "DUR": 999, "Class": "Weapon"},
        "Left Hand": {"Name": "Frostbound Talisman", "Effect": "Dodge", "Chance": 40, "Class": "Rune"},
        "Helmet": {},
        "Chestplate": {},
        "Leggings": {},
        "Boots": {},
        "Drops": [{"Name": "Frostbound Talisman", "Effect": "Dodge", "Chance": 40, "Class": "Rune"}, {"Name": "Scroll of Endless Winter", "Class": "Scroll"}],
    },
    "Shadow Assassin": {
        "HP": 2500,
        "ATK": 500,
        "DEF": 80,
        "Crit": 30,
        "SP": 60,
        "EXP": 65,
        "Weapon": {"Name": "Void Daggers", "ATK": 3.5, "SP": 2.0, "Crit": 4.0, "MAX DUR": 999, "DUR": 999, "Class": "Weapon"},
        "Left Hand": {"Name": "Shadow Cloak", "Effect": "Dodge", "Chance": 50, "Class": "Rune"},
        "Helmet": {},
        "Chestplate": {},
        "Leggings": {},
        "Boots": {},
        "Drops": [{"Name": "Shadow Essence", "Class": "Scroll"}],
    },
    "Stone Golem": {
        "HP": 5000,
        "ATK": 250,
        "DEF": 400,
        "Crit": 5,
        "SP": 10,
        "EXP": 70,
        "Weapon": {"Name": "Granite Fists", "ATK": 2.0, "SP": 0.5, "Crit": 1.5, "MAX DUR": 999, "DUR": 999, "Class": "Weapon"},
        "Left Hand": {"Name": "Stone Shield", "DEF": 5.0, "SP": 0.5, "MAX DUR": 2000, "DUR": 2000, "Class": "Shield"},
        "Helmet": {"Name": "Stone Helmet", "DEF": 3.0, "SP": 0.5, "MAX DUR": 1500, "DUR": 1500, "Class": "Helmet"},
        "Chestplate": {"Name": "Stone Chestplate", "DEF": 5.0, "SP": 0.5, "MAX DUR": 2000, "DUR": 2000, "Class": "Chestplate"},
        "Leggings": {"Name": "Stone Leggings", "DEF": 3.0, "SP": 0.5, "MAX DUR": 1500, "DUR": 1500, "Class": "Leggings"},
        "Boots": {"Name": "Stone Boots", "DEF": 2.0, "SP": 0.5, "MAX DUR": 1000, "DUR": 1000, "Class": "Boots"},
        "Drops": [{"Name": "Stone Core", "Class": "Scroll"}],
    },
    "Vampire Lord": {
        "HP": 4000,
        "ATK": 450,
        "DEF": 200,
        "Crit": 20,
        "SP": 45,
        "EXP": 80,
        "Weapon": {"Name": "Blood Drinker", "ATK": 3.5, "SP": 1.5, "Crit": 3.0, "MAX DUR": 999, "DUR": 999, "Class": "Weapon"},
        "Left Hand": {"Name": "Blood Shield", "DEF": 3.0, "SP": 1.0, "MAX DUR": 1500, "DUR": 1500, "Class": "Shield"},
        "Helmet": {},
        "Chestplate": {"Name": "Noble's Vest", "DEF": 3.0, "SP": 1.5, "MAX DUR": 1200, "DUR": 1200, "Class": "Chestplate"},
        "Leggings": {},
        "Boots": {},
        "Drops": [{"Name": "Blood Essence", "Class": "Scroll"}, {"Name": "Potion of Strength", "Tier": 3, "Effect": 5, "Class": "Potion of Strength", "Cost": 1500}],
    },
}

ADDITIONAL_BOSSES: Dict[str, Dict[str, Any]] = {
    "Dragon King": {
        "HP": 50000,
        "ATK": 3000,
        "DEF": 2000,
        "Crit": 75,
        "SP": 60,
        "EXP": 15000,
        "Weapon": {"Name": "Dragon's Maw", "ATK": 12, "SP": 2, "Crit": 4, "MAX DUR": 8000, "DUR": 8000, "Class": "Weapon"},
        "Left Hand": {"Name": "Dragon Scale Aegis", "DEF": 10, "SP": 2, "MAX DUR": 7500, "DUR": 7500, "Class": "Shield"},
        "Helmet": {"Name": "Dragon Crown", "DEF": 8, "SP": 1, "MAX DUR": 6000, "DUR": 6000, "Class": "Helmet"},
        "Chestplate": {"Name": "Dragon Scale Plate", "DEF": 12, "SP": 1, "MAX DUR": 8000, "DUR": 8000, "Class": "Chestplate"},
        "Leggings": {"Name": "Dragon Leg Guards", "DEF": 8, "SP": 2, "MAX DUR": 6500, "DUR": 6500, "Class": "Leggings"},
        "Boots": {"Name": "Dragon Talons", "DEF": 5, "SP": 3, "MAX DUR": 5500, "DUR": 5500, "Class": "Boots"},
        "Prisms": 10,
    },
    "Lich King": {
        "HP": 40000,
        "ATK": 4000,
        "DEF": 1500,
        "Crit": 100,
        "SP": 80,
        "EXP": 12000,
        "Weapon": {"Name": "Soul Reaper", "ATK": 15, "SP": 1.5, "Crit": 5, "MAX DUR": 7000, "DUR": 7000, "Class": "Weapon"},
        "Left Hand": {"Name": "Necronomicon", "Effect": "Dark Magic", "Chance": 40, "Class": "Rune"},
        "Helmet": {"Name": "Crown of Bones", "DEF": 6, "SP": 1, "MAX DUR": 5000, "DUR": 5000, "Class": "Helmet"},
        "Chestplate": {"Name": "Bone Armor", "DEF": 8, "SP": 1, "MAX DUR": 6000, "DUR": 6000, "Class": "Chestplate"},
        "Leggings": {},
        "Boots": {},
        "Prisms": 8,
    },
}
