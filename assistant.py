import pickle

import shlex

from colorama import Fore, Style

from utils import input_error
from models import Name, Phone, Birthday, NoteText, Title
from record import AddressBook, Record, NoteBook, Note


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


# Створення функції add_note та find_not длф запису та пошуку нотаток за назвою
@input_error
def add_note(args, book):
    title, text = args
    note = book.find_note(title)
    if not isinstance(note, Note):
        note = Note(title, text)
        message = book.add_note(note)
    else:
        message = "Note with this title already exists. Change the title", "warning"
    return message

@input_error
def find_note(title, book):
    note = book.find_note(title)
    if isinstance(note, Note):
        message = str(note), "common"
    else:
        message = "Note with this title doesn't exists.", "warning"
    return message

# Серіалізація даних в окремий файл з обох книг
def save_data(books, filename="data/addressbook_and_notebook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(books, f)


# Завантаження даних з файлу з кортежами обох книг та повернення у разі провало також обох з них
def load_data(filename="data/addressbook_and_notebook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook(), NoteBook()


# В main() я додаю необхідні команди для додавання та пошуку нотаток, 
# виправила command, оскільки при старому варіанті він розділятиме усі слова у нотатці 
# замість прийняття тексту в лапках, як одного з параметрів
def main():
    addressbook, notebook = load_data()
    print("Welcome to the assistant bot!")
    while True:
        command = shlex.split(input("Write a command: "))
        command[0] = command[0].lower()
        # command = command.lower().split(' ')

        match command[0]:
            case 'exit' | 'close':
                print("Good bye!")
                break
            case 'hello':
                print("How can I help you?")
            case 'add':
                output(*add_contact(command[1:], addressbook))
            case 'change':
                output(*change_contact(command[1:], addressbook))
            case 'phone':
                output(*show_phone(command[1:], addressbook))
            case 'add-birthday':
                output(*add_birthday(command[1:], addressbook))
            case 'show-birthday':
                output(*show_birthday(command[1:], addressbook))
            case 'birthdays':
                try:
                    days = int(command[1])
                except IndexError:
                    days = 7
                output(*addressbook.get_upcoming_birthdays(days))
            case 'add-note':
                output(*add_note(command[1:], notebook))
            case 'find-note':
                output(*find_note(command[1], notebook))
            case 'all':
                output(*show_all(addressbook))
            case _:
                output("Invalid command.", "error")
    save_data((addressbook, notebook))


if __name__ == '__main__':
    main()
