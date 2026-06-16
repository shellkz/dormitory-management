import customtkinter as ctk


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, on_login_success, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_login_success = on_login_success

        self.btn = ctk.CTkButton(self, text="登入", command=self.handle_login)
        self.btn.pack(pady=10)

    def handle_login(self):
        self.on_login_success("user")
