import pickle
import os

from colorama import Fore, Style

from utils import input_error
from models import Name, Phone, Birthday
from record import AddressBook, Record
from ui_helpers import user_input, user_output
from tableview import show_table


def output(message: str, mtype: str):
    if mtype == 'success':
        user_output(Fore.GREEN + message + Style.RESET_ALL)
    elif mtype == 'warning':
        user_output(Fore.YELLOW + message + Style.RESET_ALL)
    elif mtype == 'error':
        user_output(Fore.RED + message + Style.RESET_ALL)
    elif mtype == 'common list':
        for m in message:
            user_output(Fore.BLUE + m + Style.RESET_ALL)
    elif mtype == 'common':
        user_output(Fore.BLUE + message + Style.RESET_ALL)
    else:
        user_output(message)


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    if type(record) is tuple:
        record = Record(name)
        message = record.add_phone(phone)
        book.add_record(record)
    else:
        message = record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.edit_phone(old_phone, new_phone)
        return message
    else:
        return record


@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        phones = [i.value for i in record.phones]
        return phones, "common list"
    else:
        return record


@input_error
def show_all(book):
    rows = []
    for rec in book.values():
        name = rec.name.value.capitalize()
        phones = "; ".join(p.value for p in rec.phones)
        birthday = rec.birthday.value.strftime('%d.%m.%Y') if rec.birthday else "-"
        # ❗ Тепер повертаємо список з трьох колонок
        rows.append([name, phones, birthday])
    return rows, "table"


@input_error
def add_birthday(args, book):
    name, birthday, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.add_birthday(birthday)
        return message
    else:
        return record


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.show_birthday()
        return message if type(message) is tuple else (message, "common")
    else:
        return record


def save_data(book, filename="data/addressbook.pkl"):
    # створює директорію, якщо вона не існує
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # зберігає файл
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="data/addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def main():
    book = load_data()
    user_output("Welcome to the assistant bot!")
    while True:
        command = user_input("Write a command: ")
        command = command.lower().split(' ')

        match command[0]:
            case 'exit' | 'close':
                user_output("Good bye!")
                break
            case 'hello':
                user_output("How can I help you?")
            case 'add':
                output(*add_contact(command[1:], book))
            case 'change':
                output(*change_contact(command[1:], book))
            case 'phone':
                output(*show_phone(command[1:], book))
            case 'add-birthday':
                output(*add_birthday(command[1:], book))
            case 'show-birthday':
                output(*show_birthday(command[1:], book))
            case 'birthdays':
                try:
                    days = int(command[1])
                except IndexError:
                    days = 7
                output(*book.get_upcoming_birthdays(days))
            case 'all':
                show_table(*show_all(book))
            case _:
                output("Invalid command.", "error")
    save_data(book)


if __name__ == '__main__':
    main()
