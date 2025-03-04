import tkinter as tk
import random

window = tk.Tk()
window.title("Random Number Generator")
window.geometry("300x200")

label = tk.Label(window, bg="lightblue", text="Click the button", font=("Helvetica", 20), width=20, height=2)
label.pack(pady=20)

def r():
    random1 = random.randint(1, 100)
    label.config(text=f"Random: {random1}", fg="darkgreen")

button = tk.Button(window, text="Generate Random Number", bg="green", fg="white", font=("Arial", 14), command=r)
button.pack(pady=10)

def reset():
    label.config(text="Click the button", fg="black")

reset_button = tk.Button(window, text="Reset", bg="red", fg="white", font=("Arial", 12), command=reset)
reset_button.pack(pady=5)

window.mainloop()
