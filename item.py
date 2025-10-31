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
    {"name": "铁剑", "desc": "普通的铁剑，提升基础攻击。", "atk": 5, "df": 0, "hp": 0,  "crit": 0.05, "dodge": 0.0,  "slot": "weapon"},
    {"name": "钻石剑", "desc": "钻石打造的剑，看上去像是马赛克组成的。", "atk": 20, "df": 0, "hp": 0,  "crit": 0.2, "dodge": 0.0,  "slot": "weapon"},
    {"name": "断钢神剑", "desc": "湖中仙女打造的神剑。", "atk": 50, "df": 0, "hp": 20,  "crit": 0.5, "dodge": 0.0,  "slot": "weapon"},
    {"name": "钢甲", "desc": "厚重的钢制盔甲，提升防御力。", "atk": 0, "df": 5, "hp": 20, "crit": 0.0,  "dodge": 0.0,  "slot": "armor"},
    {"name": "盾牌", "desc": "厚重的钢制盔甲，提升防御力。", "atk": 0, "df": 5, "hp": 0, "crit": 0.0,  "dodge": 0.0,  "slot": "armor"},
    {"name": "魔法戒指", "desc": "发出微光的戒指，提升暴击与闪避。", "atk": 0, "df": 0, "hp": 10, "crit": 0.10, "dodge": 0.05, "slot": "accessory"},
    {"name": "红宝石戒指", "desc": "镶嵌红宝石的戒指，提升暴击几率。", "atk": 0, "df": 0, "hp": 15, "crit": 0.10,"dodge": 0.00, "slot": "accessory"},
    {"name": "蓝宝石项链", "desc": "纯净蓝宝石制成的项链，提升闪避能力。", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.10, "slot": "accessory"},
    {"name": "黑曜石护符", "desc": "黑曜石雕刻而成的护符，提升攻击力。", "atk": 8, "df": 0, "hp": 0, "crit": 0.05,"dodge": 0.00, "slot": "accessory"},
    {"name": "白银吊坠", "desc": "银质吊坠，散发淡淡光芒，略微提高防御。", "atk": 0, "df": 3, "hp": 10, "crit": 0.00,"dodge": 0.02, "slot": "accessory"},
    {"name": "翡翠耳环", "desc": "翠绿色的耳环，蕴含自然能量。", "atk": 0, "df": 2, "hp": 20, "crit": 0.00, "dodge": 0.05,"slot": "accessory"},
    {"name": "黄金戒指", "desc": "象征财富与力量的戒指，增强攻击与暴击。", "atk": 5, "df": 0, "hp": 5, "crit": 0.08,"dodge": 0.00, "slot": "accessory"},
    {"name": "夜光护符", "desc": "会在黑暗中发光的护符，增加闪避率。", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.12, "slot": "accessory"},
    {"name": "风之挂坠", "desc": "轻盈的风之结晶，提升闪避与速度感。", "atk": 2, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.10, "slot": "accessory"},
    {"name": "烈焰戒指", "desc": "内燃火焰的戒指，提升攻击力与暴击。", "atk": 10, "df": 0, "hp": 0, "crit": 0.10,"dodge": 0.00, "slot": "accessory"},
    {"name": "寒冰吊坠", "desc": "散发寒气的吊坠，强化防御力。", "atk": 0, "df": 6, "hp": 15, "crit": 0.00, "dodge": 0.02,"slot": "accessory"},
    {"name": "暗影耳环", "desc": "吸收光线的黑色耳环，提高闪避。", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.15, "slot": "accessory"},
    {"name": "圣光项链", "desc": "被祝福的圣光项链，全面强化体质。", "atk": 5, "df": 5, "hp": 20, "crit": 0.05,"dodge": 0.05, "slot": "accessory"},
    {"name": "雷鸣戒指", "desc": "雷元素凝结的戒指，强化暴击与攻击。", "atk": 8, "df": 0, "hp": 5, "crit": 0.12,"dodge": 0.00, "slot": "accessory"},
    {"name": "生命护符", "desc": "散发生命气息的护符，提升生命上限。", "atk": 0, "df": 0, "hp": 40, "crit": 0.00,"dodge": 0.00, "slot": "accessory"},
    {"name": "钢铁之环", "desc": "坚固的钢环，强化防御与生命。", "atk": 0, "df": 8, "hp": 20, "crit": 0.00, "dodge": 0.00,"slot": "accessory"},
    {"name": "毒蛇戒指", "desc": "刻有毒蛇花纹的戒指，提升暴击率。", "atk": 3, "df": 0, "hp": 10, "crit": 0.10,"dodge": 0.00, "slot": "accessory"},
    {"name": "月影耳饰", "desc": "受月光祝福的耳饰，提升闪避能力。", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.12, "slot": "accessory"},
    {"name": "龙牙坠饰", "desc": "用龙牙雕刻的坠饰，增加攻击力与防御力。", "atk": 7, "df": 4, "hp": 10, "crit": 0.05,"dodge": 0.02, "slot": "accessory"},
    {"name": "深渊吊坠", "desc": "从深渊取出的奇异饰物，蕴含强大力量。", "atk": 12, "df": 0, "hp": 10, "crit": 0.12,"dodge": 0.00, "slot": "accessory"},
    {"name": "幻影项链", "desc": "佩戴者的身影若隐若现，极大提升闪避。", "atk": 0, "df": 0, "hp": 10, "crit": 0.00,"dodge": 0.18, "slot": "accessory"}
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
    {"name": "生命药水", "desc": "恢复 30 点生命值。", "effect": lambda p: heal_player(p, 30)},
    {"name": "魔力药水", "desc": "恢复 20 点魔力值。", "effect": lambda p: restore_mp(p, 20)},
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
    print(f"{player.name} 学会了新技能：{skill.name}！")

# =======================================
# 掉落逻辑
# =======================================
def generate_loot(event_type="battle"):
    """
    - 'battle'：固定药水 + 1个【装备/技能书】二选一
    - 'chest' ：固定药水 + 2个【装备/技能书】供选择
    - 'final_boss' 或 'dragon'：无普通掉落（巨龙项链单独处理）
    """
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
            "name": f"技能书：{sk['name']}", "desc": sk["desc"],
            "effect": lambda p, s=sk: learn_skill(p, s)
        })

    random.shuffle(candidates)
    loot.extend(candidates[:choice_count])

    if not candidates:
        print("\n提示：你已获得所有装备与技能，当前只可获得药水。")

    return loot

# =======================================
# 巨龙专属奖励（只在击败巨龙时获得）
# =======================================
def apply_dragon_reward(player):
    print("\n=== 你击败了巨龙！ ===")
    print("获得独特装备：巨龙项链（全属性 +20，暴击 +0.1，闪避 +0.1）")

    necklace = Equipment(
        name="巨龙项链",
        desc="镶嵌龙牙的项链，散发古老气息。",
        atk=20, df=20, hp=20, crit=0.10, dodge=0.10,
        slot="accessory"
    )
    print(player.equip(necklace))
