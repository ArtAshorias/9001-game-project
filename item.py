# =============================
# item.py
# 掉落物品、装备、技能书与特殊奖励
# =============================

import random
from skill_buff import create_skill_from_book, SKILL_BOOKS

# =======================================
# 全局唯一装备池（不含“巨龙项链”，它只在击败巨龙时获得）
# =======================================
available_equipment = [
    {"name": "Iron Sword", "desc": "A simple iron sword that increases basic attack.", "atk": 5, "df": 0, "hp": 0,  "crit": 0.05, "dodge": 0.0,  "slot": "weapon"},
    {"name": "Diamond Sword", "desc": "A sword forged from diamonds, looks like it's made of mosaic.", "atk": 20, "df": 0, "hp": 0,  "crit": 0.2, "dodge": 0.0,  "slot": "weapon"},
    {"name": "Blade of Broken Steel", "desc": "A divine sword forged by the Lady of the Lake.", "atk": 50, "df": 0, "hp": 20,  "crit": 0.5, "dodge": 0.0,  "slot": "weapon"},
    {"name": "Steel Armor", "desc": "Heavy steel armor that increases defense.", "atk": 0, "df": 5, "hp": 20, "crit": 0.0,  "dodge": 0.0,  "slot": "armor"},
    {"name": "Shield", "desc": "A sturdy shield that improves defense.", "atk": 0, "df": 5, "hp": 0, "crit": 0.0,  "dodge": 0.0,  "slot": "armor"},
    {"name": "Magic Ring", "desc": "A glowing ring that enhances critical hit and dodge chance.", "atk": 0, "df": 0, "hp": 10, "crit": 0.10, "dodge": 0.05, "slot": "accessory"},
    {"name": "Ruby Ring", "desc": "A ring embedded with a ruby that boosts critical hit rate.", "atk": 0, "df": 0, "hp": 15, "crit": 0.10,"dodge": 0.00, "slot": "accessory"},
    {"name": "Sapphire Necklace", "desc": "A necklace made of pure sapphire that increases dodge rate.", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.10, "slot": "accessory"},
    {"name": "Obsidian Amulet", "desc": "An amulet carved from obsidian that boosts attack power.", "atk": 8, "df": 0, "hp": 0, "crit": 0.05,"dodge": 0.00, "slot": "accessory"},
    {"name": "Silver Pendant", "desc": "A silver pendant that emits a soft glow, slightly increasing defense.", "atk": 0, "df": 3, "hp": 10, "crit": 0.00,"dodge": 0.02, "slot": "accessory"},
    {"name": "Jade Earrings", "desc": "Green jade earrings infused with natural energy.", "atk": 0, "df": 2, "hp": 20, "crit": 0.00, "dodge": 0.05,"slot": "accessory"},
    {"name": "Golden Ring", "desc": "A ring symbolizing wealth and power, enhances attack and crit.", "atk": 5, "df": 0, "hp": 5, "crit": 0.08,"dodge": 0.00, "slot": "accessory"},
    {"name": "Luminous Amulet", "desc": "An amulet that glows in the dark, increasing dodge rate.", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.12, "slot": "accessory"},
    {"name": "Pendant of Wind", "desc": "A pendant made from wind crystals that enhances dodge and agility.", "atk": 2, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.10, "slot": "accessory"},
    {"name": "Flame Ring", "desc": "A ring imbued with inner flames that increases attack and crit.", "atk": 10, "df": 0, "hp": 0, "crit": 0.10,"dodge": 0.00, "slot": "accessory"},
    {"name": "Frost Pendant", "desc": "A pendant radiating cold air that strengthens defense.", "atk": 0, "df": 6, "hp": 15, "crit": 0.00, "dodge": 0.02,"slot": "accessory"},
    {"name": "Shadow Earrings", "desc": "Black earrings that absorb light, greatly improving dodge.", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.15, "slot": "accessory"},
    {"name": "Necklace of Holy Light", "desc": "A blessed necklace that improves all attributes.", "atk": 5, "df": 5, "hp": 20, "crit": 0.05,"dodge": 0.05, "slot": "accessory"},
    {"name": "Thunder Ring", "desc": "A ring condensed from lightning energy that enhances attack and crit.", "atk": 8, "df": 0, "hp": 5, "crit": 0.12,"dodge": 0.00, "slot": "accessory"},
    {"name": "Amulet of Life", "desc": "An amulet radiating life energy, increasing maximum HP.", "atk": 0, "df": 0, "hp": 40, "crit": 0.00,"dodge": 0.00, "slot": "accessory"},
    {"name": "Ring of Steel", "desc": "A solid steel ring that boosts defense and HP.", "atk": 0, "df": 8, "hp": 20, "crit": 0.00, "dodge": 0.00,"slot": "accessory"},
    {"name": "Viper Ring", "desc": "A ring engraved with a serpent pattern that improves crit rate.", "atk": 3, "df": 0, "hp": 10, "crit": 0.10,"dodge": 0.00, "slot": "accessory"},
    {"name": "Moonshadow Earrings", "desc": "Earrings blessed by moonlight that enhance dodge ability.", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.12, "slot": "accessory"},
    {"name": "Dragon Tooth Pendant", "desc": "A pendant carved from dragon teeth, increases attack and defense.", "atk": 7, "df": 4, "hp": 10, "crit": 0.05,"dodge": 0.02, "slot": "accessory"},
    {"name": "Abyss Pendant", "desc": "A mysterious relic from the abyss containing immense power.", "atk": 12, "df": 0, "hp": 10, "crit": 0.12,"dodge": 0.00, "slot": "accessory"},
    {"name": "Phantom Necklace", "desc": "A necklace that makes the wearer’s figure flicker, greatly improving dodge.", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.18, "slot": "accessory"}
]




# 技能书池：从 SKILL_BOOKS 拷贝一份，避免直接改原表
available_skillbooks = [b.copy() for b in SKILL_BOOKS]


# =======================================
# 药水（可重复）
# =======================================
def heal_player(player, amount):
    old_hp = player.HP
    player.HP = min(player.HP + amount, player.MaxHP)
    print(f"{player.name} 使用生命药水，HP {old_hp} → {player.HP}")

def restore_mp(player, amount):
    old_mp = player.MP
    player.MP = min(player.MP + amount, 100)
    print(f"{player.name} 使用魔力药水，MP {old_mp} → {player.MP}")

potions = [
    {"name": "Health Potion", "desc": "Restores 30 HP.", "effect": lambda p: heal_player(p, 30)},
    {"name": "Mana Potion", "desc": "Restores 20 MP.", "effect": lambda p: restore_mp(p, 20)},
]

# =======================================
# 装备类 + 穿戴
# =======================================
class Equipment:
    def __init__(self, name, desc, atk, df, hp, crit, dodge, slot):
        self.name = name; self.desc = desc
        self.atk = atk; self.df = df; self.hp = hp
        self.crit = crit; self.dodge = dodge
        self.slot = slot

def equip_item(player, item):
    eq = Equipment(item["name"], item["desc"],
                   item["atk"], item["df"], item["hp"],
                   item["crit"], item["dodge"], item["slot"])
    print(player.equip(eq))

def learn_skill(player, book):
    """从技能书原型生成技能，并学习"""
    skill = create_skill_from_book(book)
    player.skill.append(skill)
    print(f"{player.name} has learned a new skill: {skill.name}!")


# =======================================
# 掉落逻辑
# =======================================
def generate_loot(event_type="battle"):
    loot = []
    if event_type in ("final_boss", "dragon"):
        return loot

    # 固定：一瓶药水
    loot.append(random.choice(potions))

    # 候选生成
    choice_count = 1 if event_type == "battle" else 2
    candidates = []

    # 装备候选（唯一）
    if available_equipment:
        eq = random.choice(available_equipment)
        available_equipment.remove(eq)
        candidates.append({
            "name": eq["name"], "desc": eq["desc"],
            "effect": lambda p, e=eq: equip_item(p, e)
        })

    # 技能书候选（唯一）
    if available_skillbooks:
        sk = random.choice(available_skillbooks)
        available_skillbooks.remove(sk)
        candidates.append({
            "name": f"Skill Book：{sk['name']}", "desc": sk["desc"],
            "effect": lambda p, s=sk: learn_skill(p, s)
        })

    random.shuffle(candidates)
    loot.extend(candidates[:choice_count])

    if not candidates:
        print("\nTip: You have obtained all equipment and skills. You can now only receive potions.")

    return loot

# =======================================
# 巨龙专属奖励（只在击败巨龙时获得）
# =======================================
def apply_dragon_reward(player):
    print("\n=== You have defeated the dragon! ===")
    print("You obtained a unique equipment: Dragon Necklace (All stats +20, Crit +0.1, Dodge +0.1)")

    necklace = Equipment(
        name="Dragon Necklace",
        desc="A necklace inlaid with dragon fangs, radiating an ancient aura.",
        atk=20, df=20, hp=20, crit=0.10, dodge=0.10,
        slot="accessory"
    )
    print(player.equip(necklace))
