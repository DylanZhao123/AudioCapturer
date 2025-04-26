import tkinter as tk

class SubtitleWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.75)
        self.root.configure(bg="black")
        self.root.geometry("1000x80+100+720")

        self.history = ["", ""]

        self.label = tk.Label(
            self.root,
            text="\n".join(self.history),
            font=("Helvetica", 13),
            fg="white",
            bg="black",
            wraplength=950,
            justify="left"
        )
        self.label.pack()

    def update_text(self, text):
        self.history.append(text)
        if len(self.history) > 2:
            self.history.pop(0)
        self.label.config(text="\n".join(self.history))

    def run(self):
        self.root.mainloop()
