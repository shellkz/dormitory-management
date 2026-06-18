from tkinter import messagebox

import customtkinter as ctk

from db import StayRead
from features.assign import check_in, check_out, get_stays


class AssignFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # CheckInForm
        self.check_in_form = ctk.CTkFrame(self)
        self.check_in_form.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.check_in_form, text="辦理入住").pack(anchor="w", padx=5)

        check_in_row = ctk.CTkFrame(self.check_in_form)
        check_in_row.pack()

        self.check_in_username_entry = ctk.CTkEntry(
            check_in_row, placeholder_text="Username"
        )
        self.check_in_username_entry.pack(side="left", padx=5)

        self.check_in_room_id_entry = ctk.CTkEntry(
            check_in_row, placeholder_text="Room ID"
        )
        self.check_in_room_id_entry.pack(side="left", padx=5)

        ctk.CTkButton(check_in_row, text="Check In", command=self._on_check_in).pack(
            side="left", padx=5
        )

        # CheckOutForm
        self.check_out_form = ctk.CTkFrame(self)
        self.check_out_form.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.check_out_form, text="辦理退房").pack(anchor="w", padx=5)

        check_out_row = ctk.CTkFrame(self.check_out_form)
        check_out_row.pack()

        self.check_out_room_id_entry = ctk.CTkEntry(
            check_out_row, placeholder_text="Room ID"
        )
        self.check_out_room_id_entry.pack(side="left", padx=5)

        ctk.CTkButton(check_out_row, text="Check Out", command=self._on_check_out).pack(
            side="left", padx=5
        )

        # AssignList header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10)
        ctk.CTkLabel(header, text="Room ID", width=80).pack(side="left")
        ctk.CTkLabel(header, text="Type", width=100).pack(side="left")
        ctk.CTkLabel(header, text="Floor", width=60).pack(side="left")
        ctk.CTkLabel(header, text="Resident", width=120).pack(side="left")
        ctk.CTkLabel(header, text="Check-In At", width=160).pack(side="left")
        ctk.CTkLabel(header, text="Check-Out At", width=160).pack(side="left")

        self.assign_list = ctk.CTkScrollableFrame(self)
        self.assign_list.pack(fill="both", expand=True, padx=10, pady=5)

    def _on_check_in(self):
        # verify username and room_id
        try:
            _username = self.check_in_username_entry.get()
            _room_id = self.check_in_room_id_entry.get()
            _room_id = int(_room_id)
        except Exception:
            messagebox.showerror(
                "Error",
                "Parameter 'room_id' should be number start from 0.",
            )
            return
        try:
            check_in(_username, _room_id)
            self.show_stays(get_stays())
            pass
        except Exception as e:
            messagebox.showerror("Error", e)

    def _on_check_out(self):
        # verify room_id
        try:
            _room_id = self.check_out_room_id_entry.get()
            _room_id = int(_room_id)
        except Exception:
            messagebox.showerror(
                "Error",
                "Parameter 'room_id' should be number start from 0.",
            )
            return
        try:
            check_out(_room_id)
            self.show_stays(get_stays())
            pass
        except Exception as e:
            messagebox.showerror("Error", e)

    def _resumed(self):
        stays = get_stays()
        print(f"{len(stays)} stays found.")
        self.show_stays(stays)
        pass

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

        ctk.CTkLabel(hbox, text=str(stay.room_id), width=80).pack(side="left")
        ctk.CTkLabel(hbox, text=stay.type, width=100).pack(side="left")
        ctk.CTkLabel(hbox, text=str(stay.floor), width=60).pack(side="left")

        if stay.check_in_at:
            ctk.CTkLabel(hbox, text=stay.username, width=120).pack(side="left")
            ctk.CTkLabel(hbox, text=stay.check_in_at, width=160).pack(side="left")

            if stay.check_out_at:
                ctk.CTkLabel(hbox, text=stay.check_out_at, width=160).pack(side="left")
