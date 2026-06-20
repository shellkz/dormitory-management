from tkinter import messagebox

import customtkinter as ctk

from db import RequestMaintenanceRead
from features.maintenance import (
    complete_request,
    get_requests,
    process_request,
    submit_request,
)


class MaintenanceFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.is_admin = None
        self.current_user = None
        self.current_username = None

        # Submit tab (all users)
        self.tab_container = ctk.CTkTabview(self, height=70)
        self.tab_container.pack(fill="x", padx=10, pady=(5, 0))
        self._build_submit_form(self.tab_container.add("提交申請"))

        # Admin-only action tabs — packed dynamically in _resumed
        self.admin_tab_container = ctk.CTkTabview(self, height=70)
        self._build_process_form(self.admin_tab_container.add("處理申請"))
        self._build_complete_form(self.admin_tab_container.add("完成申請"))

        # content: SearchForm (row 0) + ColumnHeader (row 1) + ListView (row 2)
        self.content = ctk.CTkFrame(self)
        self.content.pack(fill="both", expand=True, padx=10, pady=5)
        self.content.rowconfigure(2, weight=1)
        self.content.grid_columnconfigure(6, weight=1)

        # SearchForm (row 0) — admin-only entries hidden via grid_remove in _resumed
        self.search_room_id_entry = ctk.CTkEntry(
            self.content, width=60, placeholder_text="Room"
        )
        self.search_room_id_entry.grid(row=0, column=1, padx=2, pady=5)

        self.search_username_entry = ctk.CTkEntry(
            self.content, width=100, placeholder_text="Username"
        )
        self.search_username_entry.grid(row=0, column=2, padx=2, pady=5)

        self.search_status_option = ctk.CTkOptionMenu(
            self.content,
            values=["all", "submitted", "processing", "completed"],
            width=140,
        )
        self.search_status_option.grid(row=0, column=3, padx=2, pady=5)

        ctk.CTkButton(
            self.content, text="Search", command=self._on_search, width=80
        ).grid(row=0, column=4, padx=2, pady=5)

        # ColumnHeader (row 1)
        ctk.CTkLabel(self.content, text="ID", width=40).grid(row=1, column=0, padx=2)
        ctk.CTkLabel(self.content, text="Room", width=60).grid(row=1, column=1, padx=2)
        ctk.CTkLabel(self.content, text="Submitter", width=100).grid(row=1, column=2, padx=2)
        ctk.CTkLabel(self.content, text="Submitted At", width=140).grid(row=1, column=3, padx=2)
        ctk.CTkLabel(self.content, text="Processing At", width=140).grid(row=1, column=4, padx=2)
        ctk.CTkLabel(self.content, text="Completed At", width=140).grid(row=1, column=5, padx=2)

        # ListView (row 2)
        self.request_list = ctk.CTkScrollableFrame(self.content)
        self.request_list.grid(row=2, column=0, columnspan=7, sticky="nsew")

    def _build_submit_form(self, tab):
        tab.grid_columnconfigure(0, minsize=44)   # ID spacer      (40 + 2+2)
        tab.grid_columnconfigure(2, minsize=104)  # Submitter spacer (100 + 2+2)
        tab.grid_columnconfigure(3, minsize=144)  # Submitted At spacer (140 + 2+2)
        tab.grid_columnconfigure(4, minsize=144)  # Processing At spacer (140 + 2+2)
        tab.grid_columnconfigure(6, weight=1)

        self.submit_room_id_entry = ctk.CTkEntry(tab, width=60, placeholder_text="Room ID")
        self.submit_room_id_entry.grid(row=0, column=1, padx=2, pady=5)

        self.submit_description_entry = ctk.CTkEntry(tab, placeholder_text="Description")
        self.submit_description_entry.grid(
            row=0, column=2, columnspan=3, padx=2, pady=5, sticky="ew"
        )

        ctk.CTkButton(tab, text="Submit", command=self._on_submit, width=80).grid(
            row=0, column=5, padx=2, pady=5
        )

    def _build_process_form(self, tab):
        tab.grid_columnconfigure(1, minsize=64)   # Room spacer      (60  + 2+2)
        tab.grid_columnconfigure(2, minsize=104)  # Submitter spacer (100 + 2+2)
        tab.grid_columnconfigure(3, minsize=144)  # Submitted At spacer (140 + 2+2)
        tab.grid_columnconfigure(4, minsize=144)  # Processing At spacer (140 + 2+2)
        tab.grid_columnconfigure(6, weight=1)

        self.process_id_entry = ctk.CTkEntry(tab, width=40, placeholder_text="ID")
        self.process_id_entry.grid(row=0, column=0, padx=2, pady=5)

        ctk.CTkButton(tab, text="Process", command=self._on_process, width=80).grid(
            row=0, column=5, padx=2, pady=5
        )

    def _build_complete_form(self, tab):
        tab.grid_columnconfigure(1, minsize=64)   # Room spacer
        tab.grid_columnconfigure(2, minsize=104)  # Submitter spacer
        tab.grid_columnconfigure(3, minsize=144)  # Submitted At spacer
        tab.grid_columnconfigure(4, minsize=144)  # Processing At spacer
        tab.grid_columnconfigure(6, weight=1)

        self.complete_id_entry = ctk.CTkEntry(tab, width=40, placeholder_text="ID")
        self.complete_id_entry.grid(row=0, column=0, padx=2, pady=5)

        ctk.CTkButton(tab, text="Complete", command=self._on_complete, width=80).grid(
            row=0, column=5, padx=2, pady=5
        )

    def _on_submit(self):
        try:
            _room_id = int(self.submit_room_id_entry.get())
            _description = self.submit_description_entry.get()
        except Exception:
            messagebox.showerror("Error", "Room ID should be a number.")
            return
        try:
            submit_request(_room_id, _description, self.current_user)
            self.submit_room_id_entry.delete(0, "end")
            self.submit_description_entry.delete(0, "end")
            self._refresh_list()
        except Exception as e:
            messagebox.showerror("Error", e)

    def _on_process(self):
        try:
            _id = int(self.process_id_entry.get())
        except Exception:
            messagebox.showerror("Error", "Request ID should be a number.")
            return
        try:
            process_request(_id)
            self.process_id_entry.delete(0, "end")
            self._refresh_list()
        except Exception as e:
            messagebox.showerror("Error", e)

    def _on_complete(self):
        try:
            _id = int(self.complete_id_entry.get())
        except Exception:
            messagebox.showerror("Error", "Request ID should be a number.")
            return
        try:
            complete_request(_id)
            self.complete_id_entry.delete(0, "end")
            self._refresh_list()
        except Exception as e:
            messagebox.showerror("Error", e)

    def _on_search(self):
        try:
            _status = self.search_status_option.get()
            _status = None if _status == "all" else _status

            if self.is_admin:
                _username = self.search_username_entry.get() or None
                _room_id = self.search_room_id_entry.get()
                _room_id = int(_room_id) if _room_id else None
            else:
                _username = self.current_username
                _room_id = None
        except Exception:
            messagebox.showerror("Error", "Room ID should be a number.")
            return
        try:
            self.show_requests(
                get_requests(status=_status, username=_username, room_id=_room_id)
            )
        except Exception as e:
            messagebox.showerror("Error", e)

    def _refresh_list(self):
        if self.is_admin:
            self.show_requests(get_requests())
        else:
            self.show_requests(get_requests(username=self.current_username))

    def _resumed(self):
        self.current_user = self.winfo_toplevel().context.current_user
        self.current_username = self.current_user.username
        self.is_admin = self.current_user.role == "admin"

        if self.is_admin:
            self.admin_tab_container.pack(
                fill="x", padx=10, pady=(5, 0), before=self.content
            )
            self.search_room_id_entry.grid()
            self.search_username_entry.grid()
        else:
            self.admin_tab_container.pack_forget()
            self.search_room_id_entry.grid_remove()
            self.search_username_entry.grid_remove()

        self._refresh_list()

    def show_requests(self, requests: list[RequestMaintenanceRead]):
        for widget in self.request_list.winfo_children():
            widget.destroy()
        for request in requests:
            MaintenanceItem(self.request_list, request).pack(fill="x", pady=2)


class MaintenanceItem(ctk.CTkFrame):
    def __init__(self, parent, request: RequestMaintenanceRead, **kwargs):
        super().__init__(parent, **kwargs)

        hbox = ctk.CTkFrame(self)
        hbox.pack(fill="x")

        ctk.CTkLabel(hbox, text=str(request.id), width=40).grid(row=0, column=0, padx=2)
        ctk.CTkLabel(hbox, text=str(request.room_id), width=60).grid(row=0, column=1, padx=2)
        ctk.CTkLabel(hbox, text=request.username, width=100).grid(row=0, column=2, padx=2)
        ctk.CTkLabel(hbox, text=request.created_at, width=140).grid(row=0, column=3, padx=2)
        ctk.CTkLabel(hbox, text=request.processing_at or "-", width=140).grid(
            row=0, column=4, padx=2
        )
        ctk.CTkLabel(hbox, text=request.completed_at or "-", width=140).grid(
            row=0, column=5, padx=2
        )

        ctk.CTkLabel(self, text=request.description, anchor="w").pack(fill="x", padx=5)
