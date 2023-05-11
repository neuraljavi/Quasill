import uuid
from diagnosticator.predictions import predict, get_feedback


def new_diagnostic(user_id, text):
    prediction = predict(text)
    diagnostic = Diagnostic(user_id, text, predictions=prediction)
    return diagnostic


class Diagnostic:
    def __init__(self, user_id, text="", predictions={}):
        self.text = text
        self.predictions = predictions
        self.user_id = user_id
        self.real_disease = None

    def return_diseases(self):
        return self.predictions

    def to_dict(self):
        return {
            'text': self.text,
            'predictions': self.predictions,
            'user_id': self.user_id,
            'real_disease': self.real_disease
        }


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

    def delete_diagnostic(self, diagnostic_id):
        for diagnostic in self.diagnostics:
            if diagnostic.id == diagnostic_id:
                self.diagnostics.remove(diagnostic)
                return True
        return False

    def feedback_of_diagnostic(self, diagnostic_id, real_disease):
        for diagnostic in self.diagnostics:
            if diagnostic.id == diagnostic_id:
                diagnostic.real_disease = real_disease
                return True
        return False

    def get_diagnostic(self, diagnostic_id):
        for diagnostic in self.diagnostics:
            if diagnostic.id == diagnostic_id:
                return diagnostic
        return None

    def get_diagnostics(self):
        return self.diagnostics

    def diagnosticate(self, text):
        diagnostic = new_diagnostic(self.id, text)
        self.diagnostics.append(diagnostic)
        return diagnostic

    def proportionate_feedback(self, diagnostic_id, text, correct_label):
        diagnostic = self.get_diagnostic(diagnostic_id)
        if diagnostic is None:
            return False
        feedback = get_feedback(text, correct_label)
        if feedback is None:
            return False
        diagnostic.real_disease = correct_label
        return True


