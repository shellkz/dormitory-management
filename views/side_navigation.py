import customtkinter as ctk


class SideNavigation(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, width=160, **kwargs)
        self.pack_propagate(False)

        ctk.CTkLabel(self, text="Menu", font=ctk.CTkFont(size=14, weight="bold")).pack(
            pady=(20, 10)
        )

        self._admin_btns = []
        for text, name in [
            ("Room Management", "room"),
            ("Assign Room", "assign"),
            ("Maintenance", "maintenance"),
            ("Report", "report"),
        ]:
            btn = ctk.CTkButton(
                self,
                text=text,
                width=140,
                command=lambda n=name: self.winfo_toplevel().goto(n),
            )
            self._admin_btns.append(btn)

        self._resident_btns = []
        for text, name in [
            ("Room Search", "room"),
            ("Maintenance", "maintenance"),
        ]:
            btn = ctk.CTkButton(
                self,
                text=text,
                width=140,
                command=lambda n=name: self.winfo_toplevel().goto(n),
            )
            self._resident_btns.append(btn)

    def _resumed(self, role: str):
        for btn in self._admin_btns + self._resident_btns:
            btn.pack_forget()

        btns = self._admin_btns if role == "admin" else self._resident_btns
        for btn in btns:
            btn.pack(pady=5, padx=10)
