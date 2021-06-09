import tkinter as tk

class Example(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("200x200+100+100")
        self.btn = tk.Button(self, text="Test button", command=self.update_window)
        self.btn.place(x=50, y=50)

    def update_window(self):
        self.geometry("400x400+200+200")
        self.entry = tk.Entry(self, width=15)
        self.entry.place(x=30,y=30)
        self.btn.config(text="Send", command=self.actions)
        self.btn.place(x=80, y=80)

    def actions(self):
        tk.Label(self, text=self.entry.get()).place(x=20,y=20)
        self.btn.destroy()
        self.entry.destroy()

if __name__ == "__main__":
    Example().mainloop()