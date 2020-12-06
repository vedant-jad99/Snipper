import tkinter as tk
from main_app.app import Snipper

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Snipping Tool")
    Snipper(root)
    root.mainloop()
