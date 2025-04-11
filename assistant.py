import pickle
import os
import shlex

from colorama import Fore, Style

from utils import input_error
from models import Name, Phone, Birthday, Address, Email, NoteText, Title
from record import AddressBook, Record, NoteBook, Note
from ui_helpers import user_input, user_output, extend_contact_interactive
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
def add_contact(args: list, book: AddressBook) -> tuple:
    """
    Add a contact to the book.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Message.
    """
    name, phone, *_ = args
    record = book.find(name)
    if type(record) is tuple:
        record = Record(name)
        message = record.add_phone(phone)
        book.add_record(record)
        extend_contact_interactive(record, book)
    else:
        message = record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook) -> tuple:
    """
    Change phone number to the contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Message.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.edit_phone(old_phone, new_phone)
        return message
    else:
        return record


@input_error
def show_phone(args: list, book: AddressBook) -> tuple:
    """
    Return list of phone numbers for a contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Tuple with list of phones or with message.
    """
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        phones = [i.value for i in record.phones]
        return phones, "common list"
    else:
        return record


@input_error
def show_all(book: AddressBook) -> tuple:
    """
    Return list of all contacts.

    Args:
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Tuple with list of contacts or with message.
    """
    rows = []
    for rec in book.values():
        name = rec.name.value.capitalize()
        phones = "; ".join(p.value for p in rec.phones)
        birthday = rec.birthday.value.strftime('%d.%m.%Y') if rec.birthday else "-"
        email = rec.email.value if rec.email else "-"
        address = rec.address.value if rec.address else "-"
        rows.append([name, phones, birthday, email, address])
    return rows, "table"


@input_error
def add_birthday(args: list, book: AddressBook) -> tuple:
    """
    Add birthday to contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Message.
    """
    name, birthday, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.add_birthday(birthday)
        return message
    else:
        return record


@input_error
def show_birthday(args: list, book: AddressBook) -> tuple:
    """
    Show birthday of a contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Tuple with contacts birthday or with message.
    """
    name, *_ = args
    record = book.find(name)
    if type(record) is not tuple:
        message = record.show_birthday()
        return message if type(message) is tuple else (message, "common")
    else:
        return record

@input_error
def birthdays_table(book: AddressBook, days: int = 7) -> tuple:
    data, _ = book.get_upcoming_birthdays(days)

    if len(data) <= 1:
        return f"No birthdays in the next {days} days.", "warning"

    rows = []
    for line in data[1:]:  # пропускаємо заголовок
        try:
            name, bday = line.split(": ")
            rows.append([name.strip(), bday.strip()])
        except ValueError:
            continue

    return rows, "birthdays"

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

  
@input_error
def address(args: list, book: AddressBook, func: str) -> tuple:
    """
    Call func to interact with an address of a contact.

    Args:
        args (list): Argument list from command line.
        book (AddressBook): Address book to save records.
        func (str): Function to call to interact with an address.

    Returns:
        tuple: Tuple with address or with message.
    """
    record = book.find(args[0])
    if type(record) is not tuple:
        address_func = getattr(record, func)
        return address_func(*args[1:])
    else:
        return record
    

@input_error
def add_email(args, book):
    name, email = args
    record = book.find(name)
    if record:
        return record.add_email(email)
    return "Contact not found.", "warning"


@input_error
def edit_email(args, book):
    name, new_email = args
    record = book.find(name)
    if record:
        return record.edit_email(new_email)
    return "Contact not found.", "warning"


@input_error
def show_email(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.show_email()
    return "Contact not found.", "warning"


@input_error
def delete_email(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        return record.delete_email()
    return "Contact not found.", "warning"


# Серіалізація даних в окремий файл з обох книг
def save_data(books, filename="data/addressbook_and_notebook.pkl"):
    # створює директорію, якщо вона не існує
    os.makedirs(os.path.dirname(filename), exist_ok=True)
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
    user_output("Welcome to the assistant bot!")
    while True:
        command = shlex.split(input("Write a command: "))
        command[0] = command[0].lower()


        match command[0]:
            case 'exit' | 'close':
                user_output("Good bye!")
                break
            case 'hello':
                user_output("How can I help you?")
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
            case 'add-email':
                output(*add_email(command[1:], addressbook))
            case 'change-email':
                output(*edit_email(command[1:], addressbook))
            case 'show-email':
                output(*show_email(command[1:], addressbook))
            case 'delete-email':
                output(*delete_email(command[1:], addressbook))
            case 'add-birthday':
                output(*add_birthday(command[1:], addressbook))
            case 'show-birthday':
                output(*show_birthday(command[1:], addressbook))
            case 'birthdays':
                try:
                    days = int(command[1])
                except IndexError:
                    days = 7
                show_table(*birthdays_table(addressbook, days))
            case 'add-note':
                output(*add_note(command[1:], notebook))
            case 'find-note':
                output(*find_note(command[1], notebook))
            case 'all':
                show_table(*show_all(addressbook))
            case _:
                output("Invalid command.", "error")
    save_data((addressbook, notebook))


if __name__ == '__main__':
    main()
