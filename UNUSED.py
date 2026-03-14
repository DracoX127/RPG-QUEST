def chatbot(stats):
    # Load model
    from gpt4all import GPT4All
    import re
    import json
    model_path = "/Users/yapingwu/Models/llama-3.2-1b-instruct.gguf"
    model = GPT4All(model_path, allow_download=False)

    # Convert full stats dict into a readable string for context
    stats_context = json.dumps(stats, indent=2)

    print("🤖 RPG QUEST AI Assistant is now active!")
    print(f"Loaded player: {stats['Name']} (Lvl {stats['Lvl']})")
    print("Type 'exit' to quit chatbot.\n")

    combat_tips = [
        "Always check your weapon's durability before battle.",
        "Use shields to reduce incoming damage.",
        "Enchant weapons with Sharpness or Thorns for extra damage.",
        "Fire Aspect deals burn damage over time.",
        "Higher level unlocks stronger enchantments and weapons.",
        "Stack buffs wisely; don’t waste enchantments on unused items.",
        "Use Protection enchantments when health is low.",
        "Attack strategically; timing matters more than spamming.",
        "Check enemy weaknesses to maximize damage.",
        "Switch weapons based on enemy type.",
        "Keep spare healing items in your backpack.",
        "Learn enemy attack patterns before engaging.",
        "Use ranged attacks when possible to avoid damage.",
        "Keep an eye on your durability mid-battle.",
        "Upgrade weapons before tackling high-level bosses.",
        "Don’t forget elemental weaknesses (fire, frost, etc.).",
        "Retreat if enemies are too strong, then return stronger.",
        "Use your shield to block heavy hits.",
        "Equip armor sets that boost defense stats for survival."
    ]

    enchanting_tips = [
        "Celestium Prisms are required to enchant items.",
        "Lvl 25 enchantments cost 1 Prism, Lvl 60 cost 2, Lvl 100 cost 3.",
        "Weapon enchantments: Sharpness increases ATK, Thorns rebounds damage, Unbreaking boosts durability.",
        "Shield enchantments: Protection increases DEF, Unbreaking boosts durability.",
        "Armor enchantments: Protection, Heartforge, FrostGuard add defensive perks.",
        "Fire Protection reduces fire damage from enemies.",
        "Divine Guard shields absorb heavy damage.",
        "Looting enchantments increase item drops.",
        "Unbreaking extends item lifespan.",
        "Higher-level enchantments need higher player levels.",
        "Check the enchantment cost before applying.",
        "Some enchantments only apply to specific item types.",
        "Mix and match enchantments for best effects.",
        "Save Prisms for high-level gear upgrades.",
        "Enchant low-level items to boost early gameplay.",
        "Rare enchantments can drastically improve combat stats.",
        "Enchantment progress can be checked at the Starlight Armory.",
        "Timing matters: some enchantments take longer to complete.",
        "Lvl 100 enchantments are very powerful but costly.",
        "Plan which item to enchant first based on your playstyle."
    ]

    shop_tips = [
        "Always check shop prices before buying items.",
        "Buy healing items regularly to avoid running out mid-quest.",
        "Some shops sell rare materials needed for high-level enchantments.",
        "Save gold for powerful weapons and armor upgrades.",
        "Check item stats carefully before purchasing.",
        "Compare items in your backpack with shop items.",
        "High-level items may have prerequisites or level requirements.",
        "Shops restock after certain in-game events.",
        "Trading with NPCs can unlock hidden gear.",
        "Don’t overspend on low-level items.",
        "Save currency for boss battle preparations.",
        "Some items are seasonal or limited-time only.",
        "Purchase shields if you struggle with defense.",
        "Buy enchantment materials in bulk to save trips.",
        "Check for discounted items or special offers.",
        "Focus on items that complement your gear set.",
        "Upgrade weapons via shops before tackling hard dungeons.",
        "Shops sometimes have quest-exclusive items.",
        "Plan purchases based on upcoming battles.",
        "Always leave some gold as emergency funds."
    ]

    trading_tips = [
        "Trade wisely; always know the value of your items.",
        "Rare items can fetch higher value when trading.",
        "Check both sides of the trade for fair deals.",
        "Trading weapons can improve combat efficiency.",
        "Exchange duplicate items for resources you need.",
        "Negotiate with NPCs to get better deals.",
        "Use trading to acquire enchantment materials.",
        "Don’t trade away essential gear accidentally.",
        "Some trades are one-time-only; plan carefully.",
        "Trading can unlock rare armor or weapons.",
        "High-level players often have better trade options.",
        "Save tradeable items for crucial moments.",
        "Track item rarity before trading.",
        "Trade with multiple NPCs to find the best deal.",
        "Avoid trading consumables you will need soon.",
        "Upgrade your items first to get maximum value in trade.",
        "Some NPCs offer unique trades only after quests.",
        "Trading can help balance your inventory space.",
        "Keep high-value items until you need the resources.",
        "Trade strategically to improve your combat or enchantment options."
    ]

    repairing_tips = [
        "Always repair weapons and armor before big battles.",
        "Use Diamonds to repair items at the Obsidian Anvil.",
        "Level 1 repair restores 20% durability.",
        "Level 2 repair restores 50% durability.",
        "Level 3 repair restores 100% durability.",
        "Repair costs scale with the repair level.",
        "Don’t wait until items break completely to repair.",
        "Check durability of all gear before quests.",
        "Focus repairs on weapons and armor you use most.",
        "Repairing boosts longevity of rare items.",
        "Use the right level of repair based on available Diamonds.",
        "Save Diamonds for high-level gear repairs.",
        "Repairing takes time; plan accordingly.",
        "Some repairs are only possible if you have enough Diamonds.",
        "Low-level repairs can still be helpful in emergencies.",
        "High-level repairs maximize battle efficiency.",
        "Track repair progress visually at the anvil interface.",
        "Repair before enchanting for best results.",
        "Broken items reduce combat effectiveness significantly.",
        "Combine repairs and enchantments for ultimate gear."
    ]

    tip_categories = {
        "combat": combat_tips,
        "enchanting": enchanting_tips,
        "shop": shop_tips,
        "trading": trading_tips,
        "repairing": repairing_tips
    }

    tip_indices = {cat: 0 for cat in tip_categories}

    def get_tips(category, n=1):
        if category not in tip_categories:
            return "Sorry, I don't have tips for that category."
        tips_list = tip_categories[category]
        idx = tip_indices[category]
        tips = []
        for _ in range(n):
            tips.append(tips_list[idx])
            idx = (idx + 1) % len(tips_list)
        tip_indices[category] = idx
        return "\n".join(tips)

    with model.chat_session() as session:
        while True:
            user_input = input(f"{stats['Name']}: ").strip().lower()
            if user_input in ["exit", "quit"]:
                print("Bot: Farewell, adventurer! 🐉")
                break

            tip_request = re.search(r'(\d*)\s*(combat|enchanting|shop|trading|repairing)\s*tips?', user_input)
            if tip_request:
                n = int(tip_request.group(1)) if tip_request.group(1).isdigit() else 1
                category = tip_request.group(2)
                print("Bot:", get_tips(category, n))
                continue

            prompt = f"""
You are an RPG game assistant. You have full access to the player's stats and items:
{stats_context}
Always respond with playful flair, using emojis and a friendly tone.
Don't explain reasoning unless asked. Keep answers concise and relevant to the game.
User: {user_input}
don't create any scenarios outside of RPG QUEST game.
"""

            response = session.generate(prompt, max_tokens=200)
            print("Bot:", response.text if hasattr(response, "text") else str(response))
