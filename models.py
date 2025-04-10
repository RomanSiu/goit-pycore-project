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


class Address(Field):
    def __init__(self, value):
        self.value = None
        self.validate(value)

    @input_error
    def validate(self, address):
        if address.isalpha():
            self.value = address
        else:
            self.value = None

# email
class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    @input_error
    def validate(self, email):
        if "@" in email and email.replace("@", "").replace(".", "").isalnum() and email.isascii():
            self.value = email.lower()
        else:
            self.value = None
            return "Please enter a valid email address (only Latin letters and must include @).", "warning"

    def update(self, new_email):
        self.validate(new_email)

    def delete(self):
        self.value = None
