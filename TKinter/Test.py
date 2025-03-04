import requests
import tkinter as tk

def get_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    res=requests.get(url)
    if res.status_code == 200:
        return res.json()
    return {}

data1=get_data()
key=data1.keys()
print(data1)
print(key)

def display_Key():
    data=get_data()
    keys=data.keys()
    if label:
        label.config(text="Keys:\n"+"\n".join(keys))

window=tk.Tk()
window.title("JSON Key Extractor")
window.geometry("250x250")
label=tk.Label(window,text="Clickthe button to fetch key")
label.pack(pady=10)
btn=tk.Button(window,text="Get Key",command=display_Key)
btn.pack(pady=10)
window.mainloop()