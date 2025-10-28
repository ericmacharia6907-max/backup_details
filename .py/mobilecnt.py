import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock

CONTACTS_FILE = "contacts.txt"

class ContactBook(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 30
        self.spacing = 15

        self.inputs = {}

        # Create fields with default font
        for field in ["First Name", "Second Name", "Email", "Mobile Number"]:
            label = Label(text=field, size_hint_y=None, height=30, font_size=18)
            input_field = TextInput(multiline=False, size_hint_y=None, height=40, font_size=16)
            self.add_widget(label)
            self.add_widget(input_field)
            self.inputs[field] = input_field
            input_field.opacity = 0  # Start hidden for animation

        # Animate input fields fade-in
        delay = 0
        for input_field in self.inputs.values():
            Clock.schedule_once(lambda dt, f=input_field: self.fade_in(f), delay)
            delay += 0.3

        # Stylish Add Contact button with improved colors
        add_btn = Button(text="Add Contact",
                         size_hint_y=None, height=50,
                         font_size=20,
                         background_color=(0.2, 0.6, 0.86, 1),  # Blue color
                         color=(1, 1, 1, 1))  # White text
        add_btn.bind(on_press=self.add_contact)
        add_btn.opacity = 0
        self.add_widget(add_btn)
        Clock.schedule_once(lambda dt: self.fade_in(add_btn), delay)

        # Contacts display area
        self.contacts_layout = BoxLayout(orientation="vertical", size_hint_y=None)
        self.contacts_layout.bind(minimum_height=self.contacts_layout.setter('height'))
        self.add_widget(Label(text="Contacts:", size_hint_y=None, height=30, font_size=20))
        self.add_widget(self.contacts_layout)

        self.contacts = []
        self.load_contacts()
        self.update_contacts()

    def fade_in(self, widget):
        Animation(opacity=1, duration=0.6).start(widget)

    def add_contact(self, instance):
        contact = ", ".join(self.inputs[field].text.strip() for field in self.inputs)
        if any(len(self.inputs[field].text.strip()) == 0 for field in self.inputs):
            return  # Ignore if any field empty; add popup alerts if needed
        if contact not in self.contacts:
            self.contacts.append(contact)
            self.save_contacts()
            self.update_contacts()
            for input_field in self.inputs.values():
                input_field.text = ""

    def update_contacts(self):
        self.contacts_layout.clear_widgets()
        for c in self.contacts:
            self.contacts_layout.add_widget(Label(text=c, font_size=16, size_hint_y=None, height=25))

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

class ContactBookApp(App):
    def build(self):
        return ContactBook()

if __name__ == "__main__":
    ContactBookApp().run()
