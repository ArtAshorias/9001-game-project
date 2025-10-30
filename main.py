# =============================
# main.py
# 游戏主循环
# =============================

from Player import create_player
from tool import write_end_log

def show_menu():
    print("\n==== Main Menu ====")
    print("1) New Game")
    print("2) Quit")
    return input("\nPlease enter your choice: ").strip()

def main():
    player = None
    while True:
        c = show_menu()

        if c == "1":
            player = create_player()
            if player:
                print("\nCharacter created successfully! Dungeon feature coming soon...")
                input("\nPress Enter to simulate the end of the game...")

        elif c == "2":
            print("\nGame exited.")
            if player:
                write_end_log(player)
                print("See you next time!")
            break

        else:
            print("\nInvalid input. Please try again.")

if __name__ == "__main__":
    main()
