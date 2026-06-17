import customtkinter as ctk


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.welcome_label = ctk.CTkLabel(self, text="")
        self.welcome_label.pack(pady=10)

        # Admin panel
        self.admin_panel = ctk.CTkFrame(self)
        ctk.CTkButton(
            self.admin_panel,
            text="Room Management",
            command=lambda: self.master.goto("auth"),
        ).pack(pady=5)
        ctk.CTkButton(
            self.admin_panel,
            text="Assign Room",
            command=lambda: self.master.goto("auth"),
        ).pack(pady=5)
        ctk.CTkButton(
            self.admin_panel,
            text="Maintenance",
            command=lambda: self.master.goto("auth"),
        ).pack(pady=5)
        ctk.CTkButton(
            self.admin_panel,
            text="Report",
            command=lambda: self.master.goto("auth"),
        ).pack(pady=5)

        # Resident panel
        self.resident_panel = ctk.CTkFrame(self)
        ctk.CTkButton(
            self.resident_panel,
            text="Room Search",
            command=lambda: self.master.goto("auth"),
        ).pack(pady=5)
        ctk.CTkButton(
            self.resident_panel,
            text="Maintenance",
            command=lambda: self.master.goto("auth"),
        ).pack(pady=5)

    def _resumed(self):
        user = self.master.context.current_user
        self.welcome_label.configure(text=f"Welcome, {user.username}")

        if user.role == "admin":
            self.resident_panel.pack_forget()
            self.admin_panel.pack()
        else:
            self.admin_panel.pack_forget()
            self.resident_panel.pack()
