from tkinter import messagebox

import customtkinter as ctk

from db import StayRead
from features.assign import check_in, check_out, get_stays


class AssignFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # TabContainer
        self.tab_container = ctk.CTkTabview(self, height=70)
        self.tab_container.pack(fill="x", padx=10, pady=(5, 0))
        self._build_check_in_form(self.tab_container.add("辦理入住"))
        self._build_check_out_form(self.tab_container.add("辦理退房"))

        # content: ColumnHeader (row 0) + ListView (row 1)
        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=10, pady=5)
        self.content.rowconfigure(1, weight=1)
        self.content.grid_columnconfigure(6, weight=1)

        # ColumnHeader
        ctk.CTkLabel(self.content, text="Room ID", width=80).grid(row=0, column=0, padx=2)
        ctk.CTkLabel(self.content, text="Type", width=100).grid(row=0, column=1, padx=2)
        ctk.CTkLabel(self.content, text="Floor", width=60).grid(row=0, column=2, padx=2)
        ctk.CTkLabel(self.content, text="Resident", width=120).grid(row=0, column=3, padx=2)
        ctk.CTkLabel(self.content, text="Check-In At", width=160).grid(row=0, column=4, padx=2)
        ctk.CTkLabel(self.content, text="Check-Out At", width=160).grid(row=0, column=5, padx=2)

        # ListView
        self.assign_list = ctk.CTkScrollableFrame(self.content)
        self.assign_list.grid(row=1, column=0, columnspan=7, sticky="nsew")

    def _build_check_in_form(self, tab):
        tab.grid_columnconfigure(1, minsize=104)  # Type spacer   (100 + 2+2)
        tab.grid_columnconfigure(2, minsize=64)   # Floor spacer  (60  + 2+2)
        tab.grid_columnconfigure(6, weight=1)

        self.check_in_room_id_entry = ctk.CTkEntry(tab, width=80, placeholder_text="Room ID")
        self.check_in_room_id_entry.grid(row=0, column=0, padx=2, pady=5)

        self.check_in_username_entry = ctk.CTkEntry(tab, width=120, placeholder_text="Username")
        self.check_in_username_entry.grid(row=0, column=3, padx=2, pady=5)

        ctk.CTkButton(tab, text="Check In", command=self._on_check_in, width=80).grid(
            row=0, column=4, padx=2, pady=5
        )

    def _build_check_out_form(self, tab):
        tab.grid_columnconfigure(1, minsize=104)  # Type spacer     (100 + 2+2)
        tab.grid_columnconfigure(2, minsize=64)   # Floor spacer    (60  + 2+2)
        tab.grid_columnconfigure(3, minsize=124)  # Resident spacer (120 + 2+2)
        tab.grid_columnconfigure(6, weight=1)

        self.check_out_room_id_entry = ctk.CTkEntry(tab, width=80, placeholder_text="Room ID")
        self.check_out_room_id_entry.grid(row=0, column=0, padx=2, pady=5)

        ctk.CTkButton(tab, text="Check Out", command=self._on_check_out, width=80).grid(
            row=0, column=4, padx=2, pady=5
        )

    def _on_check_in(self):
        try:
            _username = self.check_in_username_entry.get()
            _room_id = int(self.check_in_room_id_entry.get())
        except Exception:
            messagebox.showerror(
                "Error",
                "Parameter 'room_id' should be number start from 0.",
            )
            return
        try:
            check_in(_username, _room_id)
            self.show_stays(get_stays())
        except Exception as e:
            messagebox.showerror("Error", e)

    def _on_check_out(self):
        try:
            _room_id = int(self.check_out_room_id_entry.get())
        except Exception:
            messagebox.showerror(
                "Error",
                "Parameter 'room_id' should be number start from 0.",
            )
            return
        try:
            check_out(_room_id)
            self.show_stays(get_stays())
        except Exception as e:
            messagebox.showerror("Error", e)

    def _resumed(self):
        stays = get_stays()
        print(f"{len(stays)} stays found.")
        self.show_stays(stays)

    def show_stays(self, stays: list[StayRead]):
        for widget in self.assign_list.winfo_children():
            widget.destroy()
        for stay in stays:
            AssignItem(self.assign_list, stay).pack(fill="x")


class AssignItem(ctk.CTkFrame):
    def __init__(self, parent, stay: StayRead, **kwargs):
        super().__init__(parent, **kwargs)

        hbox = ctk.CTkFrame(self)
        hbox.pack(fill="x")

        ctk.CTkLabel(hbox, text=str(stay.room_id), width=80).grid(row=0, column=0, padx=2)
        ctk.CTkLabel(hbox, text=stay.type, width=100).grid(row=0, column=1, padx=2)
        ctk.CTkLabel(hbox, text=str(stay.floor), width=60).grid(row=0, column=2, padx=2)

        if stay.check_in_at:
            ctk.CTkLabel(hbox, text=stay.username, width=120).grid(row=0, column=3, padx=2)
            ctk.CTkLabel(hbox, text=stay.check_in_at, width=160).grid(row=0, column=4, padx=2)

            if stay.check_out_at:
                ctk.CTkLabel(hbox, text=stay.check_out_at, width=160).grid(
                    row=0, column=5, padx=2
                )
