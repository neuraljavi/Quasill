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
    def __init__(self, name, surname, username, email, surname2=None, **kwargs):
        self.id = None if 'id' not in kwargs else kwargs['id']
        self.name = name
        self.surname = surname
        self.surname2 = surname2
        self.username = username
        self.diagnostics = None if 'diagnostics' not in kwargs else kwargs['diagnostics']
        self.email = email
        self.password = None if 'password' not in kwargs else kwargs['password']

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'surname2': self.surname2,
            'username': self.username,
            'diagnostics': self.diagnostics,
            'email': self.email,
            'password': self.password
        }

    def add_diagnostic(self, diagnostic: Diagnostic):
        self.diagnostics.append(diagnostic)
