# =============================
# player.py
# 玩家类与角色创建逻辑（核心）
# =============================

import random
from item import Equipment


class Player:
    """玩家类，包含属性、装备、技能、状态等"""
    def __init__(self, name, Profession, Atk, HP, MP, Def, crit, dodge, skill):
        self.name = name
        self.Profession = Profession
        self.Atk = Atk
        self.HP = HP
        self.MaxHP = HP
        self.MP = MP
        self.MaxMP = MP
        self.Def = Def
        self.crit = crit
        self.dodge = dodge
        self.skill = skill  # 技能列表

        # 装备与背包系统
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.accessories = []  # 可装备多个饰品
        self.steps = 0

    # ==========================================================
    # 装备方法
    # ==========================================================
    def equip(self, eq: Equipment):
        """装备武器、防具或饰品"""
        if eq.slot == "weapon":
            self.weapon = eq
            result = f"Equipped weapon: {eq.name}"
        elif eq.slot == "armor":
            self.armor = eq
            result = f"Equipped armor: {eq.name}"
        elif eq.slot == "accessory":
            self.accessories.append(eq)
            result = f"Equipped accessory: {eq.name}"
        else:
            return "Unknown equipment type."

        # 装备后立即刷新属性上限（暴击/闪避最大为1.0）
        self._limit_stats()
        return result

    # ==========================================================
    # 计算实际属性
    # ==========================================================
    def effective_stats(self):
        """计算装备与饰品叠加后的有效属性"""
        atk = self.Atk
        df = self.Def
        hp_bonus = 0
        crit = self.crit
        dodge = self.dodge

        # 武器加成
        if self.weapon:
            atk += self.weapon.atk
            df += self.weapon.df
            hp_bonus += self.weapon.hp
            crit += self.weapon.crit
            dodge += self.weapon.dodge

        # 防具加成
        if self.armor:
            atk += self.armor.atk
            df += self.armor.df
            hp_bonus += self.armor.hp
            crit += self.armor.crit
            dodge += self.armor.dodge

        # 饰品加成
        for acc in self.accessories:
            atk += acc.atk
            df += acc.df
            hp_bonus += acc.hp
            crit += acc.crit
            dodge += acc.dodge

        # 计算总血量上限
        max_hp = self.MaxHP + hp_bonus
        if self.HP > max_hp:
            self.HP = max_hp

        # 确保暴击率与闪避率不超过1
        crit = min(crit, 1.0)
        dodge = min(dodge, 1.0)

        return {"atk": atk, "df": df, "crit": crit, "dodge": dodge, "max_hp": max_hp}

    # ==========================================================
    # 属性上限限制（暴击/闪避最大为1.0）
    # ==========================================================
    def _limit_stats(self):
        """确保暴击与闪避不超过1"""
        if self.crit > 1:
            self.crit = 1.0
        if self.dodge > 1:
            self.dodge = 1.0

    # ==========================================================
    # 存活检测
    # ==========================================================
    def is_alive(self):
        """判断玩家是否存活"""
        return self.HP > 0


# ==========================================================
# 创建玩家函数
# ==========================================================
def create_player(name="Nameless"):
    """创建玩家：支持随机角色与adam测试角色"""
    print("\nCreate your hero:")
    print("1) Random Character")
    print("0) Return to Main Menu")
    choice = input("\nPlease enter the number: ").strip()

    if choice == "0":
        print("\nReturning to main menu...")
        return None
    elif choice != "1":
        print("\nInvalid input. Please enter 1 or 0.")
        return None

    # 随机生成属性
    Profession = "Hero"
    Atk = random.randint(10, 25)
    HP = random.randint(100, 240)
    MP = random.randint(100, 180)
    Def = random.randint(8, 20)
    crit = 0.0
    dodge = 0.0
    skill = []

    # 生成角色实例
    p = Player(name, Profession, Atk, HP, MP, Def, crit, dodge, skill)
    print(f"\nRandom character created: {p.Profession} {p.name}.")
    print(f"ATK={Atk}, HP={HP}, MP={MP}, DEF={Def}")
    return p
