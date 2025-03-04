import tkinter as tk

def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + value)

def calculate():
    try:
        current = entry.get()
        result = str(eval(current))  
        entry.delete(0, tk.END)
        entry.insert(0, result)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def clear():
    entry.delete(0, tk.END)

window = tk.Tk()
window.title("Calculator")
window.geometry("400x600")

entry = tk.Entry(window, font=("Arial", 24), borderwidth=2, relief="solid", justify="right")
entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ("C", 5, 0)
]

for (text, row, col) in buttons:
    if text == "=":
        tk.Button(window, text=text, font=("Arial", 18), height=2, width=5, command=calculate).grid(row=row, column=col, pady=5, padx=5)
    elif text == "C":
        tk.Button(window, text=text, font=("Arial", 18), height=2, width=5, command=clear).grid(row=row, column=col, pady=5, padx=5)
    else:
        tk.Button(window, text=text, font=("Arial", 18), height=2, width=5, command=lambda value=text: button_click(value)).grid(row=row, column=col, pady=5, padx=5)

window.mainloop()
