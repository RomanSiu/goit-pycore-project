from datetime import datetime as dtdt
from datetime import timedelta
from collections import UserDict

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


class AddressBook(UserDict):
    @input_error
    def add_record(self, record):
        self.data[record.name.value] = record
        return "Record added.", "success"

    @input_error
    def find(self, name):
        return self.data[name.lower()]

    @input_error
    def delete(self, name):
        self.data.pop(name.lower())
        return "Record deleted.", "success"

    @input_error
    def get_upcoming_birthdays(self):
        today = dtdt.now().date()
        d7 = today + timedelta(days=7)
        lst = ["Next week You need to congratulate:"]
        for user in self.data.values():
            if user.birthday is None:
                continue
            bday = user.birthday.value.replace(year=today.year)
            if bday <= today:
                bday = bday.replace(year=today.year + 1)
            if today <= bday <= d7:
                if bday.weekday() == 5:
                    bday = bday + timedelta(days=2)
                if bday.weekday() == 6:
                    bday = bday + timedelta(days=1)
                user_bday = f"{user.name.value.capitalize()}: {dtdt.strftime(bday, '%d.%m.%Y')}"
                lst.append(user_bday)
        return lst, "common list"