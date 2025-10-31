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
    print("\n⚙️ 启动隐藏角色：Artorias（测试模式）")
    time.sleep(1)
    return Player(
        name="Artorias", Profession="Debugger",
        Atk=9999, HP=9999, MP=9999, Def=9999,
        crit=1.0, dodge=1.0, skill=[]
    )

def main():
    print("\n=== 欢迎进入地下城冒险游戏 ===")
    print("提示：输入 'adam' 可进入隐藏测试模式。")

    while True:
        c = show_menu()
        if c == "1":
            # 玩家输入角色名
            name_input = input("\n请输入角色名（或输入 Artorias 激活隐藏角色）：").strip()

            # 判断是否为隐藏角色
            if name_input.lower() == "adam":
                player = create_hidden_adam()
            else:
                # 把玩家输入的名字传入创建函数
                player = create_player(name=name_input if name_input else "Nameless")

            if player:
                print(f"\n角色 {player.name} 创建成功！")
                print("冒险即将开始，请做好准备……")
                time.sleep(1.0)
                battle = Battle(player)
                battle.start_dungeon()
                print("\n游戏结束，正在保存冒险记录……")
                write_end_log(player)
                print("存档完成，再见，勇者！")
                break
        elif c == "2":
            print("\n感谢游玩，再见。")
            break
        else:
            print("\n输入无效，请重新输入。")

if __name__ == "__main__":
    main()

