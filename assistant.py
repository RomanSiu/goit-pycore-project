import pickle
import os
import shlex

from colorama import Fore, Style

from utils import input_error
from models import Name, Phone, Birthday, Address, Email, NoteText, Title
from record import AddressBook, Record, NoteBook, Note
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
def show_all(book: AddressBook) -> tuple:
    """
    Return list of all contacts.

    Args:
        book (AddressBook): Address book to save records.

    Returns:
        tuple: Tuple with list of contacts or with message.
    """
    phones = []
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



@input_error
def add_note(book: NoteBook):
    """
    Add a new note with title and text.

    Args:
        book (NoteBook): NoteBook object to store the note.

    Returns:
        tuple: Success or warning message.
    """
    title = user_input("Write the title of the note:\n>  ")
    title_obj = Title(title)
    if title_obj.value is None:
        return "Title must be 15 characters or less.", "warning"

    text = user_input("Write the text of the note:\n>  ")
    note = book.find_note(title)
    if note:
        return "Note with this title already exists. Change the title", "warning"

    note = Note(title, text)
    return book.add_note(note)

@input_error
def find_note(book: NoteBook):
    """
    Find a note by title.

    Args:
        book (NoteBook): NoteBook to search in.

    Returns:
        tuple: Note content if found, otherwise warning message.
    """
    title = user_input("Enter the title of the note to find:\n>  ")
    note = book.find_note(title)
    if isinstance(note, Note):
        return str(note), "common"
    return "Note with this title doesn't exist.", "warning"

@input_error
def edit_note(book: NoteBook):
    """
    Edit an existing note.

    Args:
        book (NoteBook): NoteBook object containing notes.

    Returns:
        tuple: Success message or warning if not found or empty.
    """
    title = user_input("Write the title of the note to edit:\n>  ")
    note = book.find_note(title)
    if not note:
        return "Note with this title doesn't exist.", "warning"

    new_text = user_input("Write the new text for the note:\n>  ")
    return book.edit_note(title, new_text)

@input_error
def delete_note(book: NoteBook):
    """
    Delete a note by title.

    Args:
        book (NoteBook): NoteBook containing the note.

    Returns:
        tuple: Success message or warning if not found.
    """
    title = user_input("Write the title of the note to delete:\n>  ")
    if not title.strip():
        return "Note title cannot be empty.", "warning"

    message = book.delete_note(title)
    if message is None:
        return "Note not found.", "warning"

    return message

@input_error
def show_all_notes(book: NoteBook):
    """
    Display all notes in the NoteBook.

    Args:
        book (NoteBook): NoteBook containing the notes.

    Returns:
        tuple: List of all notes or a warning if none exist.
    """
    notes = book.show_all_notes()
    if not notes:
        return "No notes found.", "warning"

    return notes, "common list"

@input_error
def search_notes(book: NoteBook):
    """
    Search notes by keyword in title or text.

    Args:
        book (NoteBook): NoteBook to search in.

    Returns:
        tuple: List of matched notes or warning if nothing found.
    """
    keyword = user_input("Enter keyword to search in notes:\n>  ")
    if not keyword.strip():
        return "Please, enter a keyword.", "warning"

    result = book.search_notes(keyword)
    if not result:
        return "No matches found.", "warning"

    results = ["The results of the search:"] + result
    return results, "common list"

@input_error
def import_note(book: NoteBook):
    """
    Import a note from a text file.

    Args:
        book (NoteBook): NoteBook to add the imported note to.

    Returns:
        tuple: Success message or error if the file is invalid.
    """
    file_path = user_input("Enter file path to import note:\n>  ")
    if not os.path.exists(file_path):
        return "File not found.", "error"

    title, _ = os.path.splitext(os.path.basename(file_path))
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    note = Note(title, text)
    return book.add_note(note)

@input_error
def clear_all_notes(book: NoteBook):
    """
    Clear all notes from the NoteBook.

    Args:
        book (NoteBook): NoteBook to clear.

    Returns:
        tuple: Success or warning message if no notes exist.
    """
    if not book.notes:
        return "There are no notes to delete.", "warning"

    return book.clear_all_notes()


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


def save_data(books, filename="data/addressbook_and_notebook.pkl"):
    # створює директорію, якщо вона не існує
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        pickle.dump(books, f)


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
        if not command:
            continue
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
                output(*addressbook.get_upcoming_birthdays(days))
            case 'add-note':
                output(*add_note(notebook))
            case 'find-note':
                output(*find_note(notebook))
            case 'edit-note':
                output(*edit_note(notebook))
            case 'delete-note':
                output(*delete_note(notebook))
            case 'show-all-notes':
                output(*show_all_notes(notebook))
            case 'search-notes':
                output(*search_notes(notebook))
            case 'import-note':
                output(*import_note(notebook))
            case 'clear-all-notes':
                output(*clear_all_notes(notebook))
            case 'all':
                show_table(*show_all(addressbook))
            case _:
                output("Invalid command.", "error")
    save_data((addressbook, notebook))


if __name__ == '__main__':
    main()
