import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

API_URL = "https://jsonplaceholder.typicode.com/posts"

def send_request(method):
    post_id = entry_id.get().strip()
    url = API_URL if not post_id else f"{API_URL}/{post_id}"

    try:
        data_obj = {
            "title": entry_title.get().strip(),
            "body": entry_body.get().strip(),
            "userId": 1
        }

        json_data = json.dumps(data_obj)

        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(API_URL, data=json_data, headers={"Content-Type": "application/json"})
        elif method == "PUT":
            response = requests.put(url, data=json_data, headers={"Content-Type": "application/json"})
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            messagebox.showerror("Error", "Invalid Method")
            return

        if response.status_code in [200, 201]:
            messagebox.showinfo("Success", json.dumps(response.json(), indent=4))
        else:
            messagebox.showerror("Error", f"Status Code: {response.status_code}\n{response.text}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

window = tk.Tk()
window.title("Rest API")
window.geometry("450x400")

ttk.Label(window, text="Post ID:").pack(pady=5)
entry_id = ttk.Entry(window)
entry_id.pack(pady=5)

ttk.Label(window, text="Title:").pack(pady=5)
entry_title = ttk.Entry(window)
entry_title.pack(pady=5)

ttk.Label(window, text="Body:").pack(pady=5)
entry_body = ttk.Entry(window)
entry_body.pack(pady=5)

ttk.Button(window, text="GET", command=lambda: send_request("GET")).pack(pady=5)
ttk.Button(window, text="POST", command=lambda: send_request("POST")).pack(pady=5)
ttk.Button(window, text="PUT", command=lambda: send_request("PUT")).pack(pady=5)
ttk.Button(window, text="DELETE", command=lambda: send_request("DELETE")).pack(pady=5)

window.mainloop()