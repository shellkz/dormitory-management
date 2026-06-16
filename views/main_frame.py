import customtkinter as ctk


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, user, **kwargs):
        super().__init__(parent, **kwargs)
        self.user = user

        self.label = ctk.CTkLabel(self, text=f"Welcome {self.user}")
        self.label.pack(pady=10)
