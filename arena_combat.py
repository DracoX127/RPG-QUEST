"""Shared turn-based combat for RPG QUEST 2.0 (used by Arena and Rotfang Depths)."""
from __future__ import annotations

import copy
import random
import time
from typing import Any, Callable, Dict, Tuple
from ui import console


def run_arena_style_combat(
    stats: Dict[str, Any],
    foe: Dict[str, Any],
    tw: Callable[..., None],
    clr: Callable[[], None],
    ft: Callable[..., None],
) -> Tuple[bool, int]:
    """
    Duel until one fighter falls. Updates stats durability/HP/backpack-in-combat semantics
    identical to legacy arena. Returns (player_won, turns_taken).
    """
    foe_name = foe["name"]
    foe_lvl = foe["lvl"]
    enemyhp = foe["enemyhp"]
    enemystr = foe["enemystr"]
    enemydef = foe["enemydef"]
    enemycrit = foe["enemycrit"]
    enemysp = foe["enemysp"]
    weapon = copy.deepcopy(foe["weapon"])
    shield = copy.deepcopy(foe["shield"])
    helmet = copy.deepcopy(foe["helmet"]) if foe.get("helmet") is not None else None
    chestplate = copy.deepcopy(foe["chestplate"]) if foe.get("chestplate") is not None else None
    legging = copy.deepcopy(foe["legging"]) if foe.get("legging") is not None else None
    boot = copy.deepcopy(foe["boot"]) if foe.get("boot") is not None else None

    dead = False
    fire = False
    effect = 0
    turn = 0
    win = False
    attack = 0
    damage = 0
    yourhp = stats["HP"]
    yourstr = stats["STR"]
    yourdef = stats["DEF"]

    while True:
        if dead:
            tw("You defeated your opponent!")
            time.sleep(1)
            clr()
            win = True
            break
        turn += 1
        dodge = False
        if fire and effect != 0:
            effect -= 1
            wpn_tier = stats["Weapon"].get("Tier", 0)
            console.print("Enemy is burning! They take", 250 + (wpn_tier * 50), "damage!")
            enemyhp -= 250 + (wpn_tier * 50)
            if enemyhp <= 0:
                tw("You defeated your opponent!")
                time.sleep(1)
                clr()
                win = True
                break
        console.print(f"Your HP: {yourhp}")
        console.print("========================\n")
        time.sleep(0.1)
        console.print("1. Attack\n")
        time.sleep(0.1)
        console.print("2. Use Left Hand\n")
        time.sleep(0.1)
        console.print("3. Use Potion\n")
        time.sleep(0.1)
        console.print("4. View Enemy Stats\n")
        time.sleep(0.1)
        console.print("=======================\n")
        time.sleep(0.1)
        try:
            attack = int(console.input("Enter a number: "))
        except ValueError:
            attack = 0
        clr()
        events = [
            "You swing your sword and strike the opponent!",
            "You lunge forward with a fierce attack!",
            "Your blade clashes against their armor, sparks flying!",
            "You feint to the left and slash quickly!",
            "You charge with a powerful overhead strike!",
            "You stab forward, narrowly piercing their guard!",
            "You spin with deadly precision and land a cut!",
            "You bash your opponent with the hilt of your weapon!",
            "Your strike glances off, but you press the attack!",
            "You unleash a flurry of quick strikes!",
            "You slash diagonally, leaving a deep gash!",
            "You thrust with unrelenting force!",
            "You sweep low, striking at their legs!",
            "You hammer down with both hands on your weapon!",
            "You strike twice in rapid succession!",
            "You faint a retreat, then slash suddenly!",
            "You clash blades and overpower your foe!",
            "You swing from the side and knock them off balance!",
            "You leap forward and bring your blade down hard!",
            "You carve across their armor with brutal strength!"
        ]

        miss_events = [
            "You swing wildly, but the opponent dodges!",
            "Your strike misses by an inch!",
            "You stumble forward as your attack whiffs!",
            "The opponent parries and leaves you open!",
            "Your blade cuts only the air!",
            "You charge in, but the enemy sidesteps easily!",
            "Your attack bounces harmlessly off their shield!",
            "You overextend, leaving yourself unbalanced!",
            "The enemy ducks just in time to avoid your swing!",
            "You misjudge the distance and your strike falls short!",
            "Your blow is deflected effortlessly!",
            "You slip as you swing, losing momentum!",
            "The opponent spins away from your attack!",
            "You hit nothing but sparks as your strike glances off!",
            "The enemy blocks and counters swiftly!",
            "You overreach, exposing your guard!",
            "You strike too early, missing completely!",
            "Your weapon lodges into the ground instead of the enemy!",
            "You swing overhead, but they roll aside!",
            "Your attack is easily sidestepped with a smirk!"
        ]

        fire_events = [
            "Your enchanted blade ignites, setting the opponent aflame!",
            "Sparks erupt as your sword burns through their armor!",
            "Flames dance along your weapon, scorching your foe!",
            "Your fiery strike leaves the enemy screaming in pain!",
            "You slash across, and fire trails linger on their wounds!",
            "The blade crackles with heat, searing the opponent's flesh!",
            "A burst of flame explodes from your sword, engulfing them!",
            "You strike true, and fire spreads rapidly across their body!",
            "Your weapon blazes brightly, reducing their guard to ashes!",
            "A single fiery slash sets the battlefield alight!",
            "Fire erupts in a spiral from your swing!",
            "The air burns as your flaming strike lands!",
            "Your weapon scorches their armor to molten slag!",
            "You carve across, flames spreading from the wound!",
            "Heat radiates so strongly the enemy staggers back!",
            "You unleash a flaming arc, searing everything before you!",
            "The flames cling to your foe, refusing to die out!",
            "Your sword explodes in embers on impact!",
            "You burn their shield away with relentless fire!",
            "Your blade leaves a blazing scar across the battlefield!"
        ]

        crit_events = [
            "💥 Critical hit! Your strike shatters the enemy’s defense!",
            "⚡ A devastating blow lands squarely, dealing massive damage!",
            "🔥 You find the perfect opening and unleash a lethal strike!",
            "💢 Your weapon tears through with pinpoint precision!",
            "💀 A brutal critical! The opponent staggers backward in agony!",
            "🔪 You land a vicious slash, doubling the devastation!",
            "⚔️ Your blade finds a weak spot — CRITICAL DAMAGE!",
            "🌟 With flawless timing, you deliver a critical blow!",
            "💣 A thunderous strike smashes through their guard!",
            "👊 Your hit lands with crushing force — a perfect crit!",
            "⚡ Lightning precision! You pierce their core defenses!",
            "💥 A bone-cracking strike leaves them gasping!",
            "🔥 Your attack ignites into a fiery explosion of damage!",
            "💀 Death blow! The enemy collapses under your might!",
            "⚔️ You unleash a flawless strike at their weakest point!",
            "🔪 A razor-sharp slash deals double the carnage!",
            "🌟 Perfect timing! You devastate your opponent!",
            "💣 The ground shakes from the force of your crit!",
            "💢 The enemy reels, crushed by your critical assault!",
            "👊 Your strike echoes like thunder, shattering their resolve!"
        ]

        if attack == 1 or attack == 2:
            if attack == 1:
                miss = random.randint(1, 200)
                if miss < 180 - enemysp:
                    if stats["Weapon"]["DUR"] < 0:
                        tw("Your sword has no more durability! Your enemy charges at you while you are unarmed. STRIKE! You lost...")
                        time.sleep(1)
                        clr()
                        break
                    if "Fire Aspect" in stats["Weapon"]["Name"]:
                        fires = random.randint(1, 100)
                        wpn_tier = stats["Weapon"].get("Tier", 0)
                        if fires <= 50 + (wpn_tier * 8):
                            fire = True
                            event = random.choice(fire_events)
                            tw(event)
                            time.sleep(1)
                            clr()
                    crit = random.randint(1, 100)
                    if crit <= stats["Crit"]:
                        damage = yourstr * stats["Weapon"]["ATK"] * 2
                        event = random.choice(crit_events) + f" You dealt {damage} damage!"
                    else:
                        damage = yourstr * stats["Weapon"]["ATK"]
                        event = random.choice(events) + f" You dealt {damage} damage!"
                    block = random.randint(1, 100)
                    if block <= 20:
                        console.print("blocked!")
                        if foe_lvl < 100:
                            block = shield["DEF"]
                            if helmet is not None:
                                block += helmet["DEF"]
                            if legging is not None:
                                block += legging["DEF"]
                            if boot is not None:
                                block += boot["DEF"]
                            if chestplate is not None:
                                block += chestplate["DEF"]
                        else:
                            if block <= 50:
                                damage = 0
                    if damage - (enemydef * block) < 0:
                        damage = 0
                    else:
                        damage -= enemydef * block
                    enemyhp -= damage
                    tw(event)
                    stats["Weapon"]["DUR"] -= 1
                    time.sleep(1.9999999999)
                    clr()
                else:
                    event = random.choice(miss_events)
                    tw(event)
                    time.sleep(1)
                    clr()
            shield_events = [
                "You slam your shield forward, rattling the enemy’s teeth!",
                "With a mighty shove, your shield smashes into their chest!",
                "You bash them aside, knocking the wind out of their lungs!",
                "The shield crashes into their jaw, sending them reeling!",
                "You charge forward, shield-first, and crush their guard!",
                "Your shield collides with brutal force, staggering your foe!",
                "You feint, then slam your shield into their ribs!",
                "With a deafening clang, your shield bashes through!",
                "You ram your shield edge-first, cutting into their flesh!",
                "You smash their weapon arm with a crushing shield strike!",
                "The shield connects, stunning your opponent in place!",
                "You slam your shield downward, pinning them to the ground!",
                "You drive your shield into their gut, making them double over!",
                "Your shield strike knocks the enemy sprawling to the dirt!",
                "With raw strength, you bowl them over using your shield!",
                "The edge of your shield slams across their temple!",
                "You bash them backward, their defenses crumbling!",
                "A sharp shield thrust knocks the enemy off balance!",
                "You spin and strike with the back of your shield!",
                "Your shield collides like a hammer, ringing in their ears!"
            ]
            if attack == 2:
                if stats["Left Hand"]["Class"] == "Shield":
                    tw(random.choice(shield_events))
                    atk_mult = random.uniform(2, 3.5)
                    ft(f"You deal {stats['STR'] * atk_mult}")
                    enemyhp -= yourstr * atk_mult
                    time.sleep(1)
                    clr()
                elif stats["Left Hand"]["Class"] == "Rune":
                    rune_events = [
                        "You raise the rune in your left hand — it glows and releases a surge of power!",
                        "The rune thrums violently, unleashing waves of energy around you!",
                        "Arcane light bursts from the rune, blinding your opponent momentarily!",
                        "You clutch the rune tight, and it flares with raw magical force!",
                        "The rune in your palm hums, scattering sparks into the air!",
                        "A beam of pure energy erupts from the rune, searing the battlefield!",
                        "You press the rune forward, and runic chains lash out at your enemy!",
                        "The rune glows crimson, amplifying your next attack with fiery strength!",
                        "You lift the rune skyward, summoning a shockwave of arcane energy!",
                        "Runes spiral in the air from your hand as the artifact activates!",
                        "The rune pulses, forming a protective barrier around you!",
                        "You channel your will through the rune — a burst of light pushes foes back!",
                        "Mystic flames erupt from the rune, scorching everything nearby!",
                        "You hold the rune high, and it summons a torrent of lightning!",
                        "The rune vibrates in your grip, enhancing your reflexes!",
                        "Your rune shines with divine radiance, weakening your enemy’s resolve!",
                        "You slam the rune into the ground — cracks of glowing energy spread outward!",
                        "The rune emits an eerie blue light, chilling the air to frost!",
                        "Dark tendrils spill from the rune, siphoning energy from your foe!",
                        "You grip the rune tightly — it bursts, unleashing unstoppable chaos!"
                    ]
                    dodge = True
                    tw(random.choice(rune_events))
                    time.sleep(1.5)
                    clr()
                elif stats["Left Hand"]["Class"] == "Potion of Healing":
                    healing_potion_events = [
                        "You uncork the potion and drink deeply — your wounds begin to close!",
                        "The glowing liquid restores your vitality as you swallow it down!",
                        "You gulp the potion and feel warmth spreading through your body!",
                        "The bitter taste fades quickly as your injuries knit back together!",
                        "You drink the potion and strength surges back into your muscles!",
                        "Golden light pulses through your veins as the potion heals you!",
                        "You tilt the vial back and your heartbeat steadies instantly!",
                        "The potion soothes your pain as it flows down your throat!",
                        "You chug the potion and your vision sharpens once more!",
                        "With a quick drink, your stamina returns in a rush!",
                        "The potion's glow fades as it restores your health!",
                        "You take a long drink and your breathing becomes steady again!",
                        "A surge of energy floods you as the potion’s magic takes hold!",
                        "Your wounds begin to seal the moment the potion touches your lips!",
                        "You drink the liquid fire, but it heals as it burns!",
                        "The potion leaves a trail of warmth as your injuries fade!",
                        "You down the potion and vitality floods your body!",
                        "The vial empties and golden sparks mend your broken flesh!",
                        "You drink swiftly, and a soothing calm washes over you!",
                        "The healing potion restores your strength in moments!"
                    ]
                    tw(random.choice(healing_potion_events))
                    tw(f"You healed for {stats['Left Hand']['Effect']} HP!")
                    yourhp += stats["Left Hand"]["Effect"]
                elif stats["Left Hand"]["Class"] == "Potion of Strength":
                    strength_potion_events = [
                        "You uncork the potion and drink deeply — your muscles surge with newfound power!",
                        "The fiery liquid courses through your veins, amplifying your strength!",
                        "You gulp the potion and feel raw power radiating from your limbs!",
                        "The bitter taste fades quickly as your muscles bulge with energy!",
                        "You drink the potion and your strikes feel unstoppable!",
                        "Red light pulses through your body as the potion enhances your might!",
                        "You tilt the vial back and a wave of strength floods over you!",
                        "The potion invigorates you as it flows down your throat!",
                        "You chug the potion and your arms feel like steel!",
                        "With a quick drink, your power multiplies in an instant!",
                        "The potion's glow intensifies as it fuels your strength!",
                        "You take a long drink and your muscles tense with energy!",
                        "A surge of raw power fills you as the potion's magic takes hold!",
                        "Your strikes become devastating the moment the potion touches your lips!",
                        "You drink the liquid fire, and it ignites your fighting spirit!",
                        "The potion leaves a trail of heat as your strength swells!",
                        "You down the potion and feel invincible!",
                        "The vial empties and red sparks ignite your muscles!",
                        "You drink swiftly, and a fierce power surges through you!",
                        "The strength potion transforms you into a powerhouse!"
                    ]
                    tw(random.choice(strength_potion_events))
                    tw(f"You gained {stats['Left Hand']['Effect']} STR!")
                    yourstr += stats["Left Hand"]["Effect"]
                elif stats["Left Hand"]["Class"] == "Potion of Defense":
                    defense_potion_events = [
                        "You uncork the potion and drink deeply — your skin hardens like armor!",
                        "The shimmering liquid flows through you, bolstering your defenses!",
                        "You gulp the potion and feel an impenetrable shield forming around you!",
                        "The bitter taste fades quickly as your body toughens!",
                        "You drink the potion and your resilience feels unbreakable!",
                        "Blue light pulses through your veins as the potion fortifies you!",
                        "You tilt the vial back and a wave of protection envelops you!",
                        "The potion strengthens you as it flows down your throat!",
                        "You chug the potion and your defenses feel rock-solid!",
                        "With a quick drink, your durability increases dramatically!",
                        "The potion's glow intensifies as it reinforces your body!",
                        "You take a long drink and your skin feels like steel!",
                        "A surge of fortitude fills you as the potion's magic takes hold!",
                        "Your defenses become formidable the moment the potion touches your lips!",
                        "You drink the liquid fire, and it hardens your resolve!",
                        "The potion leaves a trail of cool energy as your defenses rise!",
                        "You down the potion and feel invincible!",
                        "The vial empties and blue sparks fortify your body!",
                        "You drink swiftly, and a sturdy shield forms around you!",
                        "The defense potion transforms you into a fortress!"
                    ]
                    tw(random.choice(defense_potion_events))
                    tw(f"You gained {stats['Left Hand']['Effect']} DEF!")
                    yourdef += stats["Left Hand"]["Effect"]
            if enemyhp <= 0:
                death_events = [
                    "With a final, desperate gasp, your opponent collapses to the ground, defeated.",
                    "Your enemy falls to their knees, clutching their wounds as they succumb to defeat.",
                    "With a last, shuddering breath, your foe crumples to the earth, vanquished.",
                    "Your opponent staggers back, eyes wide with shock, before falling lifelessly.",
                    "With a heavy thud, your enemy hits the ground, their fight finally over.",
                    "Your foe's knees buckle, and they collapse, the fight drained from their body.",
                    "With a final, pained cry, your opponent falls, the battle lost.",
                    "Your enemy's eyes flutter shut as they drop to the ground, defeated.",
                    "Their weapon slips from their hand as they collapse, strength leaving them for good.",
                    "With one last stagger, your opponent collapses in the dirt, breath gone.",
                    "A hollow gasp escapes as your foe crashes down, utterly beaten.",
                    "Their body gives way, and they crumble into the dust of the battlefield.",
                    "The enemy’s guard falters, and they drop with a dull, final thud.",
                    "Eyes dimming, your opponent slumps forward and hits the ground motionless.",
                    "With one final cry, they fall, echoing silence following soon after.",
                    "The fight leaves their body, and they collapse in a heap of defeat.",
                    "Their knees buckle and they collapse face-first, the battle over.",
                    "Your foe lets out a final breath, then falls limp upon the ground.",
                    "They sway for a moment, then fall like a toppled statue, lifeless.",
                    "With trembling arms failing, they sink to the floor, conquered at last.",
                    "Your opponent’s weapon clatters to the ground as they fall, the end upon them."
                ]
                tw(random.choice(death_events))
                time.sleep(1)
                clr()
                win = True
                dead = True
        elif attack == 3:
            for item in stats["Backpack"]:
                if item["Class"] == "Potion of Healing" or item["Class"] == "Potion of Strength" or item["Class"] == "Potion of Defense":
                    console.print(f"Name: {item.get('Name')}")
                    console.print(f"Effect: {item.get('Effect')}")
                    console.print(f"Tier: {item.get('Tier')}\n")
                potion = console.input("Which potion would you like to use(Capitalization Counts): ")
                clr()
                found = False
                for i, item in enumerate(stats["Backpack"]):
                    if item["Name"] == potion:
                        found = True
                        if item["Class"] == "Potion of Healing":
                            healing_potion_events = [
                                "You uncork the potion and drink deeply — your wounds begin to close!",
                                "The glowing liquid restores your vitality as you swallow it down!",
                                "You gulp the potion and feel warmth spreading through your body!",
                                "The bitter taste fades quickly as your injuries knit back together!",
                                "You drink the potion and strength surges back into your muscles!",
                                "Golden light pulses through your veins as the potion heals you!",
                                "You tilt the vial back and your heartbeat steadies instantly!",
                                "The potion soothes your pain as it flows down your throat!",
                                "You chug the potion and your vision sharpens once more!",
                                "With a quick drink, your stamina returns in a rush!",
                                "The potion's glow fades as it restores your health!",
                                "You take a long drink and your breathing becomes steady again!",
                                "A surge of energy floods you as the potion's magic takes hold!",
                                "Your wounds begin to seal the moment the potion touches your lips!",
                                "You drink the liquid fire, but it heals as it burns!",
                                "The potion leaves a trail of warmth as your injuries fade!",
                                "You down the potion and vitality floods your body!",
                                "The vial empties and golden sparks mend your broken flesh!",
                                "You drink swiftly, and a soothing calm washes over you!",
                                "The healing potion restores your strength in moments!"
                            ]
                            tw(random.choice(healing_potion_events))
                            tw(f"You healed for {item['Effect']} HP!")
                            yourhp += item["Effect"]
                        elif item["Class"] == "Potion of Strength":
                            strength_potion_events = [
                                "You uncork the potion and drink deeply — your muscles surge with newfound power!",
                                "The fiery liquid courses through your veins, amplifying your strength!",
                                "You gulp the potion and feel raw power radiating from your limbs!",
                                "The bitter taste fades quickly as your muscles bulge with energy!",
                                "You drink the potion and your strikes feel unstoppable!",
                                "Red light pulses through your body as the potion enhances your might!",
                                "You tilt the vial back and a wave of strength floods over you!",
                                "The potion invigorates you as it flows down your throat!",
                                "You chug the potion and your arms feel like steel!",
                                "With a quick drink, your power multiplies in an instant!",
                                "The potion's glow intensifies as it fuels your strength!",
                                "You take a long drink and your muscles tense with energy!",
                                "A surge of raw power fills you as the potion's magic takes hold!",
                                "Your strikes become devastating the moment the potion touches your lips!",
                                "You drink the liquid fire, and it ignites your fighting spirit!",
                                "The potion leaves a trail of heat as your strength swells!",
                                "You down the potion and feel invincible!",
                                "The vial empties and red sparks ignite your muscles!",
                                "You drink swiftly, and a fierce power surges through you!",
                                "The strength potion transforms you into a powerhouse!"
                            ]
                            tw(random.choice(strength_potion_events))
                            tw(f"You gained {item['Effect']} STR!")
                            yourstr += item["Effect"]
                        elif item["Class"] == "Potion of Defense":
                            defense_potion_events = [
                                "You uncork the potion and drink deeply — your skin hardens like armor!",
                                "The shimmering liquid flows through you, bolstering your defenses!",
                                "You gulp the potion and feel an impenetrable shield forming around you!",
                                "The bitter taste fades quickly as your body toughens!",
                                "You drink the potion and your resilience feels unbreakable!",
                                "Blue light pulses through your veins as the potion fortifies you!",
                                "You tilt the vial back and a wave of protection envelops you!",
                                "The potion strengthens you as it flows down your throat!",
                                "You chug the potion and your defenses feel rock-solid!",
                                "With a quick drink, your durability increases dramatically!",
                                "The potion's glow intensifies as it reinforces your body!",
                                "You take a long drink and your skin feels like steel!",
                                "A surge of fortitude fills you as the potion's magic takes hold!",
                                "Your defenses become formidable the moment the potion touches your lips!",
                                "You drink the liquid fire, and it hardens your resolve!",
                                "The potion leaves a trail of cool energy as your defenses rise!",
                                "You down the potion and feel invincible!",
                                "The vial empties and blue sparks fortify your body!",
                                "You drink swiftly, and a sturdy shield forms around you!",
                                "The defense potion transforms you into a fortress!"
                            ]
                            tw(random.choice(defense_potion_events))
                            tw(f"You gained {item['Effect']} DEF!")
                            yourdef += item["Effect"]
                        del stats["Backpack"][i]
                        time.sleep(1.5)
                        clr()
                if not found:
                    tw("You don't have that potion!")
                    time.sleep(1)
                    clr()
        elif attack == 4:
            tw(f"Enemy Level: {foe_lvl}")
            tw(f"Enemy HP: {enemyhp}")
            tw(f"Enemy STR: {enemystr}")
            tw(f"Enemy DEF: {enemydef}")
            tw(f"Enemy CRIT: {enemycrit}%")
            tw(f"Enemy SP: {enemysp}")
            tw(f"Enemy Weapon: {weapon['Name']} | ATK: {weapon['ATK']} | DUR: {weapon['DUR']}/{weapon['MAX DUR']}")
            if chestplate is not None:
                tw(f"Enemy Chestplate: {chestplate['Name']} | DEF: {chestplate['DEF']} | SP: {chestplate['SP']} | DUR: {chestplate['DUR']}/{chestplate['MAX DUR']}")
            else:
                tw("Enemy Chestplate: None")
            if helmet is not None:
                tw(f"Enemy Helmet: {helmet['Name']} | DEF: {helmet['DEF']} | SP: {helmet['SP']} | DUR: {helmet['DUR']}/{helmet['MAX DUR']}")
            else:
                tw("Enemy Helmet: None")
            if legging is not None:
                tw(f"Enemy Leggings: {legging['Name']} | DEF: {legging['DEF']} | SP: {legging['SP']} | DUR: {legging['DUR']}/{legging['MAX DUR']}")
            else:
                tw("Enemy Leggings: None")
            if boot is not None:
                tw(f"Enemy Boots: {boot['Name']} | DEF: {boot['DEF']} | SP: {boot['SP']} | DUR: {boot['DUR']}/{boot['MAX DUR']}")
            else:
                tw("Enemy Boots: None")
            tw(f"Enemy Shield: {shield['Name']} | DEF: {shield['DEF']} | SP: {shield['SP']} | DUR: {shield['DUR']}/{shield['MAX DUR']}")
            hi = console.input("Press Enter to continue: ")
            if hi is not None:
                time.sleep(0)
            clr()
        time.sleep(1)
        clr()
        tw("Enemy's Turn!")
        time.sleep(0.4)
        clr()
        for _i in range(random.randint(1, 3)):
            time.sleep(0.3)
            clr()
            console.print("Choosing action .")
            time.sleep(0.3)
            clr()
            console.print("Choosing action ..")
            time.sleep(0.3)
            clr()
            console.print("Choosing action ...")
        time.sleep(0.3)
        clr()
        enemy_attack = random.randint(1, 2)
        if enemy_attack == 1:
            incoming_enemy_damage = enemystr * weapon["ATK"]
            damage = incoming_enemy_damage
            if dodge:
                chance = random.randint(1, 100)
                if chance <= 70:
                    dodge_events = [
                        "You nimbly dodge the enemy's attack, evading harm!",
                        "With swift reflexes, you sidestep the incoming strike!",
                        "You duck under the enemy's blow, avoiding damage!",
                        "You leap aside just in time, the attack missing you completely!",
                        "You roll away from the enemy's swing, escaping unscathed!",
                        "You twist your body, letting the attack sail past you!",
                        "You step back quickly, the enemy's weapon cutting through empty air!",
                        "You parry the attack with a quick movement, avoiding injury!",
                        "You leap to the side, the enemy's strike hitting nothing but air!",
                        "You spin away from the blow, narrowly avoiding harm!",
                        "You slide to the side, the enemy's attack missing you entirely!",
                        "You vault over the enemy's strike, landing safely out of harm's way!",
                        "You duck and weave, the attack failing to connect!",
                        "You sidestep the enemy's blow with practiced ease!",
                        "You leap back just in time, the attack grazing past you!",
                        "You twist away from the strike, avoiding any damage!",
                        "You roll under the enemy's swing, escaping harm!",
                        "You step aside, the attack cutting through empty space!",
                        "You parry the blow with a quick motion, avoiding injury!",
                        "You leap to the side, the enemy's strike missing you completely!"
                    ]
                    tw(random.choice(dodge_events))
                    time.sleep(1)
                    clr()
            if stats.get("Left Hand") and stats["Left Hand"].get("Class") == "Shield":
                lh = stats["Left Hand"]
                divine_full_block = False
                if "Divine Guard" in lh.get("Name", ""):
                    if random.randint(1, 100) <= 30 + (lh.get("Tier", 0) * 10):
                        divine_shield_events = [
                            "The enemy's attack bounces off your divine shield, leaving you unharmed!",
                            "With a radiant glow, your divine shield repels the enemy's strike!",
                            "The foe's weapon shatters against your divine shield, protecting you completely!",
                            "Your divine shield emits a blinding light, causing the enemy's attack to miss!",
                            "The enemy's blow is absorbed by your divine shield, leaving you unscathed!",
                            "Your divine shield glows with holy power, deflecting the enemy's strike!",
                            "The foe's weapon is rendered useless against your divine shield!",
                            "Your divine shield radiates energy, nullifying the enemy's attack!",
                            "The enemy's blow is stopped cold by the strength of your divine shield!",
                            "Your divine shield shines brightly, causing the enemy's strike to falter!"
                        ]
                        tw(random.choice(divine_shield_events))
                        time.sleep(1)
                        clr()
                        divine_full_block = True
                        damage = 0
                if not divine_full_block:
                    block = 0
                    if "Divine Guard" not in lh.get("Name", ""):
                        block_chance = random.randint(1, 100)
                        if block_chance <= 20:
                            npc_shield_events = [
                                "The enemy slams their weapon against your shield, rattling your bones!",
                                "With a mighty strike, the foe's weapon crashes into your shield!",
                                "The enemy's blow pounds against your shield, sending shockwaves through you!",
                                "Your shield takes the brunt of the enemy's powerful strike!",
                                "The foe's weapon clangs loudly as it hits your shield!",
                                "You brace yourself as the enemy's attack smashes into your shield!",
                                "The enemy's blow reverberates through your shield, testing your endurance!",
                                "Your shield absorbs the force of the enemy's heavy strike!",
                                "The foe's weapon slams against your shield with a deafening crash!",
                                "You grit your teeth as the enemy's attack pounds on your shield!"
                            ]
                            tw(random.choice(npc_shield_events))
                            block = lh["DEF"]
                    if stats["Helmet"] != {}:
                        block += stats["Helmet"]["DEF"]
                        stats["Helmet"]["DUR"] -= 1
                        if stats["Helmet"]["DUR"] < 0:
                            tw("Your helmet has broken! You are now unprotected.")
                            time.sleep(1)
                            clr()
                            stats["Helmet"] = {}
                    if stats["Chestplate"] != {}:
                        block += stats["Chestplate"]["DEF"]
                        stats["Chestplate"]["DUR"] -= 1
                        if stats["Chestplate"]["DUR"] < 0:
                            tw("Your chestplate has broken! You are now unprotected.")
                            time.sleep(1)
                            clr()
                            stats["Chestplate"] = {}
                    if stats["Leggings"] != {}:
                        block += stats["Leggings"]["DEF"]
                        stats["Leggings"]["DUR"] -= 1
                        if stats["Leggings"]["DUR"] < 0:
                            tw("Your leggings have broken! You are now unprotected.")
                            time.sleep(1)
                            clr()
                            stats["Leggings"] = {}
                    if stats["Boots"] != {}:
                        block += stats["Boots"]["DEF"]
                        stats["Boots"]["DUR"] -= 1
                        if stats["Boots"]["DUR"] < 0:
                            tw("Your boots have broken! You are now unprotected.")
                            time.sleep(1)
                            clr()
                            stats["Boots"] = {}
                    mitigated = incoming_enemy_damage - yourdef * block
                    damage = 0 if mitigated < 0 else mitigated
                stats["Left Hand"]["DUR"] -= 1
                time.sleep(1)
                clr()
                if stats["Left Hand"]["DUR"] < 0:
                    tw("Your shield has broken! You are now unprotected.")
                    time.sleep(1)
                    clr()
                    stats["Left Hand"] = {}
            yourhp -= damage
            tw(f"The enemy dealt {damage} damage!")
            time.sleep(1)
            clr()
            if yourhp <= 0:
                death_pe = [
                    "With a final, desperate gasp, you collapse to the ground, defeated.",
                    "You fall to your knees, clutching your wounds as you succumb to defeat.",
                    "With a last, shuddering breath, you crumple to the earth, vanquished.",
                    "You stagger back, eyes wide with shock, before falling lifelessly.",
                    "With a heavy thud, you hit the ground, your fight finally over.",
                    "Your knees buckle, and you collapse, the fight drained from your body.",
                    "With a final, pained cry, you fall, the battle lost.",
                    "Your eyes flutter shut as you drop to the ground, defeated.",
                    "Your weapon slips from your hand as you collapse, strength leaving you for good.",
                    "With one last stagger, you collapse in the dirt, breath gone.",
                    "A hollow gasp escapes as you crash down, utterly beaten.",
                    "Your body gives way, and you crumble into the dust of the battlefield.",
                    "Your guard falters, and you drop with a dull, final thud.",
                    "Eyes dimming, you slump forward and hit the ground motionless.",
                    "With one final cry, you fall, echoing silence following soon after.",
                    "The fight leaves your body, and you collapse in a heap of defeat.",
                    "Your knees buckle and you collapse face-first, the battle over.",
                    "You let out a final breath, then fall limp upon the ground.",
                    "You sway for a moment, then fall like a toppled statue, lifeless.",
                    "With trembling arms failing, you sink to the floor, conquered at last."
                ]
                tw(random.choice(death_pe))
                time.sleep(1)
                clr()
                break

    stats["HP"] = max(0, yourhp)
    return win, turn
