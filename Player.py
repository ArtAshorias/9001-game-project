# =============================
# player.py
# 玩家类与角色创建逻辑
# =============================

import random
import time
class Buff:
    """Buff或Debuff（正负皆可），默认持续1回合"""
    def __init__(self, name, atk_delta=0, def_delta=0, crit_delta=0.0, dodge_delta=0.0, rounds=1):
        self.name = name
        self.atk_delta = atk_delta
        self.def_delta = def_delta
        self.crit_delta = crit_delta
        self.dodge_delta = dodge_delta
        self.rounds = rounds

    def tick(self):
        """每回合结束后持续时间减1，返回是否仍有效"""
        self.rounds -= 1
        return self.rounds > 0

class Equipment:
    """装备类"""
    def __init__(self, name, slot, atk=0, df=0, hp=0, crit=0.0, dodge=0.0, on_use_buff=None):
        self.name = name
        self.slot = slot  # weapon / armor / accessory
        self.atk = atk
        self.df = df
        self.hp = hp
        self.crit = crit
        self.dodge = dodge
        self.on_use_buff = on_use_buff

# 角色类定义
class Player:
    def __init__(self, name, Profession, Atk, HP, MP, Def, crit, dodge, skill):
        self.name = name
        self.Profession = Profession
        self.Atk = Atk
        self.HP = HP
        self.MP = MP
        self.Def = Def
        self.crit = crit
        self.dodge = dodge
        self.skill = skill
        self.MaxHP = HP

        # 背包与装备
        self.inventory = []
        self.weapon = None
        self.armor = None
        self.accessories = []

        # 临时 Buff / Debuff
        self.buffs = []

        # 探索步数（第20步Boss战）
        self.steps = 0

# ==============================
# 装备逻辑
# ==============================
    def equip(self, eq):
        """装备物品"""
        if eq.slot == "weapon":
            self.weapon = eq
            return f"Equipped weapon: {eq.name}"
        elif eq.slot == "armor":
            self.armor = eq
            return f"Equipped armor: {eq.name}"
        elif eq.slot == "accessory":
            self.accessories.append(eq)
            return f"Equipped accessory: {eq.name}"
        else:
            return "Unknown equipment type."

    # ==============================
    # 属性计算
    # ==============================
    def effective_stats(self):
        """计算装备和buff后的总属性"""
        atk = self.Atk
        df = self.Def
        hp_bonus = 0
        crit = self.crit
        dodge = self.dodge

        # 武器、防具
        if self.weapon:
            atk += self.weapon.atk
            df += self.weapon.df
            hp_bonus += self.weapon.hp
            crit += self.weapon.crit
            dodge += self.weapon.dodge
        if self.armor:
            atk += self.armor.atk
            df += self.armor.df
            hp_bonus += self.armor.hp
            crit += self.armor.crit
            dodge += self.armor.dodge

        # 饰品
        for acc in self.accessories:
            atk += acc.atk
            df += acc.df
            hp_bonus += acc.hp
            crit += acc.crit
            dodge += acc.dodge

        # Buff / Debuff
        for b in self.buffs:
            atk += b.atk_delta
            df += b.def_delta
            crit += b.crit_delta
            dodge += b.dodge_delta

        max_hp = self.MaxHP + hp_bonus
        if self.HP > max_hp:
            self.HP = max_hp

        return {"atk": atk, "df": df, "crit": crit, "dodge": dodge, "max_hp": max_hp}

    # ==============================
    # Buff逻辑
    # ==============================
    def add_buff(self, buff):
        """添加buff或debuff"""
        self.buffs.append(buff)

    def end_round(self):
        """每个回合结束时减少buff持续时间"""
        self.buffs = [b for b in self.buffs if b.tick()]

    def clear_buffs(self):
        """战斗结束时清空所有buff与debuff"""
        if self.buffs:
            print(f"All buffs and debuffs on {self.name} have worn off.")
        self.buffs.clear()

    def is_alive(self):
        return self.HP > 0

    def show_info(self):
        eff = self.effective_stats()
        print("\n=== Player Info ===")
        print(f"Name: {self.name} | Class: {self.Profession} | Skill: {self.skill}")
        print(f"HP: {self.HP}/{eff['max_hp']}")
        print(f"ATK: {eff['atk']} | DEF: {eff['df']}")
        print(f"Crit: {eff['crit']:.2f} | Dodge: {eff['dodge']:.2f}")
        print(f"Weapon: {self.weapon.name if self.weapon else 'None'}")
        print(f"Armor: {self.armor.name if self.armor else 'None'}")
        if self.accessories:
            print("Accessories:", ", ".join(a.name for a in self.accessories))
        else:
            print("Accessories: None")
        print("====================")
# 预设角色模板
PRESETS = {
    "1": {
        "Profession": "Magician",
        "name": "Merlin",
        "Atk": 10, "HP": 80, "MP": 120, "Def": 6,
        "crit": 0, "dodge": 0, "skill": "Fireball"
    },
    "2": {
        "Profession": "Warrior",
        "name": "Beowulf",
        "Atk": 12, "HP": 100, "MP": 60, "Def": 10,
        "crit": 0.15, "dodge": 0, "skill": "Triple Strike"
    },
    "3": {
        "Profession": "Paladin",
        "name": "Arthur",
        "Atk": 6, "HP": 120, "MP": 100, "Def": 12,
        "crit": 0, "dodge": 0, "skill": "Holy Shield"
    },
    "4": {
        "Profession": "Assassin",
        "name": "Hassan",
        "Atk": 15, "HP": 80, "MP": 80, "Def": 6,
        "crit": 0.15, "dodge": 0.15, "skill": "Backstab"
    }
}

# 创建角色函数
def create_player():
    print("\nPlease select your role:")
    print("1) Magician")
    print("2) Warrior")
    print("3) Paladin")
    print("4) Assassin")
    print("5) Random Character (Random Attributes, Customizable Name)")
    print("0) Return to Main Menu")


    try:
        choice = input("\nPlease enter the number: ").strip()
        #退出
        if choice == "0":
            print("\nReturning to main menu...")
            return None
        # 固定角色
        if choice in {'1', '2', '3', '4'}:
            data = PRESETS[choice]
            p = Player(
                name=data["name"], Profession=data["Profession"],
                Atk=data["Atk"], HP=data["HP"], MP=data["MP"],
                Def=data["Def"], crit=data["crit"], dodge=data["dodge"], skill=data["skill"]
            )
            print(f"\nYou have chosen {p.Profession}, named {p.name}.")
            show_player_info(p)
            return p

        # 随机角色
        elif choice == "5":
            print("\nGenerating random character...")
            name = input("Enter your name (press Enter to use 'Nameless'): ").strip() or "Nameless"
            Profession = "Hero"  # 固定为勇者
            Atk = random.randint(4, 20)
            HP = random.randint(50, 150)
            MP = random.randint(50, 150)
            Def = random.randint(2, 15)
            crit = round(random.uniform(0, 0.2), 2)
            dodge = round(random.uniform(0, 0.2), 2)
            skill = random.choice(["Fireball", "Triple Strike", "Holy Shield", "Backstab"])

            print("\nFinalizing your character...")
            time.sleep(1.2)

            p = Player(name, Profession, Atk, HP, MP, Def, crit, dodge, skill)
            print(f"\nRandom character created: {p.Profession} {p.name}.")
            show_player_info(p)
            return p

        else:
            print("Invalid input. Please enter a number between 1 and 5.")

    except Exception as e:
        print(f"Error occurred: {e}. Please try again.")

    return None


# 显示角色信息
def show_player_info(p: Player):
    print("\n=== Character Info ===")
    print(f"Name: {p.name}")
    print(f"Profession: {p.Profession}")
    print(f"ATK: {p.Atk}")
    print(f"HP: {p.HP}")
    print(f"MP: {p.MP}")
    print(f"DEF: {p.Def}")
    print(f"Crit Rate: {p.crit:.2f}")
    print(f"Dodge Rate: {p.dodge:.2f}")
    print(f"Skill: {p.skill}")
    print("=======================")
