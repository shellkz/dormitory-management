from tkinter import messagebox

import customtkinter as ctk

from features.auth import login
from state import AppState


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, context: AppState, on_login_success, **kwargs):
        super().__init__(parent, **kwargs)
        self.context = context
        self.on_login_success = on_login_success

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(container, text="登入", font=("Arial", 20, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 24)
        )

        ctk.CTkLabel(container, text="帳號").grid(
            row=1, column=0, sticky="e", padx=(0, 8), pady=6
        )
        self.username_input = ctk.CTkEntry(
            container, width=200, placeholder_text="請輸入帳號"
        )
        self.username_input.grid(row=1, column=1, pady=6)

        ctk.CTkLabel(container, text="密碼").grid(
            row=2, column=0, sticky="e", padx=(0, 8), pady=6
        )
        self.password_input = ctk.CTkEntry(
            container, width=200, placeholder_text="請輸入密碼", show="*"
        )
        self.password_input.grid(row=2, column=1, pady=6)

        ctk.CTkButton(
            container, text="登入", width=200, command=self.on_try_login
        ).grid(row=3, column=1, pady=(16, 0))

    def on_try_login(self):
        username = self.username_input.get()
        password = self.password_input.get()
        try:
            user = login(username, password)
            self.on_login_success(user)
        except Exception as e:
            messagebox.showerror("錯誤", e)
            pass
