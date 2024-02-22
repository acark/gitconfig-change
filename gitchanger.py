import tkinter as tk
from tkinter import messagebox
import subprocess
import json

# Path to the configuration file
config_file = 'git_profiles_config.json'

# Function to set git config
def set_git_config(name, email):
    subprocess.run(["git", "config", "--global", "user.name", name])
    subprocess.run(["git", "config", "--global", "user.email", email])

# Function to load configuration from JSON
def load_config():
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"profiles": []}

# Function to save configuration to JSON
def save_config(config):
    try:

        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
    except:
            messagebox.showwarning("Fail", "Git profile is not saved!")

# Main application class
class GitProfileManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Git Profile Manager")
        self.geometry("400x400")
        
        self.config = load_config()
        self.profiles = self.config.get("profiles", [])
        
        self.create_widgets()
        self.update_listbox()

    def create_widgets(self):
        # Input fields and labels
        tk.Label(self, text="Name:").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()
        
        tk.Label(self, text="Email:").pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack()
        
        # Buttons
        tk.Button(self, text="Save Profile", command=self.add_profile).pack()

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=15)
        
        tk.Button(self, text="Set Active", command=self.set_active_profile).pack()

    def add_profile(self):
        name = self.name_entry.get()
        email = self.email_entry.get()

        if name.strip() == "" or email.strip() == "":
            messagebox.showwarning("Warning", "name or email missing")
            return;

        profile = f"{name} <{email}>"
        self.profiles.append(profile)
        self.update_listbox()
        self.save_current_config()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for profile in self.profiles:
            self.listbox.insert(tk.END, profile)

    def set_active_profile(self):
        selection = self.listbox.curselection()
        if selection:
            selected_profile = self.profiles[selection[0]]
            name, email = selected_profile.rsplit(' <', 1)
            email = email.rstrip('>')
            set_git_config(name, email)
            messagebox.showinfo("Success", "Git profile updated successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a profile")

    def save_current_config(self):
        config = {'profiles': self.profiles}
        save_config(config)

if __name__ == "__main__":
    app = GitProfileManager()
    app.mainloop()
