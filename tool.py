# =============================
# utils.py
# 日志记录与存档工具
# =============================

import os
from datetime import datetime

CREATE_LOG_DIR = "."  # 当前目录

def write_end_log(player):
    """Write player end-game info to txt log"""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(CREATE_LOG_DIR, f"player_end-{ts}.txt")

    lines = [
        f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "—— Game Result ——",
        f"Name: {player.name}",
        f"Profession: {player.Profession}",
        f"ATK: {player.Atk}",
        f"HP: {player.HP}",
        f"MP: {player.MP}",
        f"DEF: {player.Def}",
        f"Crit: {player.crit:.2f}",
        f"Dodge: {player.dodge:.2f}",
        f"Skill: {player.skill}",
        "",
        "Result: The hero completed the journey and left a legend behind.",
    ]

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nGame end record saved: {os.path.basename(filename)}")
