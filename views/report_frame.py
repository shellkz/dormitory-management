import customtkinter as ctk

from features.assign import get_stays
from features.room import get_rooms


class ReportFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Access denied view (resident)
        self.denied_label = ctk.CTkLabel(
            self, text="Access denied. Admin only page.", anchor="center"
        )

        # Report view (admin)
        self.report_container = ctk.CTkFrame(self)

        self.total_label = ctk.CTkLabel(self.report_container, text="", anchor="w")
        self.total_label.pack(pady=5)

        self.occupied_label = ctk.CTkLabel(self.report_container, text="", anchor="w")
        self.occupied_label.pack(pady=5)

        self.available_label = ctk.CTkLabel(self.report_container, text="", anchor="w")
        self.available_label.pack(pady=5)

        self.occupancy_bar = ctk.CTkProgressBar(self.report_container, width=300)
        self.occupancy_bar.pack(pady=5)

        self.rate_label = ctk.CTkLabel(self.report_container, text="", anchor="w")
        self.rate_label.pack(pady=5)

    def _resumed(self):
        role = self.winfo_toplevel().context.current_user.role

        if role != "admin":
            self.report_container.place_forget()
            self.denied_label.place(relx=0.5, rely=0.5, anchor="center")
            return

        self.denied_label.place_forget()
        self.report_container.place(relx=0.5, rely=0.5, anchor="center")
        self._load_report()

    def _load_report(self):
        total = len(get_rooms())
        occupied = len(get_stays(active_only=True))
        available = total - occupied
        rate = occupied / total if total > 0 else 0

        self.total_label.configure(text=f"總房間數：{total} 間")
        self.occupied_label.configure(text=f"已入住：{occupied} 間")
        self.available_label.configure(text=f"空房：{available} 間")
        self.occupancy_bar.set(rate)
        self.rate_label.configure(text=f"{rate * 100:.1f}%")
