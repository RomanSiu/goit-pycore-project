import pickle

from colorama import Fore, Style

from utils import input_error
from models import Name, Phone, Birthday
from record import AddressBook, Record


def output(message: str, mtype: str):
    if mtype == 'success':
        print(Fore.GREEN + message + Style.RESET_ALL)
    elif mtype == 'warning':
        print(Fore.YELLOW + message + Style.RESET_ALL)
    elif mtype == 'error':
        print(Fore.RED + message + Style.RESET_ALL)
    elif mtype == 'common list':
        for m in message:
            print(Fore.BLUE + m + Style.RESET_ALL)
    elif mtype == 'common':
        print(Fore.BLUE + message + Style.RESET_ALL)
    else:
        print(message)


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
    phones = []
    for rec in book.values():

        rec_phones = ", ".join([i.value for i in rec.phones])
        phones.append(f"{rec.name.value.capitalize()}: {rec_phones}")
    return phones, "common list"


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
    print("Welcome to the assistant bot!")
    while True:
        command = input("Write a command: ")
        command = command.lower().split(' ')

        match command[0]:
            case 'exit' | 'close':
                print("Good bye!")
                break
            case 'hello':
                print("How can I help you?")
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
                output(*show_all(book))
            case _:
                output("Invalid command.", "error")
    save_data(book)


if __name__ == '__main__':
    main()
