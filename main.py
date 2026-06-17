import customtkinter as ctk

from db import User
from state import AppState
from views import AuthFrame, MainFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.context: AppState = AppState()

        # Window Setting
        self.title("Dormitory Management System")
        self.geometry("800x450")

        # Register all frames(menus)
        self.frames = {}

        def on_login_success(user: User):
            self.context.current_user = user
            self.goto("main")

        self.frames["login"] = AuthFrame(
            self, context=self.context, on_login_success=on_login_success
        )

        self.frames["main"] = MainFrame(self, context=self.context)

        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Initial frame
        self.goto("login")

    def goto(self, name, **kwargs):
        frame = self.frames[name]
        if hasattr(frame, "_resumed"):
            frame._resumed(**kwargs)
        frame.tkraise()


app = App()
app.mainloop()
