import tkinter as tk

def greet():
    name = entry.get()
    label.config(text=f"Hello, {name}!")

root = tk.Tk()
root.title("Name Greeting")

entry = tk.Entry(root)
entry.pack(pady=5)

button = tk.Button(root, text="Greet Me", command=greet)
button.pack(pady=5)

label = tk.Label(root, text="")
label.pack(pady=5)

root.mainloop()