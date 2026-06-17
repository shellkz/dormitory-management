import customtkinter as ctk

from state import AppState


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, context: AppState, **kwargs):
        super().__init__(parent, **kwargs)
        self.context = context
        self.label = ctk.CTkLabel(self, text="")
        self.label.pack(pady=10)

    def _resumed(self):
        self.label.configure(text=f"Welcome {self.context.current_user.username}")

        pass
