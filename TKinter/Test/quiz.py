import tkinter as tk
from tkinter import messagebox

def start_quiz(questions):
    def next_question():
        nonlocal current_question,score
        if var.get() == questions[current_question][2]:
            score += 1
        current_question += 1
        if current_question < len(questions):
            load_question()
        else:
            messagebox.showinfo("Quiz Finished", f"Your final score is {score} out of {len(questions)}")
            window.destroy()
    
    def load_question():
        question_label.config(text=questions[current_question][0])
        for i, option in enumerate(questions[current_question][1]):
            radio_buttons[i].config(text=option,value=option)
        var.set("")
    
    window=tk.Tk()
    window.title("Quiz")
    window.geometry("350x400")

    current_question = 0
    score = 0
    var = tk.StringVar(value="")

    question_label=tk.Label(window,text="",font=("Arial",14),wraplength=300)
    question_label.pack(pady=20)

    radio_buttons = [tk.Radiobutton(window,text="",variable=var,font=("Arial",12),value="") for _ in range(4)]
    for rb in radio_buttons:
        rb.pack(anchor="w")
    
    next_button=tk.Button(window,text="Next",command=next_question).pack(pady=10)

    load_question()
    window.mainloop()