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
        self.current_username = None

        # Admin-only: Process & Complete tabs (not packed until _resumed)
        self.admin_action_tabs = ctk.CTkTabview(self)

        process_tab = self.admin_action_tabs.add("Process")
        process_row = ctk.CTkFrame(process_tab)
        process_row.pack()
        self.process_id_entry = ctk.CTkEntry(process_row, placeholder_text="Request ID")
        self.process_id_entry.pack(side="left", padx=5)
        ctk.CTkButton(process_row, text="Process", command=self._on_process).pack(
            side="left", padx=5
        )

        complete_tab = self.admin_action_tabs.add("Complete")
        complete_row = ctk.CTkFrame(complete_tab)
        complete_row.pack()
        self.complete_id_entry = ctk.CTkEntry(
            complete_row, placeholder_text="Request ID"
        )
        self.complete_id_entry.pack(side="left", padx=5)
        ctk.CTkButton(complete_row, text="Complete", command=self._on_complete).pack(
            side="left", padx=5
        )

        # Submit form (all users)
        self.submit_form = ctk.CTkFrame(self)
        self.submit_form.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(self.submit_form, text="Submit Maintenance Request").pack(
            anchor="w", padx=5
        )
        submit_row = ctk.CTkFrame(self.submit_form)
        submit_row.pack()
        self.submit_room_id_entry = ctk.CTkEntry(submit_row, placeholder_text="Room ID")
        self.submit_room_id_entry.pack(side="left", padx=5)
        self.submit_description_entry = ctk.CTkEntry(
            submit_row, placeholder_text="Description", width=200
        )
        self.submit_description_entry.pack(side="left", padx=5)
        ctk.CTkButton(submit_row, text="Submit", command=self._on_submit).pack(
            side="left", padx=5
        )

        # Search filter
        filter_container = ctk.CTkFrame(self)
        filter_container.pack(fill="x", padx=10, pady=5)

        filter_row = ctk.CTkFrame(filter_container)
        filter_row.pack()
        self.search_status_option = ctk.CTkOptionMenu(
            filter_row, values=["all", "submitted", "processing", "completed"]
        )
        self.search_status_option.pack(side="left", padx=5)
        ctk.CTkButton(filter_row, text="Search", command=self._on_search).pack(
            side="left", padx=5
        )

        # Admin-only filter fields (not packed until _resumed)
        self.admin_filter_container = ctk.CTkFrame(filter_container)
        admin_filter_row = ctk.CTkFrame(self.admin_filter_container)
        admin_filter_row.pack()
        self.search_username_entry = ctk.CTkEntry(
            admin_filter_row, placeholder_text="Username"
        )
        self.search_username_entry.pack(side="left", padx=5)
        self.search_room_id_entry = ctk.CTkEntry(
            admin_filter_row, placeholder_text="Room ID"
        )
        self.search_room_id_entry.pack(side="left", padx=5)

        # List header
        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=10)
        ctk.CTkLabel(header, text="ID", width=40).pack(side="left")
        ctk.CTkLabel(header, text="Room", width=60).pack(side="left")
        ctk.CTkLabel(header, text="Submitter", width=100).pack(side="left")
        ctk.CTkLabel(header, text="Submitted At", width=140).pack(side="left")
        ctk.CTkLabel(header, text="Processing At", width=140).pack(side="left")
        ctk.CTkLabel(header, text="Completed At", width=140).pack(side="left")

        self.request_list = ctk.CTkScrollableFrame(self)
        self.request_list.pack(fill="both", expand=True, padx=10, pady=5)

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

    def _on_submit(self):
        try:
            _room_id = int(self.submit_room_id_entry.get())
            _description = self.submit_description_entry.get()
        except Exception:
            messagebox.showerror("Error", "Room ID should be a number.")
            return
        try:
            _created_by = self.winfo_toplevel().context.current_user.id
            submit_request(_room_id, _description, self.current_user)
            self.submit_room_id_entry.delete(0, "end")
            self.submit_description_entry.delete(0, "end")
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
        role = self.winfo_toplevel().context.current_user.role
        self.current_username = self.winfo_toplevel().context.current_user.username
        self.is_admin = role == "admin"

        if self.is_admin:
            self.admin_action_tabs.pack(
                fill="x", padx=10, pady=5, before=self.submit_form
            )
            self.admin_filter_container.pack()
        else:
            self.admin_action_tabs.pack_forget()
            self.admin_filter_container.pack_forget()

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

        ctk.CTkLabel(hbox, text=str(request.id), width=40).pack(side="left")
        ctk.CTkLabel(hbox, text=str(request.room_id), width=60).pack(side="left")
        ctk.CTkLabel(hbox, text=request.username, width=100).pack(side="left")
        ctk.CTkLabel(hbox, text=request.created_at, width=140).pack(side="left")
        ctk.CTkLabel(hbox, text=request.processing_at or "-", width=140).pack(
            side="left"
        )
        ctk.CTkLabel(hbox, text=request.completed_at or "-", width=140).pack(
            side="left"
        )

        ctk.CTkLabel(self, text=request.description, anchor="w").pack(fill="x", padx=5)
