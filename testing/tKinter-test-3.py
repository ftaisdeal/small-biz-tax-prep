import tkinter as tk
from tkinter import messagebox

def greet():
    name = entry.get()
    if name:
        messagebox.showinfo("Greeting", f"Hello, {name}!")
    else:
        messagebox.showwarning("Input Error", "Please enter your name.")

root = tk.Tk()
root.title("Personal Greeter")

tk.Label(root, text="Enter your name:").pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)
tk.Button(root, text="Greet!", command=greet).pack(pady=10)

root.mainloop()