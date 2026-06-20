from tkinter import messagebox

import customtkinter as ctk

from features.auth import login, register


class AuthFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        tabs = ctk.CTkTabview(self, width=320)
        tabs.place(relx=0.5, rely=0.5, anchor="center")

        self._build_login_tab(tabs.add("登入"))
        self._build_register_tab(tabs.add("註冊"))

    def _build_login_tab(self, tab):
        ctk.CTkLabel(tab, text="帳號").grid(
            row=0, column=0, sticky="e", padx=(0, 8), pady=6
        )
        self.login_username = ctk.CTkEntry(
            tab, width=200, placeholder_text="請輸入帳號"
        )
        self.login_username.grid(row=0, column=1, pady=6)

        ctk.CTkLabel(tab, text="密碼").grid(
            row=1, column=0, sticky="e", padx=(0, 8), pady=6
        )
        self.login_password = ctk.CTkEntry(
            tab, width=200, placeholder_text="請輸入密碼", show="*"
        )
        self.login_password.grid(row=1, column=1, pady=6)

        ctk.CTkButton(tab, text="登入", width=200, command=self.on_try_login).grid(
            row=2, column=1, pady=(16, 8)
        )

    def _build_register_tab(self, tab):
        ctk.CTkLabel(tab, text="帳號").grid(
            row=0, column=0, sticky="e", padx=(0, 8), pady=6
        )
        self.reg_username = ctk.CTkEntry(tab, width=200, placeholder_text="請輸入帳號")
        self.reg_username.grid(row=0, column=1, pady=6)

        ctk.CTkLabel(tab, text="密碼").grid(
            row=1, column=0, sticky="e", padx=(0, 8), pady=6
        )
        self.reg_password = ctk.CTkEntry(
            tab, width=200, placeholder_text="請輸入密碼", show="*"
        )
        self.reg_password.grid(row=1, column=1, pady=6)

        ctk.CTkButton(tab, text="註冊", width=200, command=self.on_try_register).grid(
            row=3, column=1, pady=(16, 8)
        )

    def on_try_login(self):
        username = self.login_username.get()
        password = self.login_password.get()
        try:
            user = login(username, password)
            self.winfo_toplevel().context.current_user = user
            self.winfo_toplevel().goto("room")

        except Exception as e:
            messagebox.showerror("錯誤", e)

    def on_try_register(self):
        username = self.reg_username.get()
        password = self.reg_password.get()

        try:
            register(username, password)
            messagebox.showinfo("成功", "註冊成功，請登入")
            self.reg_username.delete(0, "end")
            self.reg_password.delete(0, "end")

        except Exception as e:
            messagebox.showerror("錯誤", e)
