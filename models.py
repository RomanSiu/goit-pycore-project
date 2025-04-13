import re
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
            return "⚠️ Please enter a valid contact name.", "warning"


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


class Title(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validated_title(value)

    @input_error
    def validated_title(self, title):
        if type(title) is str and len(title) < 15:
            self.value = title
        else:
            self.value = None


class NoteText(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validated_notetext(value)
    
    @input_error
    def validated_notetext(self, text):
        if text is not None and text.strip().strip('"') != "":
            self.value = text
        else:
            self.value = None

                      
class Address(Field):
    def __init__(self, value):
        self.value = None
        self.validate(value)

    @input_error
    def validate(self, address):
        if not address.isspace() and len(address) >= 3:
            self.value = address

            
class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)
    
    @input_error
    def validate(self, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(email_pattern, email):
            self.value = email.lower()
        else:
            self.value = None
            return "Please enter a valid email address (e.g. example@mail.com).", "warning"

    def update(self, new_email):
        self.validate(new_email)

    def delete(self):
        self.value = None
