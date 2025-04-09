from datetime import datetime as dtdt

from utils import input_error


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    @input_error
    def validate(self, name):
        if name.isalpha():
            self.value = name.lower()
        else:
            self.value = None
            return "Please enter a valid contact name.", "warning"


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    @input_error
    def validate(self, phone):
        if phone.isdigit() and len(phone) == 10:
            self.value = phone
        else:
            self.value = None


class Birthday(Field):
    def __init__(self, value):
        self.value = None
        self.validate_bd(value)

    @input_error
    def validate_bd(self, birthday):
        self.value = dtdt.strptime(birthday, "%d.%m.%Y").date()


# Створила клас Note
class Note:
    def __init__(self, text, title=None):
        self.validate_text(text)
        self.validate_title(title)
        self.created_date = dtdt.now().replace(microsecond=0)
        self.updated_date = dtdt.now().replace(microsecond=0)

# Валідація тексту та назви нотатки, додала лише перевірку основних параметрів при вводі тексту
    def validate_title(self, title):
        if title is not None and type(title) is str:
            if len(title) < 15:
                self.title = title
            else:
                raise ValueError("Title has to have less that 15 symbols")

    def validate_text(self, text):
        if text is None or text.strip().strip('"') == "":
            raise ValueError("Note cannot be empty.")
        self.text = text

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return self.text == other.text and self.title == other.title