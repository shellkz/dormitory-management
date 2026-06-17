import customtkinter as ctk

from db import Room


class RoomFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # SearchBar
        search_bar = ctk.CTkFrame(self)
        search_bar.pack(fill="x", padx=10, pady=5)

        search_row = ctk.CTkFrame(search_bar)
        search_row.pack()

        ctk.CTkOptionMenu(
            search_row, values=["available", "occupied", "maintaining"]
        ).pack(side="left", padx=5)
        ctk.CTkOptionMenu(search_row, values=["small", "medium", "large"]).pack(
            side="left", padx=5
        )
        ctk.CTkEntry(search_row, placeholder_text="Floor").pack(side="left", padx=5)
        ctk.CTkButton(search_row, text="Search").pack(side="left", padx=5)
        ctk.CTkButton(search_row, text="Reset").pack(side="left", padx=5)

        # Header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10)

        ctk.CTkLabel(header, text="ID", width=60).pack(side="left")
        ctk.CTkLabel(header, text="Type", width=100).pack(side="left")
        ctk.CTkLabel(header, text="Floor", width=60).pack(side="left")
        ctk.CTkLabel(header, text="Status", width=100).pack(side="left")

        # Room List
        self.room_list = ctk.CTkScrollableFrame(self)
        self.room_list.pack(fill="both", expand=True, padx=10, pady=5)

        # CreateRoomForm (admin only, hidden by default)
        self.create_form = ctk.CTkFrame(self)
        form_row = ctk.CTkFrame(self.create_form)
        form_row.pack()

        ctk.CTkOptionMenu(form_row, values=["small", "medium", "large"]).pack(
            side="left", padx=5
        )
        ctk.CTkEntry(form_row, placeholder_text="Floor").pack(side="left", padx=5)
        ctk.CTkButton(form_row, text="Create").pack(side="left", padx=5)

    def _resumed(self):
        role = self.winfo_toplevel().context.current_user.role
        is_admin = role == "admin"

        if is_admin:
            self.create_form.pack(fill="x", padx=10, pady=5)
        else:
            self.create_form.pack_forget()

        # 清空舊的 RoomItem
        for widget in self.room_list.winfo_children():
            widget.destroy()

        # 重新生成 RoomItem (placeholder)
        for i in range(10):
            RoomItem(
                self.room_list, Room(i, "small", 1), "available", is_admin=is_admin
            ).pack(fill="x")


class RoomItem(ctk.CTkFrame):
    def __init__(
        self, parent, room: Room, status: str, is_admin: bool = False, **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.room = room
        self.edit_mode = False

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
            ctk.CTkButton(self.view_frame, text="Remove", width=60).pack(side="left")

        # Edit frame
        self.edit_frame = ctk.CTkFrame(self)

        ctk.CTkLabel(self.edit_frame, text=str(room.id), width=60).pack(side="left")
        self.type_menu = ctk.CTkOptionMenu(
            self.edit_frame, values=["small", "medium", "large"], width=100
        )
        self.type_menu.pack(side="left")
        self.floor_entry = ctk.CTkEntry(self.edit_frame, width=60)
        self.floor_entry.pack(side="left")
        ctk.CTkButton(self.edit_frame, text="Confirm", width=60).pack(side="left")
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
        self.type_menu.set(self.room.type)
        self.floor_entry.delete(0, "end")
        self.floor_entry.insert(0, str(self.room.floor))
        self.edit_mode = True
        self._refresh()

    def _exit_edit(self):
        self.edit_mode = False
        self._refresh()
