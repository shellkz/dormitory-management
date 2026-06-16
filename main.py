import customtkinter as ctk

from views import LoginFrame, MainFrame


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("宿舍管理系統")
        self.geometry("400x300")
        self.show_login()

    def show_login(self):
        LoginFrame(self, on_login_success=self.show_main).pack(fill="both", expand=True)

    def show_main(self, user):
        for widget in self.winfo_children():
            widget.destroy()
        MainFrame(self, user=user).pack(fill="both", expand=True)


app = App()
app.mainloop()
