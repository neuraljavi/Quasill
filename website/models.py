import uuid


class User:
    def __init__(self, name, surname, username, email, surname2=None, user_id=None):
        self.id = user_id
        self.name = name
        self.surname = surname
        self.surname2 = surname2
        self.username = username
        self.diagnostics = []
        self.email = email
