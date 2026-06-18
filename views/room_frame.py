from tkinter import messagebox
from typing import Callable

import customtkinter as ctk

from db import Room
from features.room import create_room, delete_room, get_rooms, update_room


class RoomFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.is_admin = None

        # SearchBar
        search_bar = ctk.CTkFrame(self)
        search_bar.pack(fill="x", padx=10, pady=5)

        search_row = ctk.CTkFrame(search_bar)
        search_row.pack()

        self.search_status_option = ctk.CTkOptionMenu(
            search_row, values=["all", "available", "occupied", "maintaining"]
        )
        self.search_status_option.pack(side="left", padx=5)

        self.search_type_option = ctk.CTkOptionMenu(
            search_row, values=["all", "small", "medium", "large"]
        )
        self.search_type_option.pack(side="left", padx=5)
        self.search_floor_input = ctk.CTkEntry(search_row, placeholder_text="Floor")
        self.search_floor_input.pack(side="left", padx=5)

        ctk.CTkButton(search_row, text="Search", command=self.on_search).pack(
            side="left", padx=5
        )
        ctk.CTkButton(search_row, text="Reset", command=self.on_reset_search).pack(
            side="left", padx=5
        )

        # RoomList
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10)
        ctk.CTkLabel(header, text="ID", width=60).pack(side="left")
        ctk.CTkLabel(header, text="Type", width=100).pack(side="left")
        ctk.CTkLabel(header, text="Floor", width=60).pack(side="left")
        ctk.CTkLabel(header, text="Status", width=100).pack(side="left")

        self.room_list = ctk.CTkScrollableFrame(self)
        self.room_list.pack(fill="both", expand=True, padx=10, pady=5)

        # CreateRoomForm (admin only, hidden by default)
        self.create_form = ctk.CTkFrame(self)
        form_row = ctk.CTkFrame(self.create_form)
        form_row.pack()

        self.create_type_option = ctk.CTkOptionMenu(
            form_row, values=["small", "medium", "large"]
        )
        self.create_type_option.pack(side="left", padx=5)
        self.create_floor_input = ctk.CTkEntry(form_row, placeholder_text="Floor")
        self.create_floor_input.pack(side="left", padx=5)
        ctk.CTkButton(form_row, text="Create", command=self.on_create).pack(
            side="left", padx=5
        )

    def on_search(self):
        try:
            _type = self.search_type_option.get()
            _type = None if _type == "all" else _type

            _floor = self.search_floor_input.get()
            _floor = None if not _floor else int(_floor)

        except Exception:
            messagebox.showerror(
                "Error",
                "Search parameter 'floor' should be number start from 1 or empty.",
            )
            return

        try:
            self.show_rooms(get_rooms(None, _type, _floor))
        except Exception as e:
            messagebox.showerror("Error", e)

    def on_reset_search(self):
        try:
            # reset filter components
            self.search_status_option.set("all")
            self.search_type_option.set("all")
            self.search_floor_input.delete(0, "end")

            self.show_rooms(get_rooms())
        except Exception as e:
            messagebox.showerror("Error", e)

    def on_create(self):
        try:
            _type = self.create_type_option.get()
            # _type = None if _type == "all" else _type

            _floor = self.create_floor_input.get()
            _floor = int(_floor)

        except Exception:
            messagebox.showerror(
                "Error",
                "Search parameter 'floor' should be number start from 1 or empty.",
            )
            return
        try:
            create_room(_type, _floor)
            self.create_type_option.set("small")
            self.create_floor_input.delete(0, "end")

            self.search_status_option.set("all")
            self.search_type_option.set("all")
            self.search_floor_input.delete(0, "end")

            self.show_rooms(get_rooms())
        except Exception as e:
            messagebox.showerror("Error", e)

    def on_delete(self, id: int):
        try:
            delete_room(id)

            self.search_status_option.set("all")
            self.search_type_option.set("all")
            self.search_floor_input.delete(0, "end")

            self.show_rooms(get_rooms())
        except Exception as e:
            messagebox.showerror("Error", e)

    def on_update(self, id: int, type: str, floor: int):
        try:
            update_room(id, type, floor)

            self.search_status_option.set("all")
            self.search_type_option.set("all")
            self.search_floor_input.delete(0, "end")

            self.show_rooms(get_rooms())
        except Exception as e:
            messagebox.showerror("Error", e)

    def _resumed(self):
        role = self.winfo_toplevel().context.current_user.role
        self.is_admin = role == "admin"

        if self.is_admin:
            self.create_form.pack(fill="x", padx=10, pady=5)
        else:
            self.create_form.pack_forget()

        self.show_rooms(get_rooms())

    def show_rooms(self, rooms: list[Room]):
        for widget in self.room_list.winfo_children():
            widget.destroy()
        for room in rooms:
            RoomItem(
                self.room_list,
                room,
                "available",
                is_admin=self.is_admin,
                on_delete=self.on_delete,
                on_update=self.on_update,
            ).pack(fill="x")
        pass


class RoomItem(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        room: Room,
        status: str,
        is_admin: bool = False,
        on_delete: Callable[[int], None] | None = None,
        on_update: Callable[[int, str, int], None] | None = None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)

        self.room = room
        self.edit_mode = False
        self.handle_delete = on_delete
        self.handle_update = on_update

        # View frame
        self.view_frame = ctk.CTkFrame(self)
        self.view_frame.pack(fill="x")

        ctk.CTkLabel(self.view_frame, text=str(room.id), width=60).pack(side="left")
        ctk.CTkLabel(self.view_frame, text=room.type, width=100).pack(side="left")
        ctk.CTkLabel(self.view_frame, text=str(room.floor), width=60).pack(side="left")
        ctk.CTkLabel(self.view_frame, text=status, width=100).pack(side="left")

        if is_admin:
            ctk.CTkButton(
                self.view_frame, text="Edit", width=60, command=self._enter_edit
            ).pack(side="left")
            ctk.CTkButton(
                self.view_frame, text="Remove", width=60, command=self.on_delete
            ).pack(side="left")

        # Edit frame
        self.edit_frame = ctk.CTkFrame(self)

        self.edit_id_label = ctk.CTkLabel(self.edit_frame, text=str(room.id), width=60)
        self.edit_id_label.pack(side="left")
        self.type_option = ctk.CTkOptionMenu(
            self.edit_frame, values=["small", "medium", "large"], width=100
        )
        self.type_option.pack(side="left")
        self.floor_entry = ctk.CTkEntry(self.edit_frame, width=60)
        self.floor_entry.pack(side="left")
        ctk.CTkButton(
            self.edit_frame, text="Confirm", width=60, command=self.on_update
        ).pack(side="left")
        ctk.CTkButton(
            self.edit_frame, text="Cancel", width=60, command=self._exit_edit
        ).pack(side="left")

    def _refresh(self):
        if self.edit_mode:
            self.view_frame.pack_forget()
            self.edit_frame.pack(fill="x")
        else:
            self.edit_frame.pack_forget()
            self.view_frame.pack(fill="x")

    def _enter_edit(self):
        self.type_option.set(self.room.type)
        self.floor_entry.delete(0, "end")
        self.floor_entry.insert(0, str(self.room.floor))
        self.edit_mode = True
        self._refresh()

    def _exit_edit(self):
        self.edit_mode = False
        self._refresh()

    def on_update(self):
        if self.handle_update:
            try:
                _type = self.type_option.get()
                _floor = int(self.floor_entry.get())
            except Exception:
                messagebox.showerror(
                    "Error",
                    "Parameter 'floor' should be number start from 1",
                )
                return
            self.handle_update(self.room.id, _type, _floor)
        pass

    def on_delete(self):
        if self.handle_delete:
            self.handle_delete(self.room.id)
