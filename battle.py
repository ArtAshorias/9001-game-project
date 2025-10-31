# =============================
# battle.py
# 战斗与事件控制系统
# =============================

# battle.py
import random
from enemy import Enemy, generate_event
from item import generate_loot, apply_dragon_reward

class Battle:
    def __init__(self, player):
        self.player = player
        self.max_steps = 20

    def start_dungeon(self):
        print("\n=== 地下城冒险开始 ===")
        print("你将探索20层，途中可能遇到战斗、宝箱或休息室。")

        while self.player.steps < self.max_steps:
            input("\n按下 Enter 继续前进...")
            self.player.steps += 1
            step = self.player.steps
            print(f"\n—— 当前层数：第 {step} 层 ——")

            event_type = self.trigger_event(step)

            if event_type == "rest":
                self.rest_room(); continue

            # 巨龙战
            if event_type == "dragon":
                enemy = generate_event(15, self.player)
                print("\n🔥 巨龙出现了！🔥")
                self.battle(enemy, event_type="dragon")
                if not self.player.is_alive(): break
                if not enemy.is_alive(): apply_dragon_reward(self.player)
                continue

            # 魔王战
            if event_type == "boss":
                enemy = generate_event(20, self.player)
                print("\n👑 魔王出现！终极之战开始！👑")
                self.battle(enemy, event_type="final_boss")
                if not self.player.is_alive():
                    print("\n你倒下了……冒险结束。")
                else:
                    print("\n=== 你击败了魔王！世界恢复了和平！ ===")
                break

            if event_type == "chest":
                self.treasure_room(); continue

            # 普通敌人
            enemy = generate_event(step, self.player)
            print(f"\n遭遇敌人：{enemy.name}！")
            self.battle(enemy)
            if not self.player.is_alive(): break

        print("\n=== 地下城冒险结束 ===")

    def trigger_event(self, step):
        if step in (14, 19): return "rest"
        if step == 15: return "dragon"
        if step == 20: return "boss"
        return "chest" if random.random() < 0.15 else "battle"

    def battle(self, enemy, event_type="battle"):
        print("\n=== 战斗开始 ===")
        print(f"{self.player.name} 初始 HP: {self.player.HP}/{self.player.MaxHP}")
        print(f"{enemy.name} 初始 HP: {enemy.HP}/{enemy.MaxHP}")

        round_count = 1
        while self.player.is_alive() and enemy.is_alive():
            print(f"\n—— 第 {round_count} 回合 ——")
            print(f"{self.player.name} HP: {self.player.HP}/{self.player.MaxHP} | {enemy.name} HP: {enemy.HP}/{enemy.MaxHP}")
            print("\n请选择行动:\n1) 普通攻击\n2) 使用技能")
            choice = input("请输入数字选择行动: ").strip()

            if choice == "1":
                self.normal_attack(enemy)
            elif choice == "2":
                self.use_skill(enemy)
            else:
                print("输入无效，请重新选择。")
                continue

            if not enemy.is_alive():
                print(f"\n{enemy.name} 被击败！")
                if event_type not in ["dragon", "final_boss"]:
                    self.obtain_loot()
                break

            if enemy.is_alive():
                self.enemy_attack(enemy)

            print(f"\n回合结束：{self.player.name} HP {self.player.HP}/{self.player.MaxHP} | {enemy.name} HP {enemy.HP}/{enemy.MaxHP}")
            round_count += 1

    def normal_attack(self, enemy):
        damage = max(0, self.player.Atk - enemy.Def)
        enemy.HP -= damage
        if enemy.HP < 0: enemy.HP = 0
        print(f"{self.player.name} 攻击了 {enemy.name}，造成 {damage} 点伤害！")
        print(f"{enemy.name} 当前剩余 HP: {enemy.HP}/{enemy.MaxHP}")

    def use_skill(self, enemy):
        if not self.player.skill:
            print("你尚未掌握任何技能！"); return
        print("\n=== 技能列表 ===")
        for i, sk in enumerate(self.player.skill, 1):
            print(f"{i}. {sk.name} - {sk.desc} (MP消耗: {sk.mp_cost})")
        try:
            idx = int(input("请选择技能编号: "))
            if 1 <= idx <= len(self.player.skill):
                skill = self.player.skill[idx - 1]
                if self.player.MP < skill.mp_cost:
                    print("MP不足！"); return
                self.player.MP -= skill.mp_cost
                skill.use(self.player, enemy)
            else:
                print("无效选择。")
        except ValueError:
            print("请输入有效数字。")

    def enemy_attack(self, enemy):
        damage = max(0, enemy.Atk - self.player.Def)
        self.player.HP -= damage
        if self.player.HP < 0: self.player.HP = 0
        print(f"{enemy.name} 攻击了 {self.player.name}，造成 {damage} 点伤害！")
        print(f"{self.player.name} 当前剩余 HP: {self.player.HP}/{self.player.MaxHP}")

    def treasure_room(self):
        print("\n=== 宝箱房 ===")
        loot_items = generate_loot(event_type="chest")
        for i, item in enumerate(loot_items, 1):
            print(f"{i}. {item['name']} - {item['desc']}")
        try:
            choice = int(input("\n请选择要使用或装备的物品编号（或输入0跳过）："))
            if choice != 0 and 1 <= choice <= len(loot_items):
                loot_items[choice - 1]["effect"](self.player)
        except ValueError:
            print("输入无效，跳过本次选择。")

    def rest_room(self):
        print("\n=== 休息房 ===")
        old_hp = self.player.HP
        old_mp = self.player.MP

        self.player.HP = self.player.MaxHP
        self.player.MP = self.player.MaxMP

        print(f"{self.player.name} 的生命值已完全恢复（{old_hp} → {self.player.HP}）！")
        print(f"{self.player.name} 的生命值已完全恢复（{old_mp} → {self.player.MP}）！")

    def obtain_loot(self):
        loot_items = generate_loot(event_type="battle")
        print("\n=== 战斗奖励 ===")
        for i, item in enumerate(loot_items, 1):
            print(f"{i}. {item['name']} - {item['desc']}")
        try:
            choice = int(input("\n请选择要使用或装备的物品编号（或输入0跳过）："))
            if choice != 0 and 1 <= choice <= len(loot_items):
                loot_items[choice - 1]["effect"](self.player)
        except ValueError:
            print("输入无效，跳过奖励。")
