import customtkinter as ctk
from tkinter import messagebox
import os

ctk.set_appearance_mode("System")  # "Dark", "Light", or "System"
ctk.set_default_color_theme("blue")  # Choose from "blue", "green", "dark-blue"

CONTACTS_FILE = "contacts.txt"

class ContactBookApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Contact Book")
        self.geometry("500x500")
        self.icon_path = "your_icon.ico"
        if os.path.exists(self.icon_path):
            self.iconbitmap(self.icon_path)

        self.font_main = ctk.CTkFont(family="Segoe UI", size=20, weight="bold")
        self.font_label = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_entry = ctk.CTkFont(family="Consolas", size=14)
        self.font_button = ctk.CTkFont(family="Segoe UI", size=12, weight="bold")

        self.contacts = []
        self.load_contacts()

        # Title label with animation
        self.title_label = ctk.CTkLabel(self, text="Contact Book", font=self.font_main)
        self.title_label.pack(pady=20)
        self.animate_title()

        # Entry fields
        entry_frame = ctk.CTkFrame(self, fg_color="transparent")
        entry_frame.pack(pady=10)

        ctk.CTkLabel(entry_frame, text="Name:", font=self.font_label).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry = ctk.CTkEntry(entry_frame, font=self.font_entry, width=200)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        ctk.CTkLabel(entry_frame, text="Mobile Number:", font=self.font_label).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.mobile_entry = ctk.CTkEntry(entry_frame, font=self.font_entry, width=200)
        self.mobile_entry.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(button_frame, text="Add", font=self.font_button, command=self.add_contact)
        self.add_button.grid(row=0, column=0, padx=10)

        self.delete_button = ctk.CTkButton(button_frame, text="Delete", font=self.font_button, command=self.delete_contact)
        self.delete_button.grid(row=0, column=1, padx=10)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", font=self.font_button, command=self.clear_entries)
        self.clear_button.grid(row=0, column=2, padx=10)

        # Contact Listbox
        self.contact_listbox = ctk.CTkTextbox(self, height=200, width=400, font=self.font_entry, state="disabled", wrap="none", border_width=2)
        self.contact_listbox.pack(pady=15)

        # Populate with loaded contacts
        self.update_listbox()

    def animate_title(self, colors=None, idx=0):
        # Simple color animation
        if colors is None:
            colors = ["#348ceb", "#1be71b", "#eedd44", "#ed3c3c"]
        self.title_label.configure(text_color=colors[idx % len(colors)])
        self.after(600, lambda: self.animate_title(colors, idx + 1))

    def add_contact(self):
        name = self.name_entry.get().strip()
        mobile = self.mobile_entry.get().strip()
        if not name or not mobile:
            messagebox.showwarning("Input Error", "Please enter both name and mobile number.")
            return
        contact = f"{name} - {mobile}"
        if contact in self.contacts:
            messagebox.showinfo("Duplicate", "Contact already exists.")
            return
        self.contacts.append(contact)
        self.save_contacts()
        self.update_listbox()
        self.clear_entries()
        messagebox.showinfo("Success", "Contact added successfully.")

    def delete_contact(self):
        # Ask for line number for deletion
        try:
            line = self.contact_listbox.index("insert").split('.')[0]
            idx = int(line) - 1
            if idx < 0 or idx >= len(self.contacts):
                raise ValueError
            contact = self.contacts.pop(idx)
            self.save_contacts()
            self.update_listbox()
            messagebox.showinfo("Deleted", f"Deleted: {contact}")
        except Exception:
            messagebox.showwarning("Select Error", "Click a contact's line in the list to select and delete.")

    def update_listbox(self):
        self.contact_listbox.configure(state="normal")
        self.contact_listbox.delete("1.0", "end")
        for contact in self.contacts:
            self.contact_listbox.insert("end", contact + '\n')
        self.contact_listbox.configure(state="disabled")

    def clear_entries(self):
        self.name_entry.delete(0, "end")
        self.mobile_entry.delete(0, "end")

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r") as f:
                self.contacts = [line.strip() for line in f if line.strip()]
        else:
            self.contacts = []

    def save_contacts(self):
        with open(CONTACTS_FILE, "w") as f:
            for contact in self.contacts:
                f.write(contact + "\n")

if __name__ == "__main__":
    app = ContactBookApp()
    app.mainloop()
