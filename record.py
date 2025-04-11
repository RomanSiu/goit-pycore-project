from datetime import datetime as dtdt
from datetime import timedelta
from collections import UserDict

from utils import input_error
from models import Name, Phone, Birthday, Address, Email, NoteText, Title


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None

    def __str__(self):
        birthday_str = ""
        address_str = ""
        if self.birthday:
            birthday_str = f"birthday: {self.birthday.strftime('%d.%m.%Y')}"
        if self.address:
            address_str = f"address: {self.address}"
        return (f"Contact name: {self.name.value}, phones: {'; '.join(str(p.value) for p in self.phones)}"
                + birthday_str + address_str)

    @input_error
    def add_phone(self, phone: str) -> tuple:
        """
        Add a phone to the record

        Args:
            phone (str): phone number

        Returns:
            tuple: message
        """
        phone = Phone(phone)
        if phone.value is None:
            return "Please enter a valid phone number.", "warning"
        elif phone.value not in [i.value for i in self.phones]:
            self.phones.append(phone)
            return "Phone added.", "success"
        else:
            return "Phone already exists.", "warning"

    @input_error
    def remove_phone(self, phone_rm: str) -> tuple:
        """
        Remove a phone from the record

        Args:
            phone_rm (str): phone number to remove

        Returns:
            tuple: message
        """
        for phone in self.phones:
            if phone_rm == phone.value:
                self.phones.remove(phone)
                return f"Phone {phone_rm} removed.", "success"

        return "No such phone exists.", "warning"

    @input_error
    def edit_phone(self, old_phone: str, new_phone: str) -> tuple:
        """
        Edit a phone in the record

        Args:
            old_phone (str): phone number to edit
            new_phone (str): new phone number

        Returns:
            tuple: message
        """
        new_phone = Phone(new_phone)

        if new_phone.value is None:
            return "Please enter a valid phone number.", "warning"

        for phone in self.phones:
            if old_phone == phone.value and new_phone.value:
                phone.value = new_phone.value
                return f"Phone {old_phone} changed to {new_phone}.", "success"

        return "No such phone exists.", "warning"

    @input_error
    def find_phone(self, phone_to_find: str) -> tuple:
        """
        Find a phone in the record

        Args:
             phone_to_find (str): phone number to find

        Returns:
            tuple: message
        """
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

    @input_error
    def add_address(self, address: str, *args) -> tuple:
        address = Address(address)
        if address.value is None:
            return "Please enter a valid address.", "warning"
        else:
            self.address = address
            return "Address added.", "success"

    @input_error
    def show_address(self, *args) -> tuple:
        if self.address is None:
            return "No address found.", "warning"
        return self.address.value, "common"

    @input_error
    def edit_address(self, address: str, *args) -> tuple:
        address = Address(address)
        if self.address is None:
            return "No address found.", "warning"
        elif address.value is None:
            return "Please enter a valid address.", "warning"
        else:
            self.address = address
            return "Address changed.", "success"

    @input_error
    def delete_address(self, *args) -> tuple:
        self.address = None
        return "Address deleted.", "success"
    

class Note:
    def __init__(self, title, text):
        self.title = Title(title)
        self.text = NoteText(text)
        self.created_date = dtdt.now().replace(microsecond=0)
        self.updated_date = dtdt.now().replace(microsecond=0)
    
    def __str__(self):
        return (f"Title: {self.title.value}\n"
                f"Content: {self.text.value}\n"
                f"Created: {self.created_date}\n"
                f"Updated: {self.updated_date}\n")


class NoteBook:
    def __init__(self):
        super().__init__()
        self.notes = []

    @input_error
    def add_note(self, note):
        if note.text.value is None:
            return "Note cannot be empty.", "warning"
        elif note.title.value is None:
            return "Title must be 15 characters or less.", "warning"
        self.notes.append(note)
        return "Note added.", "success"
    
    @input_error
    def find_note(self, title):
        for note in self.notes:
            if note.title.value.lower() == title.lower():
                return note
    
    @input_error
    def delete_note(self, title):
        for note in self.notes:
            if note.title.value.lower() == title.lower():
                self.notes.remove(note)
                return "Note deleted.", "success"

    @input_error
    def add_address(self, address: str, *args) -> tuple:
        address = Address(address)
        if address.value is None:
            return "Please enter a valid address.", "warning"
        else:
            self.address = address
            return "Address added.", "success"

    @input_error
    def show_address(self, *args) -> tuple:
        if self.address is None:
            return "No address found.", "warning"
        return self.address.value, "common"

    @input_error
    def edit_address(self, address: str, *args) -> tuple:
        address = Address(address)
        if self.address is None:
            return "No address found.", "warning"
        elif address.value is None:
            return "Please enter a valid address.", "warning"
        else:
            self.address = address
            return "Address changed.", "success"

    @input_error
    def delete_address(self, *args) -> tuple:
        self.address = None
        return "Address deleted.", "success"


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
    def get_upcoming_birthdays(self, days: int = 7) -> (list, str):
        today = dtdt.now().date()
        d7 = today + timedelta(days=days)
        lst = [f"Next {days} days You need to congratulate:"]
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
