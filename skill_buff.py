# =============================
# skill_buff.py
# 技能与 Buff 系统（完整版）
# =============================

import random

# -----------------------------
# Skill 类
# -----------------------------
# skill_buff.py
# 技能系统（无 Buff 版本）

class Skill:
    """技能类：分为攻击型与治疗型"""
    def __init__(self, name, desc, mp_cost, mode="damage", scale="flat", value=10, hits=1):
        self.name = name
        self.desc = desc
        self.mp_cost = mp_cost
        self.mode = mode
        self.scale = scale
        self.value = value
        self.hits = hits

    def _pick_value(self):
        """如果 value 是列表则随机抽取一个"""
        if isinstance(self.value, list):
            return random.choice(self.value)
        return self.value

    def use(self, player, enemy):
        print(f"\n{player.name} 使用技能 [{self.name}]！")

        total_damage = 0
        for i in range(self.hits):
            val = self._pick_value()
            base = int(val if self.scale == "flat" else val * player.Atk)
            damage = max(0, base + player.Atk - enemy.Def)
            enemy.HP -= damage
            total_damage += damage
            if enemy.HP < 0:
                enemy.HP = 0
            if self.hits > 1:
                print(f"{self.name} 第{i + 1}击造成 {damage} 点伤害！")
            if enemy.HP <= 0:
                break

        if self.hits == 1:
            print(f"{self.name} 对 {enemy.name} 造成了 {total_damage} 点伤害！")
        else:
            print(f"{self.name} 总计造成 {total_damage} 点伤害！")
        print(f"{enemy.name} 剩余 HP: {enemy.HP}/{enemy.MaxHP}")


# ==================================================
# 技能注册
# ==================================================
SKILL_BOOKS = [
    # 造成 1.5 倍攻击伤害（单段）
    {"name": "Fireball", "desc": "造成1.5倍攻击力的伤害",
     "mp_cost": 5, "mode": "damage", "scale": "mult", "value": 1.5, "hits": 1},

    # 三连击：每次 0.6 倍攻击
    {"name": "Triple Strike", "desc": "连续攻击三次，每次造成0.6倍攻击伤害",
     "mp_cost": 5, "mode": "damage", "scale": "mult", "value": 0.6, "hits": 3},

    # 爆燃：3 倍攻击（单段）
    {"name": "Flame Burst", "desc": "造成3倍攻击伤害",
     "mp_cost": 10, "mode": "damage", "scale": "mult", "value": 3.0, "hits": 1},

    # 陨石：5 倍攻击（单段）
    {"name": "Meteor", "desc": "造成5倍攻击伤害",
     "mp_cost": 10, "mode": "damage", "scale": "mult", "value": 5.0, "hits": 1},

    # 处决：随机 3 倍或 5 倍（单段）
    {"name": "Fatal Strike", "desc": "随机造成3或5倍伤害",
     "mp_cost": 10, "mode": "damage", "scale": "mult", "value": [3.0, 5.0], "hits": 1},

    # 流剑：4 倍攻击（单段）
    {"name": "Flow Sword", "desc": "造成4倍伤害",
     "mp_cost": 10, "mode": "damage", "scale": "mult", "value": 0.6, "hits": 10},

]

def create_skill_from_book(book: dict) -> Skill:
    """把技能书原型转为真正可用的 Skill 实例"""
    return Skill(
        name=book["name"],
        desc=book["desc"],
        mp_cost=book["mp_cost"],
        mode=book.get("mode", "damage"),
        scale=book.get("scale", "flat"),
        value=book.get("value", 10),
        hits=book.get("hits", 1),
    )
