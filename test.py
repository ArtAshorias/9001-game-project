import tkinter as tk
from PIL import Image, ImageTk   # 注意：需要 pillow 支持： pip install pillow
import threading, queue, sys, traceback
from pathlib import Path
import main  # 你的游戏逻辑

# 输出重定向
class CanvasRedirector:
    def __init__(self, canvas):
        self.canvas = canvas
        self.text_lines = []  # 保存所有文字行
        self.max_lines = 28   # 最大显示行数（控制不超出窗口）
        self.font = ("Consolas", 14, "bold")
        self.color = "white"

    def write(self, text):
        for line in text.split("\n"):
            if line.strip():
                self.text_lines.append(line)
            else:
                self.text_lines.append("")
            # 超过窗口最大行时删除顶部
            if len(self.text_lines) > self.max_lines:
                self.text_lines.pop(0)
        self.refresh_canvas()

    def refresh_canvas(self):
        self.canvas.delete("text")
        y = 60
        for line in self.text_lines:
            self.canvas.create_text(
                50, y, text=line, anchor="w", fill=self.color,
                font=self.font, tags="text"
            )
            y += 22
        self.canvas.update()

    def flush(self):
        pass

# 模拟输入流
class StdinRedirector:
    def __init__(self):
        self.q = queue.Queue()
    def readline(self):
        return self.q.get() + "\n"

class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Adventure - Pixel Console")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)

        base = Path(__file__).resolve().parent

        # ==== 背景加载并自适应缩放 ====
        try:
            from PIL import Image, ImageTk
            img_path = base / "2.png"
            img = Image.open(img_path)
            img = img.resize((1280, 720), Image.LANCZOS)  # 缩放到窗口大小
            self.bg_img = ImageTk.PhotoImage(img)
            self.canvas = tk.Canvas(root, width=1280, height=720, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        except Exception as e:
            print(f"[WARNING] 背景加载失败: {e}")
            self.canvas = tk.Canvas(root, bg="#1e252b", width=1280, height=720)
            self.canvas.pack(fill="both", expand=True)

        # 输入文本模拟
        self.input_text = ""
        self.input_display = self.canvas.create_text(
            50, 680, text="> ", anchor="w", fill="yellow",
            font=("Consolas", 14, "bold")
        )

        # 绑定键盘输入
        self.root.bind("<Key>", self.on_key_press)

        # 输入输出重定向
        self.stdin_redirector = StdinRedirector()
        sys.stdin = self.stdin_redirector
        sys.stdout = CanvasRedirector(self.canvas)

        # 启动游戏线程
        self.root.after_idle(self.start_game_thread)

    def start_game_thread(self):
        def runner():
            try:
                main.main()
            except Exception:
                err = traceback.format_exc()
                print("\n[ERROR] 游戏运行出错：\n" + err)
        threading.Thread(target=runner, daemon=True).start()

    def on_key_press(self, event):
        if event.keysym == "Return":
            text = self.input_text.strip()
            self.stdin_redirector.q.put(text)
            self.input_text = ""
            self.canvas.itemconfig(self.input_display, text="> ")
        elif event.keysym == "BackSpace":
            self.input_text = self.input_text[:-1]
            self.canvas.itemconfig(self.input_display, text="> " + self.input_text)
        elif len(event.char) == 1:
            self.input_text += event.char
            self.canvas.itemconfig(self.input_display, text="> " + self.input_text)

if __name__ == "__main__":
    root = tk.Tk()
    GameWindow(root)
    root.mainloop()
