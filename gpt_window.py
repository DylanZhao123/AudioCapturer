import tkinter as tk

class GPTWindow:
    def __init__(self):
        self.root = tk.Toplevel()
        self.root.title("GPT Response")
        self.root.overrideredirect(True)              # 无边框
        self.root.attributes("-topmost", True)         # 始终置顶
        self.root.attributes("-alpha", 0.8)            # 半透明
        self.root.configure(bg="black")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = 400
        height = 500
        x = screen_width - width - 20     # 屏幕右侧留 20 px 边距
        y = 100                            # 屏幕顶部下移一点

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        self.text = tk.Text(
            self.root,
            font=("Helvetica", 14),
            bg="black",
            fg="white",
            wrap="word",
            insertbackground="white",
            relief="flat"
        )
        self.text.pack(expand=True, fill="both")
        self.text.configure(state="disabled")

    def update_text(self, content):
        self.text.configure(state="normal")
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)
        self.text.configure(state="disabled")
        self.root.lift()
