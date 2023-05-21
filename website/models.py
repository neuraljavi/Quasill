import uuid
from diagnosticator import predict, get_feedback


# MODELOS CREADOS POR JAVIER

# FUNCIÓN PARA LA CREACIÓN DE UN DIAGNÓSTICO
def new_diagnostic(user_id, text):
    prediction = predict(text)
    diagnostic = Diagnostic(user_id, text, predictions=prediction)
    return diagnostic


class Diagnostic:
    def __init__(self, user_id, text="", predictions={}, real_disease=None):
        self.text = text
        self.predictions = predictions
        self.user_id = user_id
        # PARA QUE DIAGNOSTIC PUEDA MANEJAR real_disease COMO UN ARGUMENTO DE ENTRADA
        self.real_disease = real_disease

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
        self.diagnostics = [] if 'diagnostics' not in kwargs else kwargs['diagnostics']
        self.email = email
        self.password = None if 'password' not in kwargs else kwargs['password']

    # ACEPTA LOS DATOS DEL USUARIO Y LOS CONVIERTE EN UN USUARIO
    @classmethod
    def from_dict(cls, data):
        diagnostics = [Diagnostic(**diagnostic_data) for diagnostic_data in data.get('diagnostics', [])] if data.get(
            'diagnostics') else []
        return cls(
            name=data['name'],
            surname=data['surname'],
            username=data['username'],
            email=data['email'],
            surname2=data.get('surname2'),
            diagnostics=diagnostics,
            id=data.get('id'),
            password=data.get('password')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'surname2': self.surname2,
            'username': self.username,
            # dict indexado
            'diagnostics': [diagnostic.to_dict() for diagnostic in self.diagnostics] if self.diagnostics else None,
            'email': self.email,
            'password': self.password
        }

    def add_diagnostic(self, diagnostic: Diagnostic):
        if self.diagnostics is None:
            self.diagnostics = []
        self.diagnostics.append(diagnostic)

    def delete_diagnostic(self, diagnostic_index):
        diagnostic_index = int(diagnostic_index)
        try:
            self.diagnostics.pop(diagnostic_index)
            print("delete_diagnostic borra el diagnóstico")
            return True
        except IndexError:
            print("delete_diagnostic no borra el diagnóstico")
            return False

    def get_diagnostic(self, diagnostic_id):
        return self.diagnostics[diagnostic_id]

    def get_diagnostics(self):
        return self.diagnostics

    # FUNCIÓN QUE DEVUELVE UN DIAGNÓSTICO
    def diagnosticate(self, text):
        if len(self.diagnostics) >= 20:
            self.diagnostics.pop(0)

        diagnostic = new_diagnostic(self.id, text)
        self.diagnostics.append(diagnostic)
        return diagnostic

    def proportionate_feedback(self, diagnostic_id, correct_label):
        diagnostic = self.get_diagnostic(diagnostic_id)
        if diagnostic is None:
            return False
        text = diagnostic.text
        feedback = get_feedback(text, correct_label)
        if feedback is None:
            return False
        diagnostic.real_disease = correct_label
        return True

    def get_last_diagnostic(self):
        return self.diagnostics[-1]
