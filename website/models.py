import uuid


class Diagnostic:
    def __init__(self, user_id, diagnostic_id=None, text="", predictions={}):
        self.id = diagnostic_id
        self.text = text
        self.predictions = predictions
        self.user_id = user_id

    def return_diseases(self):
        return self.predictions

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'predictions': self.predictions,
            'user_id': self.user_id
        }

    def add_prediction(self, disease, probability):
        self.predictions[disease] = probability


class User:
    def __init__(self, name, surname, username, email, surname2=None, user_id=None):
        self.id = user_id
        self.name = name
        self.surname = surname
        self.surname2 = surname2
        self.username = username
        self.diagnostics = []
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'surname2': self.surname2,
            'username': self.username,
            'email': self.email,
            'diagnostics': self.diagnostics
        }

    def add_diagnostic(self, diagnostic: Diagnostic):
        self.diagnostics.append(diagnostic)
