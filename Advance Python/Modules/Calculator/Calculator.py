import tkinter as tk

def Cal():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        if operation == "Add":
            result = num1 + num2
        elif operation == "Sub":
            result = num1 - num2
        elif operation == "Multiply":
            result = num1 * num2
        elif operation == "Div":
            if num2 == 0:
                result_var.set("Error: Divide by 0")
                return
            result = num1 / num2
        else:
            result_var.set("Select an Operation")
            return
        
        result_var.set(f"Result: {result}")
    except ValueError:
        result_var.set("Invalid Input!!")

def reset():
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)
    operation_var.set("")
    result_var.set("Result: ")

window=tk.Tk()
window.title("Simple Calculator")
window.geometry("450x550")

tk.Label(window,text="Enter Number 1: ").pack(pady=5)
entry_num1=tk.Entry(window)
entry_num1.pack(pady=5)

tk.Label(window,text="Enter Number 2: ").pack(pady=5)
entry_num2=tk.Entry(window)
entry_num2.pack(pady=5)

tk.Label(window,text="Select Operation: ").pack(pady=5)
operation_var=tk.StringVar(window)
tk.OptionMenu(window,operation_var,"Add","Sub","Multiply","Div").pack()

result_var=tk.StringVar(value="Result: ")
tk.Label(window,textvariable=result_var).pack(pady=10)

tk.Button(window,text="Calculate",font='Calibri',command=Cal).pack(pady=10)

reset_button=tk.Button(window,text="Reset",font='Calibri',command=reset).pack(pady=10)

window.mainloop()