# =============================
# enemy.py
# 敌人类与战斗事件生成逻辑
# =============================

# enemy.py
import random


class Enemy:
    def __init__(self, name, atk, hp, df, crit=0.0, dodge=0.0, exp=10, is_boss=False):
        self.name = name
        self.Atk = atk
        self.HP = hp
        self.MaxHP = hp
        self.Def = df
        self.crit = crit
        self.dodge = dodge
        self.exp = exp
        self.is_boss = is_boss
        self.buffs = []

    def is_alive(self):
        return self.HP > 0

    def end_round(self):
        if not self.buffs: return
        remaining = []
        for buff in self.buffs:
            # 简化：这里只更新持续回合，忽略DoT以保证流程稳定
            if buff.tick():
                remaining.append(buff)
        self.buffs = remaining

    def show_info(self):
        print(f"\n=== Enemy Info ===")
        print(f"Name: {self.name}")
        print(f"HP: {self.HP}/{self.MaxHP} | ATK: {self.Atk} | DEF: {self.Def}")
        print(f"Crit: {self.crit:.2f} | Dodge: {self.dodge:.2f}")
        print("===================")

ENEMY_TEMPLATES = {
    "Slime": {"atk": (4, 8), "hp": (50, 80), "df": (2, 5), "crit": 0.0, "dodge": 0.0, "exp": 10},
    "Goblin": {"atk": (8, 12), "hp": (80, 120), "df": (4, 8), "crit": 0.05, "dodge": 0.05, "exp": 15},
    "Dragon": {"atk": (20, 35), "hp": (350, 400), "df": (12, 16), "crit": 0.1, "dodge": 0.05, "exp": 100, "is_boss": True},
    "Demon King": {"atk": (45, 50), "hp": (800, 800), "df": (20, 22), "crit": 0.15, "dodge": 0.1, "exp": 999, "is_boss": True},
}

def create_enemy(name):
    data = ENEMY_TEMPLATES[name]
    enemy = Enemy(
        name=name,
        atk=random.randint(*data["atk"]),
        hp=random.randint(*data["hp"]),
        df=random.randint(*data["df"]),
        crit=data["crit"], dodge=data["dodge"], exp=data["exp"],
        is_boss=data.get("is_boss", False)
    )
    enemy.show_info()
    return enemy

def generate_event(step, player):
    if step in (14, 19):
        print("\n=== You have arrived at the rest room. ===")
        player.HP = player.MaxHP
        print(f"{player.name} HP has been fully restored {player.HP}/{player.MaxHP}。")
        return None
    elif step == 15:
        print("\n=== Boss Battle: Dragon ===")
        return create_enemy("Dragon")
    elif step == 20:
        print("\n=== Final Battle: Demon King ===")
        return create_enemy("Demon King")
    else:
        name = random.choice(["Slime", "Goblin"])
        e = create_enemy(name)
        return e

