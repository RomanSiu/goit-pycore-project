from datetime import datetime as dtdt

from utils import input_error
from models import Name, Phone, Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p.value) for p in self.phones)}"

    @input_error
    def add_phone(self, phone):
        phone = Phone(phone)
        if phone.value is None:
            return "Please enter a valid phone number.", "warning"
        elif phone.value not in [i.value for i in self.phones]:
            self.phones.append(phone)
            return "Phone added.", "success"
        else:
            return "Phone already exists.", "warning"

    @input_error
    def remove_phone(self, phone_rm):
        for phone in self.phones:
            if phone_rm == phone.value:
                self.phones.remove(phone)
                return f"Phone {phone_rm} removed.", "success"

        return "No such phone exists.", "warning"

    @input_error
    def edit_phone(self, old_phone, new_phone):
        new_phone = Phone(new_phone)

        if new_phone.value is None:
            return "Please enter a valid phone number.", "warning"

        for phone in self.phones:
            if old_phone == phone.value and new_phone.value:
                phone.value = new_phone.value
                return f"Phone {old_phone} changed to {new_phone}.", "success"

        return "No such phone exists.", "warning"

    @input_error
    def find_phone(self, phone_to_find):
        for phone in self.phones:
            if phone_to_find == phone.value:
                return phone

    @input_error
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        if self.birthday.value is None:
            return "Invalid date format. Try DD.MM.YYYY.", "warning"
        return "Birthday added.", "success"

    @input_error
    def show_birthday(self):
        if self.birthday is None:
            return "No birthday found.", "warning"
        return f"{self.name.value.capitalize()}'s birthday: {dtdt.strftime(self.birthday.value, '%d.%m.%Y')}"
