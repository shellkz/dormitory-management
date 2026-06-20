from tkinter import messagebox
from typing import Callable

import customtkinter as ctk

from db import RoomRead
from features.room import (
    VALID_STATUS,
    VALID_TYPE,
    create_room,
    delete_room,
    get_rooms,
    update_room,
)


class RoomFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.is_admin = None

        # TabContainer (admin only, packed dynamically in _resumed)
        self.tab_container = ctk.CTkTabview(self, height=70)
        self._build_create_form(self.tab_container.add("新增房間"))

        # content: SearchRoomForm (row 0) + ColumnNameHeader (row 1) + ListView (row 2)
        # All three share the same grid so columns align automatically.
        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=10, pady=5)
        self.content.rowconfigure(2, weight=1)
        self.content.grid_columnconfigure(0, minsize=60)  # ID — no search widget here
        self.content.grid_columnconfigure(6, weight=1)    # spacer: absorbs remaining width

        # SearchRoomForm
        self.search_type_option = ctk.CTkOptionMenu(
            self.content, values=["all"] + sorted(VALID_TYPE), width=100
        )
        self.search_type_option.grid(row=0, column=1, padx=2, pady=5)

        self.search_floor_input = ctk.CTkEntry(
            self.content, width=60, placeholder_text="Floor"
        )
        self.search_floor_input.grid(row=0, column=2, padx=2, pady=5)

        self.search_status_option = ctk.CTkOptionMenu(
            self.content, values=["all"] + sorted(VALID_STATUS), width=100
        )
        self.search_status_option.grid(row=0, column=3, padx=2, pady=5)

        ctk.CTkButton(
            self.content, text="Search", command=self.on_search, width=80
        ).grid(row=0, column=4, padx=2, pady=5)
        ctk.CTkButton(
            self.content, text="Reset", command=self.on_reset_search, width=80
        ).grid(row=0, column=5, padx=2, pady=5)

        # ColumnNameHeader
        ctk.CTkLabel(self.content, text="ID", width=60).grid(row=1, column=0, padx=2)
        ctk.CTkLabel(self.content, text="Type", width=100).grid(row=1, column=1, padx=2)
        ctk.CTkLabel(self.content, text="Floor", width=60).grid(row=1, column=2, padx=2)
        ctk.CTkLabel(self.content, text="Status", width=100).grid(
            row=1, column=3, padx=2
        )

        # ListView
        self.room_list = ctk.CTkScrollableFrame(self.content)
        self.room_list.grid(row=2, column=0, columnspan=7, sticky="nsew")

    def _build_create_form(self, tab):
        tab.grid_columnconfigure(0, minsize=64)  # 60 (width) + 2+2 (padx) to match list items
        tab.grid_columnconfigure(6, weight=1)

        self.create_type_option = ctk.CTkOptionMenu(tab, values=sorted(VALID_TYPE), width=100)
        self.create_type_option.grid(row=0, column=1, padx=2, pady=5)

        self.create_floor_input = ctk.CTkEntry(tab, width=60, placeholder_text="Floor")
        self.create_floor_input.grid(row=0, column=2, padx=2, pady=5)

        ctk.CTkButton(tab, text="Create", command=self.on_create, width=80).grid(
            row=0, column=4, padx=2, pady=5
        )

    def on_search(self):
        try:
            _status = self.search_status_option.get()
            _status = None if _status == "all" else _status

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
            self.show_rooms(get_rooms(_status, _type, _floor))
        except Exception as e:
            messagebox.showerror("Error", e)

    def on_reset_search(self):
        try:
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
            self.tab_container.pack(fill="x", padx=10, pady=(5, 0), before=self.content)
        else:
            self.tab_container.pack_forget()

        self.show_rooms(get_rooms())

    def show_rooms(self, rooms: list[RoomRead]):
        for widget in self.room_list.winfo_children():
            widget.destroy()
        for room in rooms:
            RoomItem(
                self.room_list,
                room,
                is_admin=self.is_admin,
                on_delete=self.on_delete,
                on_update=self.on_update,
            ).pack(fill="x")


class RoomItem(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        room: RoomRead,
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

        ctk.CTkLabel(self.view_frame, text=str(room.id), width=60).grid(
            row=0, column=0, padx=2
        )
        ctk.CTkLabel(self.view_frame, text=room.type, width=100).grid(
            row=0, column=1, padx=2
        )
        ctk.CTkLabel(self.view_frame, text=str(room.floor), width=60).grid(
            row=0, column=2, padx=2
        )
        ctk.CTkLabel(self.view_frame, text=room.status, width=100).grid(
            row=0, column=3, padx=2
        )

        if is_admin:
            ctk.CTkButton(
                self.view_frame, text="Edit", width=80, command=self._enter_edit
            ).grid(row=0, column=4, padx=2)
            ctk.CTkButton(
                self.view_frame, text="Remove", width=80, command=self.on_delete
            ).grid(row=0, column=5, padx=2)

        # Edit frame
        self.edit_frame = ctk.CTkFrame(self)

        self.edit_id_label = ctk.CTkLabel(self.edit_frame, text=str(room.id), width=60)
        self.edit_id_label.grid(row=0, column=0, padx=2)

        self.type_option = ctk.CTkOptionMenu(
            self.edit_frame, values=["small", "medium", "large"], width=100
        )
        self.type_option.grid(row=0, column=1, padx=2)

        self.floor_entry = ctk.CTkEntry(self.edit_frame, width=60)
        self.floor_entry.grid(row=0, column=2, padx=2)

        self.edit_frame.grid_columnconfigure(
            3, minsize=100
        )  # status spacer (not editable)

        ctk.CTkButton(
            self.edit_frame, text="Confirm", width=80, command=self.on_update
        ).grid(row=0, column=4, padx=2)
        ctk.CTkButton(
            self.edit_frame, text="Cancel", width=80, command=self._exit_edit
        ).grid(row=0, column=5, padx=2)

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

    def on_delete(self):
        if self.handle_delete:
            self.handle_delete(self.room.id)
