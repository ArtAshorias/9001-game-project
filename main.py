# =============================
# main.py
# 游戏主入口
# =============================

# main.py
from Player import create_player, Player
from battle import Battle
from tool import write_end_log
import time

def show_menu():
    print("\n==== Main Menu ====")
    print("1) New Game ")
    print("2) Quit")
    return input("\nPlease enter your choice: ").strip()

def create_hidden_adam():
    print("\n⚙️ Start Hidden Character：Artorias（Test Type）")
    time.sleep(1)
    return Player(
        name="Artorias", Profession="Debugger",
        Atk=9999, HP=9999, MP=9999, Def=9999,
        crit=1.0, dodge=1.0, skill=[]
    )

def main():
    print("\n=== Welcome to the Dungeon Adventure Game ===")
    print("Tip: Enter ‘Artorias’ to enter hidden test mode.")

    while True:
        c = show_menu()
        if c == "1":
            # 玩家输入角色名
            name_input = input("\nPlease enter your character name (or enter Artorias to unlock the hidden character).：").strip()

            # 判断是否为隐藏角色
            if name_input.lower() == "Artorias":
                player = create_hidden_adam()
            else:
                # 把玩家输入的名字传入创建函数
                player = create_player(name=name_input if name_input else "Nameless")

            if player:
                print(f"\nRole {player.name} Creation successful!")
                print("The adventure is about to begin. Get ready.……")
                time.sleep(1.0)
                battle = Battle(player)
                battle.start_dungeon()
                print("\nGame over. Saving adventure log.……")
                write_end_log(player)
                print("Saving complete. Farewell, brave adventurer!")
                break
        elif c == "2":
            print("\nThanks for playing. See you later.。")
            break
        else:
            print("\nInvalid input. Please re-enter.")

if __name__ == "__main__":
    main()

