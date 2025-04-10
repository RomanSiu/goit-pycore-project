import pickle
import shlex

from colorama import Fore, Style

from utils import input_error
from models import Name, Phone, Birthday, NoteText, Title, Address
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
def add_contact(args, book: AddressBook):
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
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.edit_phone(old_phone, new_phone)
        return message
    else:
        return record


@input_error
def show_phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        phones = [i.value for i in record.phones]
        return phones, "common list"
    else:
        return record


@input_error
def show_all(book: AddressBook):
    phones = []
    for rec in book.values():
        rec_phones = ", ".join([i.value for i in rec.phones])
        phones.append(f"{rec.name.value.capitalize()}: {rec_phones}")
    return phones, "common list"


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.add_birthday(birthday)
        return message
    else:
        return record


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.show_birthday()
        return message if type(message) is tuple else (message, "common")
    else:
        return record



# Створення функції add_note та find_not длф запису та пошуку нотаток за назвою
@input_error
def interactive_add_note(book: NoteBook):
    title = input("Write the title of the note:\n>  ")
    title_obj = Title(title)
    if title_obj.value is None:
        return output("Title must be 15 characters or less.", "warning")
    text = input("Write the text of the note:\n>  ")
    note = book.find_note(title)
    if not isinstance(note, Note):
        note = Note(title, text)
        message = book.add_note(note)
    else:
        message = "Note with this title already exists. Change the title", "warning"
    output(*message)


@input_error
def find_note(args, book: NoteBook):
    title = args[0]
    note = book.find_note(title)
    if isinstance(note, Note):
        message = str(note), "common"
    else:
        message = "Note with this title doesn't exists.", "warning"
    return message

@input_error
def interactive_edit_note(book: NoteBook):
    title = input("Write the title of the note to edit:\n>  ")
    note = book.find_note(title)
    if not note:
        return output("Note with this title doesn't exists.", "warning")
    new_text = input("Write the new text for the note:\n>  ")
    message = book.edit_note(title, new_text)
    return output(*message)

@input_error
def delete_note(args, book: NoteBook):
    title = args[0]
    if not title.strip():
        return "Note title cannot be empty.", "warning"
    message = book.delete_note(title)
    if message is None:
        return "Note not found.", "warning"
    return message

@input_error
def show_all_notes(book):
    notes = book.show_all_notes()
    if not notes:
        return "No notes found.", "warning"
    return notes, "common list"

@input_error
def search_notes(args, book):
    keyword = args[0]
    if not keyword.strip():
        return "Please, enter a keyword.", "warning"
    message = book.search_notes(keyword)
    if not message:
        return "No matches found.", "warning"
    return ["The results of the search:"] + message, "common list"



@input_error
def address(args: list, book: AddressBook, func: str) -> tuple:
    record = book.find(args[0])
    if type(record) is not tuple:
        address_func = getattr(record, func)
        return address_func(*args[1:])
    else:
        return record


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


def main():
    addressbook, notebook = load_data()
    print("Welcome to the assistant bot!")
    while True:
        command = shlex.split(input("Write a command: "))
        command[0] = command[0].lower()

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
            case 'add-address':
                output(*address(command[1:], addressbook, "add_address"))
            case 'show-address':
                output(*address(command[1:], addressbook, "show_address"))
            case 'change-address':
                output(*address(command[1:], addressbook, "edit_address"))
            case 'delete-address':
                output(*address(command[1:], addressbook, "delete_address"))
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
                interactive_add_note(notebook)
            case 'find-note':
                output(*find_note(command[1:], notebook))
            case 'edit-note':
                interactive_edit_note(notebook)
            case 'delete-note':
                output(*delete_note(command[1:], notebook))
            case 'show-all-notes':
                output(*show_all_notes(notebook))
            case 'search-notes':
                output(*search_notes(command[1:], notebook))
            case 'all':
                output(*show_all(addressbook))
            case _:
                output("Invalid command.", "error")
    save_data((addressbook, notebook))


if __name__ == '__main__':
    main()
