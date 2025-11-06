import tkinter as tk
from PIL import Image, ImageTk   # 注意：需要 pillow 支持： pip install pillow
import threading, queue, sys, traceback
from pathlib import Path
import main  # 你的游戏逻辑

# 输出重定向
class CanvasRedirector:
    def __init__(self, canvas):
        self.canvas = canvas
        self.text_lines = []
        self.font = ("Consolas", 14, "bold")
        self.color = "white"
        self.scroll_offset = 0   # 当前滚动偏移量
        self.line_height = 22
        self.visible_lines = 28  # 一屏显示行数

        # 绑定鼠标滚轮事件
        self.canvas.bind_all("<MouseWheel>", self.on_scroll)
        self.canvas.bind_all("<Button-4>", self.on_scroll)  # Linux支持
        self.canvas.bind_all("<Button-5>", self.on_scroll)

    def write(self, text):
        for line in text.split("\n"):
            self.text_lines.append(line)
        self.refresh_canvas(auto_scroll=True)

    def refresh_canvas(self, auto_scroll=False):
        self.canvas.delete("text")
        total_lines = len(self.text_lines)
        start = max(0, total_lines - self.visible_lines - self.scroll_offset)
        end = start + self.visible_lines
        visible = self.text_lines[start:end]

        y = 60
        for line in visible:
            self.canvas.create_text(
                50, y, text=line, anchor="w", fill=self.color,
                font=self.font, tags="text"
            )
            y += self.line_height
        self.canvas.update()

    def on_scroll(self, event):
        # event.delta 在 Windows 为 ±120，Linux 为 ±1
        direction = 1 if event.delta > 0 else -1
        self.scroll_offset += direction
        self.scroll_offset = max(0, min(self.scroll_offset, max(0, len(self.text_lines) - self.visible_lines)))
        self.refresh_canvas()

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
