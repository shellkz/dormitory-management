import customtkinter as ctk

from state import AppState
from views import (
    AssignFrame,
    AuthFrame,
    MainFrame,
    MaintenanceFrame,
    ReportFrame,
    RoomFrame,
    SideNavigation,
)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.context: AppState = AppState()

        # Window setting
        self.title("Dormitory Management System")
        self.geometry("1280x720")

        # Shared components
        self.side_navigation = SideNavigation(self)

        # Custom frame container
        self.content_panel = ctk.CTkFrame(self)
        self.content_panel.pack(side="left", fill="both", expand=True)

        # Custom frames
        self.frames = {}
        self.frames["auth"] = AuthFrame(self.content_panel)
        self.frames["main"] = MainFrame(self.content_panel)
        self.frames["room"] = RoomFrame(self.content_panel)
        self.frames["assign"] = AssignFrame(self.content_panel)
        self.frames["maintenance"] = MaintenanceFrame(self.content_panel)
        self.frames["report"] = ReportFrame(self.content_panel)

        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.goto("auth")

    def goto(self, name, **kwargs):
        if name == "auth":
            self.side_navigation.pack_forget()
        else:
            self.side_navigation.pack(side="left", fill="y", before=self.content_panel)
            self.side_navigation._resumed(self.context.current_user.role)

        frame = self.frames[name]
        if hasattr(frame, "_resumed"):
            frame._resumed(**kwargs)
        frame.tkraise()


app = App()
app.mainloop()
