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
        self.steps = 0

    def start_dungeon(self):
        print("\n=== The dungeon adventure begins! ===")
        print("You will explore 20 floors, encountering battles, treasure chests, or rest rooms along the way.")

        while self.player.steps < self.max_steps:
            input("\nPress Enter to continue...")
            self.player.steps += 1
            step = self.player.steps
            print(f"\n—— Current Floor: {step} ——")

            event_type = self.trigger_event(step)

            if event_type == "rest":
                self.rest_room(); continue

            # 巨龙战
            if event_type == "dragon":
                enemy = generate_event(15, self.player)
                print("\n The dragon has appeared!")
                self.battle(enemy, event_type="dragon")
                if not self.player.is_alive(): break
                if not enemy.is_alive(): apply_dragon_reward(self.player)
                continue

            # 魔王战
            if event_type == "boss":
                enemy = generate_event(20, self.player)
                print("\n The Demon King has appeared! The ultimate battle begins!")
                self.battle(enemy, event_type="final_boss")
                if not self.player.is_alive():
                    print("\nYou have fallen... The adventure is over.")
                else:
                    print("\n=== You have defeated the Demon King! Peace has returned to the world! ===")
                break

            if event_type == "chest":
                self.treasure_room(); continue

            # 普通敌人
            enemy = generate_event(step, self.player)
            print(f"\nAn enemy has appeared!：{enemy.name}！")
            self.battle(enemy)
            if not self.player.is_alive(): break

        print("\n=== The dungeon adventure has ended. ===")

    def trigger_event(self, step):
        if step in (14, 19): return "rest"
        if step == 15: return "dragon"
        if step == 20: return "boss"
        return "chest" if random.random() < 0.15 else "battle"

    def battle(self, enemy, event_type="battle"):
        print("\n=== The battle begins! ===")
        print(f"{self.player.name} HP: {self.player.HP}/{self.player.MaxHP}")
        print(f"{enemy.name} HP: {enemy.HP}/{enemy.MaxHP}")

        round_count = 1
        while self.player.is_alive() and enemy.is_alive():
            print(f"\n—— Round {round_count}  ——")
            print(f"{self.player.name} HP: {self.player.HP}/{self.player.MaxHP} | {enemy.name} HP: {enemy.HP}/{enemy.MaxHP}")
            print("\nChoice:\n1) Attack\n2) Skill")
            choice = input("Please enter a number to choose your action: ").strip()

            if choice == "1":
                self.normal_attack(enemy)
            elif choice == "2":
                self.use_skill(enemy)
            else:
                print("Invalid input, please choose again.")
                continue

            if not enemy.is_alive():
                print(f"\n{enemy.name} Defeated!")
                if event_type not in ["dragon", "final_boss"]:
                    self.obtain_loot()
                break

            if enemy.is_alive():
                self.enemy_attack(enemy)

            print(f"\nTurn ended.：{self.player.name} HP {self.player.HP}/{self.player.MaxHP} | {enemy.name} HP {enemy.HP}/{enemy.MaxHP}")
            round_count += 1

    def normal_attack(self, enemy):
        damage = max(0, self.player.Atk - enemy.Def)
        enemy.HP -= damage
        if enemy.HP < 0: enemy.HP = 0
        print(f"{self.player.name} Attack {enemy.name}，Dealt {damage} of damage!")
        print(f"{enemy.name} Current remaining HP: {enemy.HP}/{enemy.MaxHP}")

    def use_skill(self, enemy):
        if not self.player.skill:
            print("You have not learned any skills yet！"); return
        print("\n=== Skill List ===")
        for i, sk in enumerate(self.player.skill, 1):
            print(f"{i}. {sk.name} - {sk.desc} (MP Cost: {sk.mp_cost})")
        try:
            idx = int(input("Please select a skill number: "))
            if 1 <= idx <= len(self.player.skill):
                skill = self.player.skill[idx - 1]
                if self.player.MP < skill.mp_cost:
                    print("No MP！"); return
                self.player.MP -= skill.mp_cost
                skill.use(self.player, enemy)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Please enter a valid number.。")

    def enemy_attack(self, enemy):
        damage = max(0, enemy.Atk - self.player.Def)
        self.player.HP -= damage
        if self.player.HP < 0: self.player.HP = 0
        print(f"{enemy.name} Attack {self.player.name}，Dealt {damage} of damage!")
        print(f"{self.player.name} Current remaining HP: {self.player.HP}/{self.player.MaxHP}")

    def treasure_room(self):
        print("\n=== Treasure Chest Room ===")
        loot_items = generate_loot(event_type="chest")
        for i, item in enumerate(loot_items, 1):
            print(f"{i}. {item['name']} - {item['desc']}")
        try:
            choice = int(input("\nPlease select the item number to use or equip (or enter 0 to skip): "))
            if choice != 0 and 1 <= choice <= len(loot_items):
                loot_items[choice - 1]["effect"](self.player)
        except ValueError:
            print("Invalid input. Skipping this selection.。")

    def rest_room(self):
        print("\n=== Rest Room ===")
        old_hp = self.player.HP
        old_mp = self.player.MP

        self.player.HP = self.player.MaxHP
        self.player.MP = self.player.MaxMP

        print(f"{self.player.name} HP has been fully restored（{old_hp} → {self.player.HP}）！")
        print(f"{self.player.name} HP has been fully restored（{old_mp} → {self.player.MP}）！")

    def obtain_loot(self):
        loot_items = generate_loot(event_type="battle")
        print("\n=== Battle Rewards ===")
        for i, item in enumerate(loot_items, 1):
            print(f"{i}. {item['name']} - {item['desc']}")
        try:
            choice = int(input("\nPlease select the item number to use or equip (or enter 0 to skip): "))
            if choice != 0 and 1 <= choice <= len(loot_items):
                loot_items[choice - 1]["effect"](self.player)
        except ValueError:
            print("Invalid input. Skipping rewards.")
