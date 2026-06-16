import customtkinter as ctk


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.user = ""
        self.label = ctk.CTkLabel(self, text=f"Welcome {self.user}")
        self.label.pack(pady=10)

    def _resumed(self, username):
        self.user = username
        self.label.configure(text=f"Welcome {self.user}")

        pass
