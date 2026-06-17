import customtkinter as ctk

from state import AppState
from views import AuthFrame, MainFrame, RoomFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.context: AppState = AppState()

        # Window Setting
        self.title("Dormitory Management System")
        self.geometry("800x450")

        # Register all frames(menus)
        self.frames = {}

        self.frames["auth"] = AuthFrame(self)
        self.frames["main"] = MainFrame(self)
        self.frames["room"] = RoomFrame(self)
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Initial frame
        self.goto("auth")

    def goto(self, name, **kwargs):
        frame = self.frames[name]
        if hasattr(frame, "_resumed"):
            frame._resumed(**kwargs)
        frame.tkraise()


app = App()
app.mainloop()
