import customtkinter as ctk


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.welcome_label = ctk.CTkLabel(self, text="")
        self.welcome_label.pack(pady=10)

    def _resumed(self):
        user = self.winfo_toplevel().context.current_user
        self.welcome_label.configure(text=f"Welcome, {user.username}")
