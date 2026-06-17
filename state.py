from db import User


class AppState:
    def __init__(self):
        self.current_user: User = None
