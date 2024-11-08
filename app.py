import requests
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import json

# GitHub URLs
LIST_JSON_URL = "https://raw.githubusercontent.com/username/repository/main/list.json"
INI_BASE_URL = "https://raw.githubusercontent.com/username/repository/main/ini/"

def fetch_version_list():
    try:
        response = requests.get(LIST_JSON_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch version list: {e}")
        return {}

def download_ini_file(filename, save_path):
    try:
        response = requests.get(INI_BASE_URL + filename)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
        return True
    except Exception as e:
        messagebox.showerror("Download Error", f"Failed to download ini file: {e}")
        return False

def stop_remote_service():
    subprocess.run(["sc", "stop", "TermService"], shell=True)

def start_remote_service():
    subprocess.run(["sc", "start", "TermService"], shell=True)

def update_ini(selected_os, selected_version, ini_path):
    stop_remote_service()
    if download_ini_file(selected_version, ini_path):
        messagebox.showinfo("Success", "INI file updated successfully.")
    start_remote_service()

def create_gui():
    data = fetch_version_list()
    if not data:
        return

    root = tk.Tk()
    root.title("RDP Wrapper INI Updater")

    ttk.Label(root, text="Select Operating System:").pack(pady=5)
    os_selection = ttk.Combobox(root, values=list(data.keys()), state="readonly")
    os_selection.pack()

    version_label = ttk.Label(root, text="Select Version:")
    version_label.pack(pady=5)
    version_selection = ttk.Combobox(root, state="readonly")
    version_selection.pack()

    def update_version_list(event):
        selected_os = os_selection.get()
        version_selection['values'] = data[selected_os]
        version_selection.set('')

    os_selection.bind('<<ComboboxSelected>>', update_version_list)

    def on_update():
        selected_os = os_selection.get()
        selected_version = version_selection.get()
        if not selected_os or not selected_version:
            messagebox.showwarning("Warning", "Please select both OS and Version.")
            return
        update_ini(selected_os, selected_version, "C:/path/to/rdpwrap.ini")

    ttk.Button(root, text="Update INI File", command=on_update).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
