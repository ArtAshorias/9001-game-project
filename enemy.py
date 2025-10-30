# ================================
# enemy.py
# 敌人类模块（两种类型 + 属性随机波动）
# ================================

import random
import time


class Enemy:
    def __init__(self, name, enemy_type, Atk, Def, HP, crit, dodge, skill):
        self.name = name
        self.enemy_type = enemy_type
        self.Atk = Atk
        self.Def = Def
        self.HP = HP
        self.crit = crit
        self.dodge = dodge
        self.skill = skill

    def show_info(self):
        print("\n=== Enemy Info ===")
        print(f"Name: {self.name}")
        print(f"Type: {self.enemy_type}")
        print(f"ATK: {self.Atk}")
        print(f"DEF: {self.Def}")
        print(f"HP: {self.HP}")
        print(f"Crit Rate: {self.crit:.2f}")
        print(f"Dodge Rate: {self.dodge:.2f}")
        print(f"Skill: {self.skill}")
        print("====================")


# 固定模板：只存在两种敌人
ENEMY_TEMPLATES = {
    "Slime": {
        "base_name": "Slime",
        "base_Atk": 5,
        "base_Def": 3,
        "base_HP": 50,
        "base_crit": 0,
        "base_dodge": 0,
        "skill": "",
    },
    "Goblin": {
        "base_name": "Goblin",
        "base_Atk": 8,
        "base_Def": 4,
        "base_HP": 70,
        "base_crit": 0.1,
        "base_dodge": 0.05,
        "skill": "",
    },
}


def generate_random_enemy():
    """从两种模板中随机生成一个敌人，并随机化属性"""
    print("\nA wild enemy appears...")
    time.sleep(1.2)

    # 1. 随机选择敌人类型（Slime or Goblin）
    enemy_type = random.choice(list(ENEMY_TEMPLATES.keys()))
    template = ENEMY_TEMPLATES[enemy_type]

    # 2. 为每个属性添加轻微随机浮动（±20%）
    def randomize(value, variation=0.1):
        """基础属性 ±20% 波动"""
        delta = value * variation
        return int(random.uniform(value - delta, value + delta))

    Atk = randomize(template["base_Atk"])
    Def = randomize(template["base_Def"])
    HP = randomize(template["base_HP"])

    # 3. 直接使用模板中的固定值
    crit = template["crit"]
    dodge = template["dodge"]
    name = template["name"]
    skill = template["skill"]

    # 4. 创建敌人对象
    e = Enemy(
        name=name,
        enemy_type=enemy_type,
        Atk=Atk,
        Def=Def,
        HP=HP,
        crit=crit,
        dodge=dodge,
        skill=template["skill"],
    )

    # 5. 输出结果
    print(f"\nYou have encountered a {e.name}!")
    e.show_info()
    return e
