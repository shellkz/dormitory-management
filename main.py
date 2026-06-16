import customtkinter as ctk

from views import LoginFrame, MainFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setting
        self.title("Dormitory Management System")
        self.geometry("800x450")

        # Register all frames(menus)
        self.frames = {}

        def on_login_success(username, password):
            self.goto("main", username=username)

        self.frames["login"] = LoginFrame(self, on_login_success=on_login_success)

        self.frames["main"] = MainFrame(self)

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
